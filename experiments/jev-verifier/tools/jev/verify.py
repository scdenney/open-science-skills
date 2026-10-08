#!/usr/bin/env python3
"""Small, auditable Jev verifier prototype.

The verifier is intentionally not an automatic hook.  A lead supplies an evidence
manifest, explicitly chooses a new output path, and explicitly opts in to either a
mock response or the network.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import math
import os
import platform
import re
import socket
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable


ENDPOINT = "https://api.typesafe.ai/v1/systemone"
DEFAULT_MODEL = "jev-1.13.0"
RESULT_SCHEMA_VERSION = "jev-result-v1"
MANIFEST_SCHEMA_VERSION = "jev-evidence-v1"
FACT_STATE_SCHEMA_VERSION = "jev-fact-check-state-v1"
CITATION_STATE_SCHEMA_VERSION = "jev-citation-check-state-v1"
ROUTE_STATE_SCHEMA_VERSION = "jev-route-state-v2"
ROUTE_RESULT_SCHEMA_VERSION = "jev-route-result-v2"
MAX_INPUT_BYTES = 1_048_576
MAX_ARTIFACT_BYTES = 4_194_304
TIMEOUT_SECONDS = 10.0
MAX_ATTEMPTS = 3
CONTRACT_DIR = Path(__file__).resolve().with_name("contracts")

HEX64 = re.compile(r"^[0-9a-f]{64}$")
SAFE_ID = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
KEYCHAIN_SERVICE = "TypeSafe Jev API"
SECRET_TOOL_SERVICE = "typesafe-jev"

# Routing vocabulary. Jev is asked about the task, never about models: the
# questions below describe the work, and this runtime maps the answers to the
# harness's own executors locally. Model names never leave the machine, so a
# new model release changes the local table, not the questions.
ROUTE_QUESTION_IDS = (
    "task_needs_deep_judgment",
    "task_mostly_mechanical",
    "task_parallelizable",
    "task_context_heavy",
    "task_outlives_session",
    "task_high_stakes",
)
ROUTE_HARNESSES = ("claude", "codex")
# Executors the harness confirms it can launch this session. The runtime never
# infers one; an unconfirmed executor is reported unavailable, not replaced.
ROUTE_EXECUTORS = (
    "premier_lead",
    "fast_worker",
    "deep_reasoner",
    "workflow",
    "spawn_peer",
    "cross_vendor_peer",
)
ROUTE_TOPOLOGIES = (
    "lead",
    "native_subagent",
    "native_workflow",
    "one_shot",
    "spawn_peer",
)
# Keep both harness vocabularies intact: Codex exposes xhigh; Claude exposes
# max. The per-harness caller supplies only values its current session supports.
ROUTE_EFFORTS = ("low", "medium", "high", "xhigh", "max")
ROUTE_BASELINE_FIELD = "lead_choice"
# The local executor table. Claude entries are CLI aliases, so they follow the
# current release; Codex entries are the explicit IDs its policy requires. A
# spawned peer runs on the lead's own model, which the caller reports.
ROUTE_EXECUTOR_MAP: dict[str, dict[str, dict[str, str | None]]] = {
    "claude": {
        "premier_lead": {"topology": "lead", "model": "fable", "effort": "xhigh"},
        "fast_worker": {"topology": "native_subagent", "model": "haiku", "effort": "medium"},
        "deep_reasoner": {"topology": "native_subagent", "model": "opus", "effort": "high"},
        "workflow": {"topology": "native_workflow", "model": None, "effort": None},
        "spawn_peer": {"topology": "spawn_peer", "model": None, "effort": None},
        "cross_vendor_peer": {"topology": "one_shot", "model": "gpt-6-astra", "effort": "xhigh"},
    },
    "codex": {
        "premier_lead": {"topology": "lead", "model": "gpt-6-astra", "effort": "xhigh"},
        "fast_worker": {"topology": "native_subagent", "model": "gpt-6-luna", "effort": "medium"},
        "deep_reasoner": {"topology": "native_subagent", "model": "gpt-6.1-sol", "effort": "high"},
        "workflow": {"topology": "native_workflow", "model": None, "effort": None},
        "spawn_peer": {"topology": "spawn_peer", "model": None, "effort": None},
        "cross_vendor_peer": {"topology": "one_shot", "model": "fable", "effort": "high"},
    },
}
# Lead effort by how hard the task's hardest judgment is. "yes" means the
# premier lead, whose effort comes from the executor table.
ROUTE_LEAD_EFFORT = {"unclear": "high", "no": "medium"}


class ValidationError(ValueError):
    """Expected, sanitized validation failure."""


class NetworkFailure(RuntimeError):
    """Expected, sanitized network/API failure."""


def get_api_key() -> str:
    """Get the credential from the environment or this Mac user's login Keychain."""
    configured = os.environ.get("TYPESAFE_API_KEY", "")
    if configured:
        return configured
    if sys.platform == "darwin":
        command = [
            "/usr/bin/security",
            "find-generic-password",
            "-s",
            KEYCHAIN_SERVICE,
            "-a",
            getpass.getuser(),
            "-w",
        ]
    elif sys.platform.startswith("linux"):
        command = [
            "/usr/bin/secret-tool",
            "lookup",
            "service",
            SECRET_TOOL_SERVICE,
            "account",
            getpass.getuser(),
        ]
    else:
        return ""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.rstrip("\r\n")


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValidationError("duplicate JSON object key")
        value[key] = item
    return value


def _reject_constant(_value: str) -> None:
    raise ValidationError("non-finite JSON number")


def read_json(path: Path) -> tuple[dict[str, Any], str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValidationError("input file is unavailable") from exc
    if len(raw) > MAX_INPUT_BYTES:
        raise ValidationError("input file exceeds size limit")
    digest = hashlib.sha256(raw).hexdigest()
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, ValueError, RecursionError) as exc:
        raise ValidationError("input is not strict JSON") from exc
    if not isinstance(value, dict):
        raise ValidationError("JSON root must be an object")
    return value, digest


def _exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise ValidationError(f"{label} fields do not match schema")


def _string(value: Any, label: str, *, maximum: int = 2_000) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValidationError(f"{label} must be a non-empty bounded string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValidationError(f"{label} must be valid UTF-8 text") from exc
    return value


def _safe_number(value: Any, label: str, *, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{label} must be numeric")
    try:
        number = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValidationError(f"{label} is outside the allowed range") from exc
    if not math.isfinite(number) or number < minimum or number > maximum:
        raise ValidationError(f"{label} is outside the allowed range")
    return number


def _string_list(value: Any, label: str, *, maximum_items: int = 20) -> list[str]:
    if not isinstance(value, list) or not value or len(value) > maximum_items:
        raise ValidationError(f"{label} must be a non-empty bounded array")
    return [_string(item, label) for item in value]


def load_contract(name: str) -> dict[str, Any]:
    if name not in {"orchestrate", "fact-check", "citation-check", "route"}:
        raise ValidationError("unsupported contract")
    value, _ = read_json(CONTRACT_DIR / f"{name}.json")
    _exact_keys(
        value,
        {
            "schema_version",
            "contract",
            "questions_version",
            "model",
            "thresholds",
            "required_checks",
            "questions",
        },
        "contract",
    )
    if value["schema_version"] != "jev-contract-v1" or value["contract"] != name:
        raise ValidationError("contract identity is invalid")
    questions_version = _string(value["questions_version"], "questions_version", maximum=128)
    model = _string(value["model"], "contract model", maximum=128)
    if model != DEFAULT_MODEL:
        raise ValidationError("contract model is not the supported pin")
    required_checks = value["required_checks"]
    if not isinstance(required_checks, list) or not required_checks or len(required_checks) > 20:
        raise ValidationError("contract required_checks is invalid")
    checked_ids: list[str] = []
    for check_id in required_checks:
        check_id = _string(check_id, "required check id", maximum=128)
        if not SAFE_ID.fullmatch(check_id) or check_id in checked_ids:
            raise ValidationError("contract check id is invalid or duplicated")
        checked_ids.append(check_id)

    thresholds = value["thresholds"]
    if not isinstance(thresholds, dict):
        raise ValidationError("contract thresholds must be an object")
    _exact_keys(thresholds, {"pass_min", "fail_max", "calibration"}, "thresholds")
    pass_min = _safe_number(thresholds["pass_min"], "pass_min", minimum=0.0, maximum=1.0)
    fail_max = _safe_number(thresholds["fail_max"], "fail_max", minimum=0.0, maximum=1.0)
    if fail_max >= pass_min:
        raise ValidationError("contract thresholds overlap")
    calibration = _string(thresholds["calibration"], "calibration", maximum=128)

    questions = value["questions"]
    if not isinstance(questions, dict) or not questions or len(questions) > 20:
        raise ValidationError("contract questions must be a non-empty bounded object")
    validated_questions: dict[str, Any] = {}
    for question_id, question in questions.items():
        if not isinstance(question_id, str) or not SAFE_ID.fullmatch(question_id):
            raise ValidationError("question id is invalid")
        if not isinstance(question, dict):
            raise ValidationError("question must be an object")
        _exact_keys(question, {"type", "instructions", "criteria"}, "question")
        if question["type"] != "noul":
            raise ValidationError("only Noul questions are supported")
        instructions = _string(question["instructions"], "question instructions", maximum=4_000)
        criteria = question["criteria"]
        if not isinstance(criteria, dict):
            raise ValidationError("question criteria must be an object")
        _exact_keys(criteria, {"true", "false"}, "question criteria")
        validated_questions[question_id] = {
            "type": "noul",
            "instructions": instructions,
            "criteria": {
                "true": _string(criteria["true"], "true criterion"),
                "false": _string(criteria["false"], "false criterion"),
            },
        }
    canonical_questions = json.dumps(
        validated_questions, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    contract_shapes = {
        "route": {
            "checks": {
                "task_supplied",
                "executor_availability_confirmed",
                "user_constraints_respected",
            },
            "questions": set(ROUTE_QUESTION_IDS),
        },
        "fact-check": {
            "checks": {"readiness", "citation_integrity", "knowledge_base", "evidence_sufficiency"},
            "questions": {
                "source_supports_claim",
                "source_contradicts_claim",
                "scope_matches",
                "strength_matches",
                "direction_magnitude_matches",
                "material_omission_absent",
            },
        },
        "citation-check": {
            "checks": {"retrieval_provenance", "retrieved_evidence", "deterministic_identity"},
            "questions": {"ambiguous_identity_matches", "version_relationship_coherent"},
        },
    }
    if name in contract_shapes:
        shape = contract_shapes[name]
        if set(checked_ids) != shape["checks"] or set(validated_questions) != shape["questions"]:
            raise ValidationError("contract check or question ids are invalid")
    return {
        "contract": name,
        "questions_version": questions_version,
        "questions_sha256": hashlib.sha256(canonical_questions).hexdigest(),
        "model": model,
        "thresholds": {
            "pass_min": pass_min,
            "fail_max": fail_max,
            "calibration": calibration,
        },
        "required_checks": checked_ids,
        "questions": validated_questions,
    }


def read_artifact(path: Path) -> tuple[bytes, str]:
    try:
        if not path.is_file():
            raise ValidationError("evidence artifact is not a regular file")
        with path.open("rb") as handle:
            content = handle.read(MAX_ARTIFACT_BYTES + 1)
    except OSError as exc:
        raise ValidationError("evidence artifact is unavailable") from exc
    if len(content) > MAX_ARTIFACT_BYTES:
        raise ValidationError("evidence artifact exceeds excerpt validation limit")
    return content, hashlib.sha256(content).hexdigest()


def validate_manifest(
    value: dict[str, Any], manifest_path: Path, contract: dict[str, Any]
) -> dict[str, Any]:
    _exact_keys(
        value,
        {
            "schema_version",
            "contract",
            "run_id",
            "task",
            "worker_claim",
            "lead_decision",
            "evidence",
        },
        "manifest",
    )
    if value["schema_version"] != MANIFEST_SCHEMA_VERSION:
        raise ValidationError("unsupported manifest schema_version")
    if value["contract"] != contract["contract"]:
        raise ValidationError("manifest contract mismatch")
    run_id = _string(value["run_id"], "run_id", maximum=128)
    if not SAFE_ID.fullmatch(run_id):
        raise ValidationError("run_id contains unsupported characters")
    task = value["task"]
    if not isinstance(task, dict):
        raise ValidationError("task must be an object")
    _exact_keys(task, {"objective", "acceptance_criteria", "scope_constraints"}, "task")
    validated_task = {
        "objective": _string(task["objective"], "task objective", maximum=4_000),
        "acceptance_criteria": _string_list(
            task["acceptance_criteria"], "acceptance criterion"
        ),
        "scope_constraints": _string_list(task["scope_constraints"], "scope constraint"),
    }
    worker_claim = _string(value["worker_claim"], "worker_claim", maximum=4_000)
    lead_decision = value["lead_decision"]
    if not isinstance(lead_decision, dict):
        raise ValidationError("lead_decision must be an object")
    _exact_keys(lead_decision, {"label"}, "lead_decision")
    lead_label = lead_decision["label"]
    if not isinstance(lead_label, str) or lead_label not in {"PASS", "REWORK", "ESCALATE"}:
        raise ValidationError("lead_decision label is unknown")
    canonical_lead_decision = json.dumps(
        lead_decision, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    lead_decision_hash = hashlib.sha256(canonical_lead_decision).hexdigest()
    evidence = value["evidence"]
    required_checks = contract["required_checks"]
    if not isinstance(evidence, list) or len(evidence) != len(required_checks):
        raise ValidationError("manifest must contain each required evidence check once")

    seen: set[str] = set()
    validated: list[dict[str, Any]] = []
    for index, check in enumerate(evidence):
        if not isinstance(check, dict):
            raise ValidationError("evidence entry must be an object")
        _exact_keys(check, {"check_id", "result", "observation", "artifacts"}, "evidence entry")
        check_id = check["check_id"]
        if (
            not isinstance(check_id, str)
            or check_id not in required_checks
            or check_id in seen
        ):
            raise ValidationError("evidence check_id is unknown or duplicated")
        seen.add(check_id)
        result = check["result"]
        if not isinstance(result, str) or result not in {"pass", "fail", "not_checked"}:
            raise ValidationError("evidence result is unknown")
        observation = _string(check["observation"], "observation")
        artifacts = check["artifacts"]
        if not isinstance(artifacts, list):
            raise ValidationError("artifacts must be an array")
        if result != "not_checked" and not artifacts:
            raise ValidationError("checked evidence requires at least one artifact")
        if result == "not_checked" and artifacts:
            raise ValidationError("not_checked evidence cannot cite artifacts")

        verified_artifacts: list[dict[str, str]] = []
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                raise ValidationError("artifact must be an object")
            _exact_keys(artifact, {"path", "sha256", "excerpt"}, "artifact")
            raw_path = _string(artifact["path"], "artifact path", maximum=1_024)
            expected_hash = artifact["sha256"]
            if not isinstance(expected_hash, str) or not HEX64.fullmatch(expected_hash):
                raise ValidationError("artifact sha256 must be lowercase hexadecimal")
            excerpt = _string(artifact["excerpt"], "artifact excerpt", maximum=4_000)
            candidate = Path(raw_path)
            if not candidate.is_absolute():
                candidate = manifest_path.parent / candidate
            artifact_bytes, actual_hash = read_artifact(candidate)
            if actual_hash != expected_hash:
                raise ValidationError("evidence artifact hash mismatch")
            if excerpt.encode("utf-8") not in artifact_bytes:
                raise ValidationError("evidence excerpt does not occur in artifact")
            verified_artifacts.append({"sha256": actual_hash, "excerpt": excerpt})
        validated.append(
            {
                "check_id": check_id,
                "result": result,
                "observation": observation,
                "artifacts": verified_artifacts,
            }
        )
    if seen != set(required_checks):
        raise ValidationError("required evidence check is missing")
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "contract": contract["contract"],
        "run_id": run_id,
        "task": validated_task,
        "worker_claim": worker_claim,
        "lead_decision": {
            "label": lead_label,
            "sha256": lead_decision_hash,
        },
        "evidence": validated,
    }


FACT_BASELINE_LABELS = {
    "SUPPORTED",
    "PARTIALLY SUPPORTED",
    "UNSUPPORTED",
    "CONTRADICTED",
    "MISATTRIBUTED",
    "SOURCE INSUFFICIENT",
    "NOT IN KB",
    "UNVERIFIABLE",
    "UNVERIFIABLE — citation problem",
}

CITATION_BASELINE_LABELS = {
    "MISSING DOI",
    "NO DOI FOUND",
    "DEAD DOI",
    "DOI RESOLVES TO DIFFERENT WORK",
    "METADATA MISMATCH",
    "TITLE DRIFT",
    "STATUS UPDATE",
    "NEEDS AUTHOR VERIFICATION",
    "LIKELY FABRICATED",
    "SOURCE TEXT NOT CHECKED",
    "AMBIGUOUS",
    "VERIFIED",
    "NOT CHECKED",
}


def _enum(value: Any, allowed: set[str], label: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise ValidationError(f"{label} is unknown")
    return value


def _boolean(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValidationError(f"{label} must be boolean")
    return value


def _optional_string(value: Any, label: str, *, maximum: int = 2_000) -> str | None:
    if value is None:
        return None
    return _string(value, label, maximum=maximum)


def _baseline(value: Any, labels: set[str]) -> dict[str, str]:
    if not isinstance(value, dict):
        raise ValidationError("blind_baseline must be an object")
    _exact_keys(value, {"label"}, "blind_baseline")
    label = _enum(value["label"], labels, "blind baseline label")
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return {"label": label, "sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest()}


def _research_artifacts(value: Any, manifest_path: Path) -> list[dict[str, str]]:
    if not isinstance(value, list) or len(value) > 10:
        raise ValidationError("artifacts must be a bounded array")
    validated: list[dict[str, str]] = []
    for artifact in value:
        if not isinstance(artifact, dict):
            raise ValidationError("artifact must be an object")
        _exact_keys(artifact, {"path", "sha256", "excerpt"}, "artifact")
        raw_path = _string(artifact["path"], "artifact path", maximum=1_024)
        expected_hash = artifact["sha256"]
        if not isinstance(expected_hash, str) or not HEX64.fullmatch(expected_hash):
            raise ValidationError("artifact sha256 must be lowercase hexadecimal")
        excerpt = _string(artifact["excerpt"], "artifact excerpt", maximum=4_000)
        candidate = Path(raw_path)
        if not candidate.is_absolute():
            candidate = manifest_path.parent / candidate
        artifact_bytes, actual_hash = read_artifact(candidate)
        if actual_hash != expected_hash:
            raise ValidationError("evidence artifact hash mismatch")
        if excerpt.encode("utf-8") not in artifact_bytes:
            raise ValidationError("evidence excerpt does not occur in artifact")
        validated.append({"sha256": actual_hash, "excerpt": excerpt})
    return validated


def validate_fact_state(value: dict[str, Any], path: Path, contract: dict[str, Any]) -> dict[str, Any]:
    _exact_keys(
        value,
        {"schema_version", "contract", "run_id", "claim", "source", "evidence", "blind_baseline"},
        "fact-check state",
    )
    if value["schema_version"] != FACT_STATE_SCHEMA_VERSION or value["contract"] != "fact-check":
        raise ValidationError("fact-check state identity is invalid")
    if contract["contract"] != "fact-check":
        raise ValidationError("state contract mismatch")
    run_id = _string(value["run_id"], "run_id", maximum=128)
    if not SAFE_ID.fullmatch(run_id):
        raise ValidationError("run_id contains unsupported characters")

    claim = value["claim"]
    if not isinstance(claim, dict):
        raise ValidationError("claim must be an object")
    _exact_keys(
        claim,
        {"text", "kind", "strength_applicable", "direction_magnitude_applicable", "omission_applicable"},
        "claim",
    )
    validated_claim = {
        "text": _string(claim["text"], "claim text", maximum=4_000),
        "kind": _enum(claim["kind"], {"empirical", "theoretical"}, "claim kind"),
        "strength_applicable": _boolean(claim["strength_applicable"], "strength_applicable"),
        "direction_magnitude_applicable": _boolean(
            claim["direction_magnitude_applicable"], "direction_magnitude_applicable"
        ),
        "omission_applicable": _boolean(claim["omission_applicable"], "omission_applicable"),
    }

    source = value["source"]
    if not isinstance(source, dict):
        raise ValidationError("source must be an object")
    _exact_keys(source, {"identity", "kind", "knowledge_base_status"}, "source")
    validated_source = {
        "identity": _string(source["identity"], "source identity", maximum=2_000),
        "kind": _enum(source["kind"], {"fulltext", "summary"}, "source kind"),
        "knowledge_base_status": _enum(
            source["knowledge_base_status"], {"available", "missing"}, "knowledge base status"
        ),
    }

    evidence = value["evidence"]
    if not isinstance(evidence, dict):
        raise ValidationError("evidence must be an object")
    _exact_keys(evidence, {"readiness", "citation_integrity", "sufficiency", "artifacts"}, "evidence")
    validated_evidence = {
        "readiness": _enum(evidence["readiness"], {"ready", "not_ready"}, "readiness"),
        "citation_integrity": _enum(
            evidence["citation_integrity"], {"valid", "invalid", "not_checked"}, "citation integrity"
        ),
        "sufficiency": _enum(
            evidence["sufficiency"], {"sufficient", "insufficient", "not_checked"}, "evidence sufficiency"
        ),
        "artifacts": _research_artifacts(evidence["artifacts"], path),
    }
    return {
        "schema_version": FACT_STATE_SCHEMA_VERSION,
        "contract": "fact-check",
        "run_id": run_id,
        "claim": validated_claim,
        "source": validated_source,
        "evidence": validated_evidence,
        "blind_baseline": _baseline(value["blind_baseline"], FACT_BASELINE_LABELS),
    }


def validate_citation_state(value: dict[str, Any], path: Path, contract: dict[str, Any]) -> dict[str, Any]:
    _exact_keys(
        value,
        {"schema_version", "contract", "run_id", "bibliographic_entry", "retrieved_record", "blind_baseline"},
        "citation-check state",
    )
    if value["schema_version"] != CITATION_STATE_SCHEMA_VERSION or value["contract"] != "citation-check":
        raise ValidationError("citation-check state identity is invalid")
    if contract["contract"] != "citation-check":
        raise ValidationError("state contract mismatch")
    run_id = _string(value["run_id"], "run_id", maximum=128)
    if not SAFE_ID.fullmatch(run_id):
        raise ValidationError("run_id contains unsupported characters")

    entry = value["bibliographic_entry"]
    if not isinstance(entry, dict):
        raise ValidationError("bibliographic_entry must be an object")
    metadata_keys = {"rendered", "title", "authors", "year", "doi", "version"}
    _exact_keys(entry, metadata_keys, "bibliographic_entry")
    validated_entry = {
        "rendered": _string(entry["rendered"], "rendered bibliographic entry", maximum=4_000),
        **{
            key: _optional_string(entry[key], f"bibliographic {key}", maximum=2_000)
            for key in metadata_keys - {"rendered"}
        },
    }

    record = value["retrieved_record"]
    if not isinstance(record, dict):
        raise ValidationError("retrieved_record must be an object")
    _exact_keys(
        record,
        {"title", "authors", "year", "doi", "version", "deterministic_identity", "retrieval", "artifacts"},
        "retrieved_record",
    )
    retrieval = record["retrieval"]
    if not isinstance(retrieval, dict):
        raise ValidationError("retrieval must be an object")
    _exact_keys(retrieval, {"provider", "url", "retrieved_at", "status"}, "retrieval")
    validated_record = {
        **{
            key: _optional_string(record[key], f"retrieved {key}", maximum=2_000)
            for key in {"title", "authors", "year", "doi", "version"}
        },
        "deterministic_identity": _enum(
            record["deterministic_identity"],
            {"match", "different_work", "ambiguous", "not_checked"},
            "deterministic identity",
        ),
        "retrieval": {
            "provider": _string(retrieval["provider"], "retrieval provider", maximum=256),
            "url": _string(retrieval["url"], "retrieval URL", maximum=2_000),
            "retrieved_at": _string(retrieval["retrieved_at"], "retrieval time", maximum=128),
            "status": _enum(retrieval["status"], {"success", "not_found", "error"}, "retrieval status"),
        },
        "artifacts": _research_artifacts(record["artifacts"], path),
    }
    return {
        "schema_version": CITATION_STATE_SCHEMA_VERSION,
        "contract": "citation-check",
        "run_id": run_id,
        "bibliographic_entry": validated_entry,
        "retrieved_record": validated_record,
        "blind_baseline": _baseline(value["blind_baseline"], CITATION_BASELINE_LABELS),
    }


def _route_baseline(value: Any) -> dict[str, str]:
    """Hash the lead's own pre-Jev plan; the plan itself is never kept."""
    if not isinstance(value, dict):
        raise ValidationError("blind_baseline must be an object")
    _exact_keys(value, {ROUTE_BASELINE_FIELD}, "blind_baseline")
    choice = _string(value[ROUTE_BASELINE_FIELD], "lead_choice", maximum=2_000)
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return {"sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(), "length": len(choice)}


def validate_route_state(value: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    _exact_keys(
        value,
        {
            "schema_version",
            "contract",
            "run_id",
            "task",
            "harness",
            "lead",
            "available",
            "constraints",
            "blind_baseline",
        },
        "route state",
    )
    if value["schema_version"] != ROUTE_STATE_SCHEMA_VERSION or value["contract"] != "route":
        raise ValidationError("route state identity is invalid")
    if contract["contract"] != "route":
        raise ValidationError("state contract mismatch")
    run_id = _string(value["run_id"], "run_id", maximum=128)
    if not SAFE_ID.fullmatch(run_id):
        raise ValidationError("run_id contains unsupported characters")

    task = value["task"]
    if not isinstance(task, dict):
        raise ValidationError("task must be an object")
    _exact_keys(task, {"objective", "acceptance_criteria", "scope_constraints"}, "task")
    validated_task = {
        "objective": _string(task["objective"], "task objective", maximum=4_000),
        "acceptance_criteria": _string_list(task["acceptance_criteria"], "acceptance criterion"),
        "scope_constraints": _string_list(task["scope_constraints"], "scope constraint"),
    }

    lead = value["lead"]
    if not isinstance(lead, dict):
        raise ValidationError("lead must be an object")
    _exact_keys(lead, {"model", "effort"}, "lead")
    validated_lead = {
        # The model the session reports it is running, not a claim about it.
        "model": _string(lead["model"], "lead model", maximum=128),
        "effort": _enum(lead["effort"], set(ROUTE_EFFORTS), "lead effort"),
    }

    available = value["available"]
    if not isinstance(available, dict):
        raise ValidationError("available must be an object")
    _exact_keys(available, set(ROUTE_EXECUTORS), "available")
    # The harness owns every flag. This runtime cannot observe an entitlement
    # or a harness capability and never infers one.
    validated_available = {
        key: _boolean(available[key], f"availability {key}") for key in ROUTE_EXECUTORS
    }

    constraints = value["constraints"]
    if not isinstance(constraints, dict):
        raise ValidationError("constraints must be an object")
    _exact_keys(constraints, {"model", "effort", "topology"}, "constraints")
    validated_constraints = {
        "model": _optional_string(constraints["model"], "pinned model", maximum=128),
        "effort": None
        if constraints["effort"] is None
        else _enum(constraints["effort"], set(ROUTE_EFFORTS), "pinned effort"),
        "topology": None
        if constraints["topology"] is None
        else _enum(constraints["topology"], set(ROUTE_TOPOLOGIES), "pinned topology"),
    }
    canonical_available = json.dumps(
        validated_available, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return {
        "schema_version": ROUTE_STATE_SCHEMA_VERSION,
        "contract": "route",
        "run_id": run_id,
        "task": validated_task,
        "harness": _enum(value["harness"], set(ROUTE_HARNESSES), "harness"),
        "lead": validated_lead,
        "available": validated_available,
        "available_sha256": hashlib.sha256(canonical_available).hexdigest(),
        "constraints": validated_constraints,
        "blind_baseline": _route_baseline(value["blind_baseline"]),
    }


def route_api_state(state: dict[str, Any]) -> dict[str, Any]:
    """Return the bounded remote state: the task and nothing else.

    Withheld deliberately: the harness, the lead's model, the executor table,
    and availability, because mapping a task profile to executors is local
    arithmetic; and the lead's own blind plan, so the answer cannot be
    anchored by it. No model name is sent, so the questions do not depend on
    Jev knowing a model released after it was trained.
    """
    return {"contract": "route", "run_id": state["run_id"], "task": state["task"]}


def signal_reading(probability: float, thresholds: dict[str, Any]) -> str:
    if probability >= thresholds["pass_min"]:
        return "yes"
    if probability <= thresholds["fail_max"]:
        return "no"
    return "unclear"


def route_signals(probabilities: dict[str, float], thresholds: dict[str, Any]) -> dict[str, Any]:
    return {
        question_id: {
            "probability": probabilities[question_id],
            "reading": signal_reading(probabilities[question_id], thresholds),
        }
        for question_id in ROUTE_QUESTION_IDS
    }


def _same_family(reported_model: str, alias: str) -> bool:
    """A session reports a full ID (claude-fable-5-1); the table holds an alias."""
    return alias.lower() in reported_model.lower()


def _route_lead(state: dict[str, Any], deep: str) -> dict[str, Any]:
    lead = state["lead"]
    pins = state["constraints"]
    if pins["model"] is not None or pins["effort"] is not None:
        return {
            "model": pins["model"] or lead["model"],
            "effort": pins["effort"] or lead["effort"],
            "status": "pinned",
        }
    if deep == "yes":
        premier = ROUTE_EXECUTOR_MAP[state["harness"]]["premier_lead"]
        if _same_family(lead["model"], premier["model"]):
            status = "keep" if lead["effort"] == premier["effort"] else "change_effort"
        elif not state["available"]["premier_lead"]:
            status = "unavailable"
        else:
            status = "switch_suggested"
        return {"model": premier["model"], "effort": premier["effort"], "status": status}
    effort = ROUTE_LEAD_EFFORT[deep]
    return {
        "model": lead["model"],
        "effort": effort,
        "status": "keep" if lead["effort"] == effort else "change_effort",
    }


def route_plan(
    state: dict[str, Any], probabilities: dict[str, float], thresholds: dict[str, Any]
) -> tuple[str, list[str], dict[str, Any]]:
    """Map the task profile to a proposed plan through the local executor table.

    Every item names the signal that triggered it. An unclear signal is marked
    for review, an unconfirmed executor is marked unavailable, and neither is
    replaced by a different executor.
    """
    readings = {
        question_id: signal_reading(probabilities[question_id], thresholds)
        for question_id in ROUTE_QUESTION_IDS
    }
    table = ROUTE_EXECUTOR_MAP[state["harness"]]
    available = state["available"]
    pinned_topology = state["constraints"]["topology"]
    deep = readings["task_needs_deep_judgment"]
    items: list[dict[str, Any]] = []

    def add(executor: str, purpose: str, trigger: str) -> None:
        spec = table[executor]
        own_model = executor == "spawn_peer"
        reading = readings[trigger]
        if reading == "unclear":
            status = "review"
        elif not available[executor]:
            status = "unavailable"
        elif pinned_topology is not None and spec["topology"] != pinned_topology:
            status = "excluded_by_pin"
        else:
            status = "proposed"
        items.append(
            {
                "executor": executor,
                "purpose": purpose,
                "topology": spec["topology"],
                "model": state["lead"]["model"] if own_model else spec["model"],
                "effort": state["lead"]["effort"] if own_model else spec["effort"],
                "trigger": trigger,
                "status": status,
            }
        )

    def wanted(question_id: str) -> bool:
        return readings[question_id] in {"yes", "unclear"}

    if wanted("task_mostly_mechanical"):
        add("fast_worker", "carry out the fully specified work", "task_mostly_mechanical")
    if wanted("task_parallelizable"):
        if available["workflow"]:
            fan_out = "workflow"
        else:
            fan_out = "deep_reasoner" if deep == "yes" else "fast_worker"
        add(fan_out, "run the independent units in parallel", "task_parallelizable")
    if wanted("task_context_heavy"):
        reader = "fast_worker" if deep == "no" else "deep_reasoner"
        add(reader, "read the material in a separate context and report back", "task_context_heavy")
    if wanted("task_outlives_session"):
        add("spawn_peer", "run as a peer session in its own worktree", "task_outlives_session")
    if wanted("task_high_stakes"):
        add("cross_vendor_peer", "blind cross-check before the result is final", "task_high_stakes")

    lead = _route_lead(state, deep)
    unclear = [question_id for question_id in ROUTE_QUESTION_IDS if readings[question_id] == "unclear"]
    reasons: list[str] = []
    if lead["status"] == "pinned":
        reasons.append("user_pin_applied")
    elif lead["status"] in {"switch_suggested", "change_effort"}:
        reasons.append("lead_change_suggested")
    elif lead["status"] == "unavailable":
        reasons.append("premier_lead_unavailable")
    if any(item["status"] == "unavailable" for item in items):
        reasons.append("some_executors_unavailable")
    if any(item["status"] == "excluded_by_pin" for item in items):
        reasons.append("topology_pin_excluded_items")
    detail = {
        "lead": lead,
        "items": items,
        "keep_in_lead": not any(item["status"] == "proposed" for item in items),
        "unclear_signals": unclear,
    }
    if any(item["status"] == "review" for item in items):
        return "REVIEW_REQUIRED", ["unclear_task_signal", *reasons], detail
    return "PLAN_PROPOSED", reasons or ["task_profile_mapped"], detail


def _route_result(contract: dict[str, Any], mode: str) -> dict[str, Any]:
    return {
        "schema_version": ROUTE_RESULT_SCHEMA_VERSION,
        "run_id": None,
        "contract": "route",
        "mode": mode,
        "runtime_status": "not_completed",
        "route_status": "not_run",
        "live_assessed": False,
        # A routing recommendation is not, and never becomes, a completion check.
        "completion_verified": False,
        "input_state_sha256": None,
        "blind_baseline_sha256": None,
        "availability_sha256": None,
        "reason_codes": [],
        "recommendation": {
            "outcome": "NOT_CHECKED",
            "lead": None,
            "items": [],
            "keep_in_lead": None,
            "unclear_signals": [],
            # This runtime writes a file. It launches nothing, ever.
            "applied": False,
        },
        "jev": {
            "requested_model": contract["model"],
            "response_model": None,
            "questions_version": contract["questions_version"],
            "questions_sha256": contract["questions_sha256"],
            "calls": 0,
            "latency_ms": None,
            "usage": None,
            "signals": None,
            "simulated_outcome": None,
            "simulated_plan": None,
        },
        "thresholds": contract["thresholds"],
    }


def run_route(args: argparse.Namespace) -> int:
    output = Path(args.out)
    if output.exists() or output.is_symlink():
        print("error: output path already exists; refusing overwrite", file=sys.stderr)
        return 2
    try:
        contract = load_contract("route")
    except ValidationError as exc:
        print(f"error: bundled contract is invalid: {exc}", file=sys.stderr)
        return 2

    result = _route_result(contract, args.mode)
    exit_code = 0
    try:
        raw_state, state_hash = read_json(Path(args.state))
        result["input_state_sha256"] = state_hash
        state = validate_route_state(raw_state, contract)
        result["run_id"] = state["run_id"]
        result["blind_baseline_sha256"] = state["blind_baseline"]["sha256"]
        result["availability_sha256"] = state["available_sha256"]
        thresholds = contract["thresholds"]

        if args.mock_response:
            raw_response, _ = read_json(Path(args.mock_response))
            fixture = validate_response(raw_response, contract)
            outcome, _reasons, detail = route_plan(state, fixture["probabilities"], thresholds)
            result["runtime_status"] = "completed"
            result["route_status"] = "simulation"
            result["reason_codes"] = ["mock_response_not_live_routing"]
            # A simulated answer may not propose a plan: nothing downstream may
            # read one out of a fixture and act on it.
            result["jev"].update(
                {
                    "signals": route_signals(fixture["probabilities"], thresholds),
                    "simulated_outcome": outcome,
                    "simulated_plan": detail,
                }
            )
        elif args.allow_network:
            payload = {
                "state": route_api_state(state),
                "model": contract["model"],
                "questions": contract["questions"],
            }
            raw_response, latency_ms = post_live(payload, get_api_key())
            response = validate_response(raw_response, contract)
            outcome, reasons, detail = route_plan(state, response["probabilities"], thresholds)
            result["runtime_status"] = "completed"
            result["route_status"] = "live"
            result["live_assessed"] = True
            result["reason_codes"] = reasons
            result["recommendation"].update(detail)
            result["recommendation"]["outcome"] = outcome
            result["jev"].update(
                {
                    "response_model": response["model"],
                    "calls": 1,
                    "latency_ms": latency_ms,
                    "usage": response["usage"],
                    "signals": route_signals(response["probabilities"], thresholds),
                }
            )
        else:
            result["reason_codes"] = ["network_not_enabled_and_no_mock_supplied"]
            exit_code = 2
    except ValidationError:
        result["reason_codes"] = ["schema_or_state_validation_failed"]
        exit_code = 2
    except NetworkFailure as exc:
        result["reason_codes"] = ["live_routing_failed"]
        print(f"error: {exc}", file=sys.stderr)
        exit_code = 2

    try:
        write_new_json(output, result)
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.mode == "advisory":
        recommendation = result["recommendation"]
        lead = recommendation["lead"]
        lead_text = f"{lead['model']}/{lead['effort']} ({lead['status']})" if lead else "none"
        proposed = sum(1 for item in recommendation["items"] if item["status"] == "proposed")
        print(
            f"advisory route outcome: {recommendation['outcome']}; lead: {lead_text}; "
            f"proposed delegations: {proposed}; result written to {output}"
        )
    else:
        print(f"shadow route result written to {output}; outcome intentionally not displayed")
    return exit_code


def deterministic_decision(evidence: list[dict[str, Any]]) -> tuple[str | None, list[str]]:
    results = {item["check_id"]: item["result"] for item in evidence}
    if any(result == "fail" for result in results.values()):
        return "REWORK", ["deterministic_check_failed"]
    if any(result == "not_checked" for result in results.values()):
        return "ESCALATE", ["deterministic_check_not_checked"]
    return None, []


def api_state(manifest: dict[str, Any]) -> dict[str, Any]:
    # Paths and unselected file contents are deliberately excluded. The lead's
    # bounded, hash-verified excerpts are the only artifact source text sent.
    # lead_decision is also excluded so Jev cannot be anchored by the blind label.
    return {
        "contract": manifest["contract"],
        "run_id": manifest["run_id"],
        "task": manifest["task"],
        "worker_claim": manifest["worker_claim"],
        "evidence": manifest["evidence"],
    }


def research_api_state(state: dict[str, Any]) -> dict[str, Any]:
    """Return the bounded remote state, excluding paths and blind judgments."""
    if state["contract"] == "fact-check":
        return {
            "contract": "fact-check",
            "run_id": state["run_id"],
            "claim": state["claim"],
            "source": state["source"],
            "evidence": state["evidence"],
        }
    record = state["retrieved_record"]
    return {
        "contract": "citation-check",
        "run_id": state["run_id"],
        "bibliographic_entry": state["bibliographic_entry"],
        "retrieved_record": {
            "title": record["title"],
            "authors": record["authors"],
            "year": record["year"],
            "doi": record["doi"],
            "version": record["version"],
            "deterministic_identity": record["deterministic_identity"],
            "retrieval": record["retrieval"],
            "artifacts": record["artifacts"],
        },
    }


def research_preflight(state: dict[str, Any]) -> tuple[str | None, list[str]]:
    """Return a conservative local outcome and every independently failed gate."""
    reasons: list[str] = []
    if state["contract"] == "fact-check":
        evidence = state["evidence"]
        if evidence["readiness"] != "ready":
            reasons.append("research_not_ready")
        if state["source"]["knowledge_base_status"] != "available":
            reasons.append("knowledge_base_missing")
        if evidence["citation_integrity"] == "invalid":
            reasons.append("citation_integrity_invalid")
        elif evidence["citation_integrity"] == "not_checked":
            reasons.append("citation_integrity_not_checked")
        if evidence["sufficiency"] == "insufficient":
            reasons.append("source_evidence_insufficient")
        elif evidence["sufficiency"] == "not_checked":
            reasons.append("source_evidence_not_checked")
        if not evidence["artifacts"]:
            reasons.append("passage_evidence_missing")
        if reasons:
            outcome = "INVALID_CITATION" if "citation_integrity_invalid" in reasons else "NOT_CHECKED"
            return outcome, reasons
        return None, []

    record = state["retrieved_record"]
    if record["retrieval"]["status"] != "success":
        reasons.append("retrieval_not_successful")
    if not record["artifacts"]:
        reasons.append("retrieved_evidence_missing")
    entry = state["bibliographic_entry"]
    if not entry["title"] or not entry["authors"] or not record["title"] or not record["authors"]:
        reasons.append("identity_comparison_fields_missing")
    identity = record["deterministic_identity"]
    if identity == "not_checked":
        reasons.append("deterministic_identity_not_checked")
    if reasons:
        return "NOT_CHECKED", reasons
    if identity == "different_work":
        return "DIFFERENT_WORK", ["deterministic_different_work"]
    if identity == "match":
        return "VERIFIED", ["deterministic_identity_match"]
    return None, []


def applicable_question_ids(state: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    ids = list(contract["questions"])
    if state["contract"] != "fact-check":
        return ids
    applicability = {
        "strength_matches": "strength_applicable",
        "direction_magnitude_matches": "direction_magnitude_applicable",
        "material_omission_absent": "omission_applicable",
    }
    return [
        question_id
        for question_id in ids
        if question_id not in applicability or state["claim"][applicability[question_id]]
    ]


def research_model_outcome(
    state: dict[str, Any], probabilities: dict[str, float], contract: dict[str, Any]
) -> tuple[str, list[str], list[dict[str, Any]]]:
    applicable = applicable_question_ids(state, contract)
    thresholds = contract["thresholds"]
    signals = []
    for question_id in applicable:
        probability = probabilities[question_id]
        category = (
            "positive"
            if probability >= thresholds["pass_min"]
            else "negative"
            if probability <= thresholds["fail_max"]
            else "ambiguous"
        )
        signals.append({"question_id": question_id, "probability": probability, "category": category})

    if state["contract"] == "fact-check":
        contradiction = probabilities["source_contradicts_claim"]
        positive_ids = [item for item in applicable if item != "source_contradicts_claim"]
        if (
            contradiction >= thresholds["pass_min"]
            and probabilities["source_supports_claim"] >= thresholds["pass_min"]
        ):
            return "REVIEW_REQUIRED", ["conflicting_support_and_contradiction_signals"], signals
        if contradiction >= thresholds["pass_min"]:
            return "CONTRADICTED", ["explicit_contradiction_signal"], signals
        if (
            contradiction <= thresholds["fail_max"]
            and positive_ids
            and all(probabilities[item] >= thresholds["pass_min"] for item in positive_ids)
        ):
            return "SUPPORTED", ["applicable_support_signals_positive"], signals
        return "REVIEW_REQUIRED", ["mixed_or_ambiguous_fact_signals"], signals

    values = [probabilities[item] for item in applicable]
    if values and all(value >= thresholds["pass_min"] for value in values):
        return "VERIFIED", ["ambiguous_identity_signals_match"], signals
    return "REVIEW_REQUIRED", ["ambiguous_identity_requires_review"], signals


def validate_response(value: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    _exact_keys(value, {"model", "answers", "usage"}, "API response")
    model = _string(value["model"], "response model", maximum=128)
    if model != contract["model"]:
        raise ValidationError("response model does not match pinned model")
    answers = value["answers"]
    questions = contract["questions"]
    if not isinstance(answers, dict) or set(answers) != set(questions):
        raise ValidationError("response answer ids do not match questions")
    probabilities: dict[str, float] = {}
    for question_id in questions:
        answer = answers[question_id]
        if not isinstance(answer, dict):
            raise ValidationError("response answer must be an object")
        _exact_keys(answer, {"type", "noul"}, "Noul answer")
        if answer["type"] != "noul":
            raise ValidationError("response contains an unknown answer type")
        probabilities[question_id] = _safe_number(
            answer["noul"], f"answer {question_id}", minimum=0.0, maximum=1.0
        )
    usage = value["usage"]
    if not isinstance(usage, dict):
        raise ValidationError("usage must be an object")
    _exact_keys(usage, {"input_tokens", "output_tokens"}, "usage")
    for key in ("input_tokens", "output_tokens"):
        token_count = usage[key]
        if isinstance(token_count, bool) or not isinstance(token_count, int) or token_count < 0:
            raise ValidationError("usage token counts must be non-negative integers")
    return {"model": model, "probabilities": probabilities, "usage": usage}


def model_decision(
    probabilities: dict[str, float], thresholds: dict[str, Any]
) -> tuple[str, list[str]]:
    if any(value <= thresholds["fail_max"] for value in probabilities.values()):
        return "REWORK", ["jev_negative_signal"]
    if all(value >= thresholds["pass_min"] for value in probabilities.values()):
        return "PASS", ["jev_positive_signals"]
    return "ESCALATE", ["jev_ambiguous_signal"]


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


def post_live(
    payload: dict[str, Any],
    api_key: str,
    *,
    opener: Any | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[dict[str, Any], int]:
    if not api_key or "\n" in api_key or "\r" in api_key:
        raise NetworkFailure("TYPESAFE_API_KEY is missing or invalid")
    body = json.dumps(payload, allow_nan=False, separators=(",", ":")).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "open-science-jev-verifier/0.1",
        },
    )
    client = opener or urllib.request.build_opener(
        _NoRedirect(), urllib.request.HTTPSHandler(context=ssl.create_default_context())
    )
    started = time.monotonic()
    for attempt in range(MAX_ATTEMPTS):
        try:
            with client.open(request, timeout=TIMEOUT_SECONDS) as response:
                if response.geturl() != ENDPOINT:
                    raise NetworkFailure("API redirect refused")
                status = getattr(response, "status", 200)
                if status != 200:
                    raise NetworkFailure(f"API returned HTTP {status}")
                raw = response.read(MAX_INPUT_BYTES + 1)
                if len(raw) > MAX_INPUT_BYTES:
                    raise NetworkFailure("API response exceeds size limit")
                try:
                    value = json.loads(
                        raw.decode("utf-8"),
                        object_pairs_hook=_strict_object,
                        parse_constant=_reject_constant,
                    )
                except (UnicodeDecodeError, ValueError, RecursionError) as exc:
                    raise NetworkFailure("API response is not strict JSON") from exc
                if not isinstance(value, dict):
                    raise NetworkFailure("API response root is not an object")
                return value, round((time.monotonic() - started) * 1_000)
        except urllib.error.HTTPError as exc:
            # Do not read or expose the response body: it may echo submitted content.
            if 300 <= exc.code < 400:
                raise NetworkFailure("API redirect refused") from exc
            if exc.code not in {429, 529} or attempt + 1 == MAX_ATTEMPTS:
                raise NetworkFailure(f"API returned HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
            if attempt + 1 == MAX_ATTEMPTS:
                raise NetworkFailure("API request failed after bounded retries") from exc
        sleep(min(0.25 * (2**attempt), 1.0))
    raise NetworkFailure("API request failed after bounded retries")


def _base_result(
    *,
    contract: dict[str, Any],
    mode: str,
    manifest_hash: str | None,
    run_id: str | None,
) -> dict[str, Any]:
    return {
        "schema_version": RESULT_SCHEMA_VERSION,
        "run_id": run_id,
        "contract": contract["contract"],
        "mode": mode,
        "verification_status": "not_run",
        "live_verified": False,
        "decision": "ESCALATE",
        "reason_codes": [],
        "input_manifest_sha256": manifest_hash,
        "deterministic_checks": [],
        "lead_decision": None,
        "jev": {
            "requested_model": contract["model"],
            "response_model": None,
            "questions_version": contract["questions_version"],
            "questions_sha256": contract["questions_sha256"],
            "latency_ms": None,
            "usage": None,
            "probabilities": None,
            "simulated_decision": None,
        },
        "thresholds": contract["thresholds"],
    }


def _sanitized_checks(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": item["check_id"],
            "result": item["result"],
            "artifact_hashes": [artifact["sha256"] for artifact in item["artifacts"]],
        }
        for item in manifest["evidence"]
    ]


def write_new_json(path: Path, value: dict[str, Any]) -> None:
    payload = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise ValidationError("output path already exists; refusing overwrite") from exc
    except OSError as exc:
        raise ValidationError("output path cannot be created") from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            path.unlink()
        except OSError:
            pass
        raise


def _research_result(contract: dict[str, Any], mode: str) -> dict[str, Any]:
    return {
        "schema_version": "jev-research-result-v1",
        "run_id": None,
        "contract": contract["contract"],
        "mode": mode,
        "runtime_status": "not_completed",
        "verification_status": "not_run",
        "live_verified": False,
        "content_certified": False,
        "input_state_sha256": None,
        "blind_baseline_sha256": None,
        "evidence_hashes": [],
        "reason_codes": [],
        "assessment": {
            "proposed_outcome": "NOT_CHECKED",
            "advisory_categories": [],
            "signals": [],
        },
        "jev": {
            "requested_model": contract["model"],
            "response_model": None,
            "questions_version": contract["questions_version"],
            "questions_sha256": contract["questions_sha256"],
            "latency_ms": None,
            "usage": None,
            "probabilities": None,
            "simulated_outcome": None,
            "simulated_signals": None,
        },
        "thresholds": contract["thresholds"],
    }


def _research_hashes(state: dict[str, Any]) -> list[str]:
    artifacts = (
        state["evidence"]["artifacts"]
        if state["contract"] == "fact-check"
        else state["retrieved_record"]["artifacts"]
    )
    return [item["sha256"] for item in artifacts]


def run_research_verify(args: argparse.Namespace, contract: dict[str, Any], output: Path) -> int:
    state_path = Path(args.state)
    result = _research_result(contract, args.mode)
    exit_code = 0
    try:
        raw_state, state_hash = read_json(state_path)
        result["input_state_sha256"] = state_hash
        if contract["contract"] == "fact-check":
            state = validate_fact_state(raw_state, state_path, contract)
        else:
            state = validate_citation_state(raw_state, state_path, contract)
        result["run_id"] = state["run_id"]
        result["blind_baseline_sha256"] = state["blind_baseline"]["sha256"]
        result["evidence_hashes"] = _research_hashes(state)
        deterministic, deterministic_reasons = research_preflight(state)

        if deterministic is not None:
            result["runtime_status"] = "completed"
            result["verification_status"] = "deterministic"
            result["assessment"]["proposed_outcome"] = deterministic
            result["assessment"]["advisory_categories"] = deterministic_reasons
            result["reason_codes"] = deterministic_reasons
        elif args.mock_response:
            raw_response, _ = read_json(Path(args.mock_response))
            response = validate_response(raw_response, contract)
            outcome, categories, signals = research_model_outcome(
                state, response["probabilities"], contract
            )
            result["runtime_status"] = "completed"
            result["verification_status"] = "simulation"
            result["reason_codes"] = ["mock_response_not_live_verification"]
            result["assessment"]["advisory_categories"] = ["simulation_not_content_verification"]
            result["jev"].update(
                {
                    "response_model": response["model"],
                    "latency_ms": 0,
                    "usage": response["usage"],
                    "probabilities": response["probabilities"],
                    "simulated_outcome": outcome,
                    "simulated_signals": signals,
                }
            )
        elif args.allow_network:
            payload = {
                "state": research_api_state(state),
                "model": contract["model"],
                "questions": contract["questions"],
            }
            raw_response, latency_ms = post_live(payload, get_api_key())
            response = validate_response(raw_response, contract)
            outcome, categories, signals = research_model_outcome(
                state, response["probabilities"], contract
            )
            result["runtime_status"] = "completed"
            result["verification_status"] = "live"
            result["live_verified"] = True
            result["reason_codes"] = categories
            result["assessment"] = {
                "proposed_outcome": outcome,
                "advisory_categories": categories,
                "signals": signals,
            }
            result["jev"].update(
                {
                    "response_model": response["model"],
                    "latency_ms": latency_ms,
                    "usage": response["usage"],
                    "probabilities": response["probabilities"],
                }
            )
        else:
            result["reason_codes"] = ["network_not_enabled_and_no_mock_supplied"]
            exit_code = 2
    except ValidationError:
        result["reason_codes"] = ["schema_or_evidence_validation_failed"]
        exit_code = 2
    except NetworkFailure as exc:
        result["reason_codes"] = ["live_verification_failed"]
        print(f"error: {exc}", file=sys.stderr)
        exit_code = 2

    try:
        write_new_json(output, result)
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.mode == "advisory":
        print(
            f"advisory research outcome: {result['assessment']['proposed_outcome']}; "
            f"result written to {output}"
        )
    else:
        print(f"shadow result written to {output}; outcome intentionally not displayed")
    return exit_code


def run_verify(args: argparse.Namespace) -> int:
    output = Path(args.out)
    # Check first so even malformed inputs cannot overwrite an existing audit record.
    if output.exists() or output.is_symlink():
        print("error: output path already exists; refusing overwrite", file=sys.stderr)
        return 2

    try:
        contract = load_contract(args.contract)
    except ValidationError as exc:
        print(f"error: bundled contract is invalid: {exc}", file=sys.stderr)
        return 2
    if args.contract in {"fact-check", "citation-check"}:
        return run_research_verify(args, contract, output)
    state_path = Path(args.state)
    manifest_hash: str | None = None
    run_id: str | None = None
    result = _base_result(
        contract=contract, mode=args.mode, manifest_hash=None, run_id=None
    )
    deterministic: str | None = None
    deterministic_reasons: list[str] = []
    exit_code = 0
    try:
        raw_manifest, manifest_hash = read_json(state_path)
        result["input_manifest_sha256"] = manifest_hash
        manifest = validate_manifest(raw_manifest, state_path, contract)
        run_id = manifest["run_id"]
        result["run_id"] = run_id
        result["lead_decision"] = manifest["lead_decision"]
        result["deterministic_checks"] = _sanitized_checks(manifest)
        deterministic, deterministic_reasons = deterministic_decision(manifest["evidence"])

        if args.mock_response:
            raw_response, _ = read_json(Path(args.mock_response))
            response = validate_response(raw_response, contract)
            evaluated, evaluated_reasons = model_decision(
                response["probabilities"], contract["thresholds"]
            )
            result["verification_status"] = "simulation"
            result["reason_codes"] = ["mock_response_not_live_verification"]
            if deterministic is not None:
                result["reason_codes"].extend(deterministic_reasons)
            result["jev"].update(
                {
                    "response_model": response["model"],
                    "latency_ms": 0,
                    "usage": response["usage"],
                    "probabilities": response["probabilities"],
                    "simulated_decision": deterministic or evaluated,
                }
            )
            # A mock is useful to exercise routing, but cannot certify the work.
            result["decision"] = "ESCALATE"
            if deterministic is None:
                result["reason_codes"].extend(evaluated_reasons)
        elif args.allow_network:
            api_key = get_api_key()
            payload = {
                "state": api_state(manifest),
                "model": contract["model"],
                "questions": contract["questions"],
            }
            raw_response, latency_ms = post_live(payload, api_key)
            response = validate_response(raw_response, contract)
            evaluated, evaluated_reasons = model_decision(
                response["probabilities"], contract["thresholds"]
            )
            result["verification_status"] = "live"
            result["live_verified"] = True
            result["decision"] = deterministic or evaluated
            result["reason_codes"] = deterministic_reasons or evaluated_reasons
            result["jev"].update(
                {
                    "response_model": response["model"],
                    "latency_ms": latency_ms,
                    "usage": response["usage"],
                    "probabilities": response["probabilities"],
                }
            )
        else:
            result["reason_codes"] = ["network_not_enabled_and_no_mock_supplied"]
            if deterministic is not None:
                result["reason_codes"].extend(deterministic_reasons)
            exit_code = 2
    except ValidationError:
        result["decision"] = "ESCALATE"
        result["reason_codes"] = ["schema_or_evidence_validation_failed"]
        exit_code = 2
    except NetworkFailure as exc:
        result["decision"] = deterministic or "ESCALATE"
        result["reason_codes"] = deterministic_reasons + ["live_verification_failed"]
        print(f"error: {exc}", file=sys.stderr)
        exit_code = 2

    try:
        write_new_json(output, result)
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.mode == "advisory":
        print(f"advisory decision: {result['decision']}; result written to {output}")
    else:
        print(f"shadow result written to {output}; decision intentionally not displayed")
    return exit_code


def run_doctor(args: argparse.Namespace) -> int:
    try:
        contract = load_contract(args.contract)
        contract_valid = True
    except ValidationError:
        contract = {
            "model": DEFAULT_MODEL,
            "questions_version": None,
            "questions_sha256": None,
        }
        contract_valid = False
    supported = sys.platform.startswith("linux") or sys.platform == "darwin"
    report = {
        "supported_platform": supported,
        "platform": "macOS" if sys.platform == "darwin" else "Linux" if sys.platform.startswith("linux") else platform.system(),
        "python": platform.python_version(),
        "python_supported": sys.version_info >= (3, 10),
        "contract_valid": contract_valid,
        "contract": args.contract,
        "network_opt_in": bool(args.allow_network),
        "api_key_present": bool(get_api_key()),
        "endpoint": ENDPOINT,
        "model": contract["model"],
        "questions_version": contract["questions_version"],
        "questions_sha256": contract["questions_sha256"],
        "note": "doctor performs no API request",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if supported and sys.version_info >= (3, 10) and contract_valid else 2


def validate_result_for_adjudication(value: dict[str, Any]) -> str:
    if value.get("schema_version") != RESULT_SCHEMA_VERSION:
        raise ValidationError("unsupported result schema")
    mode = value.get("mode")
    if not isinstance(mode, str) or mode not in {"shadow", "advisory"}:
        raise ValidationError("result mode is invalid")
    run_id = value.get("run_id")
    if run_id is not None:
        _string(run_id, "run_id", maximum=128)
    return run_id


def run_adjudicate(args: argparse.Namespace) -> int:
    output = Path(args.out)
    if output.exists() or output.is_symlink():
        print("error: output path already exists; refusing overwrite", file=sys.stderr)
        return 2
    try:
        result, result_hash = read_json(Path(args.result))
        run_id = validate_result_for_adjudication(result)
        record = {
            "schema_version": "jev-adjudication-v1",
            "run_id": run_id,
            "blind_label": args.label,
            "verifier_result_sha256": result_hash,
            "cli_displays_jev_decision": False,
        }
        write_new_json(output, record)
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"blind label recorded at {output}; Jev decision intentionally not displayed")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evidence-gated Jev verifier prototype")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="check local compatibility without an API call")
    doctor.add_argument(
        "--contract",
        choices=("orchestrate", "fact-check", "citation-check", "route"),
        default="orchestrate",
    )
    doctor.add_argument("--allow-network", action="store_true", help="report explicit network intent only")
    doctor.set_defaults(func=run_doctor)

    verify = subparsers.add_parser("verify", help="verify an evidence manifest")
    verify.add_argument(
        "--contract", required=True, choices=("orchestrate", "fact-check", "citation-check")
    )
    verify.add_argument("--state", required=True, help="path to evidence manifest JSON")
    verify.add_argument("--out", required=True, help="new local result JSON path")
    verify.add_argument("--mode", choices=("shadow", "advisory"), default="shadow")
    backend = verify.add_mutually_exclusive_group()
    backend.add_argument("--mock-response", help="offline API-response fixture; always simulation")
    backend.add_argument("--allow-network", action="store_true", help="allow one bounded live API operation")
    verify.set_defaults(func=run_verify)

    # Routing is a separate subcommand, not a --contract on `verify`: the two
    # carry different state, different results, and different claims, and a
    # route state must never be readable as a completion manifest.
    route = subparsers.add_parser(
        "route", help="experimental: profile the task with Jev and propose an execution plan"
    )
    route.add_argument("--state", required=True, help="path to route state JSON")
    route.add_argument("--out", required=True, help="new local route result JSON path")
    route.add_argument("--mode", choices=("shadow", "advisory"), default="shadow")
    route_backend = route.add_mutually_exclusive_group()
    route_backend.add_argument(
        "--mock-response", help="offline API-response fixture; always simulation, never a route"
    )
    route_backend.add_argument(
        "--allow-network", action="store_true", help="allow one bounded live API operation"
    )
    route.set_defaults(func=run_route)

    adjudicate = subparsers.add_parser(
        "adjudicate", help="record a blind lead label without displaying the Jev decision"
    )
    adjudicate.add_argument("--result", required=True, help="verifier result JSON path")
    adjudicate.add_argument("--label", required=True, choices=("PASS", "REWORK", "ESCALATE"))
    adjudicate.add_argument("--out", required=True, help="new local adjudication JSON path")
    adjudicate.set_defaults(func=run_adjudicate)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
