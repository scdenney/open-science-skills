from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "verify.py"
SPEC = importlib.util.spec_from_file_location("jev_research_verify", MODULE_PATH)
assert SPEC and SPEC.loader
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)


class ResearchRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.fact_artifact = self.root / "source-conversion.md"
        self.fact_artifact.write_text(
            "The survey estimate was positive in the sampled municipalities, with uncertainty.\n",
            encoding="utf-8",
        )
        self.citation_artifact = self.root / "crossref-record.json"
        self.citation_artifact.write_text(
            '{"title":"Local Participation","author":"Rivera","year":2024}\n',
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def artifact(path: Path, excerpt: str) -> dict:
        return {
            "path": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "excerpt": excerpt,
        }

    def fact_state(self, *, kind="fulltext", sufficiency="sufficient", artifacts=True) -> dict:
        return {
            "schema_version": verify.FACT_STATE_SCHEMA_VERSION,
            "contract": "fact-check",
            "run_id": "fact-synthetic-001",
            "claim": {
                "text": "Participation increased in the sampled municipalities.",
                "kind": "empirical",
                "strength_applicable": True,
                "direction_magnitude_applicable": True,
                "omission_applicable": True,
            },
            "source": {
                "identity": "Rivera (2024), Local Participation",
                "kind": kind,
                "knowledge_base_status": "available",
            },
            "evidence": {
                "readiness": "ready",
                "citation_integrity": "valid",
                "sufficiency": sufficiency,
                "artifacts": [
                    self.artifact(self.fact_artifact, "estimate was positive in the sampled municipalities")
                ] if artifacts else [],
            },
            "blind_baseline": {"label": "PARTIALLY SUPPORTED"},
        }

    def citation_state(self, *, identity="ambiguous", artifacts=True, status="success") -> dict:
        return {
            "schema_version": verify.CITATION_STATE_SCHEMA_VERSION,
            "contract": "citation-check",
            "run_id": "citation-synthetic-001",
            "bibliographic_entry": {
                "rendered": "Rivera, A. (2023). Local Participation. Working paper.",
                "title": "Local Participation",
                "authors": "A. Rivera",
                "year": "2023",
                "doi": "10.5555/preprint.1",
                "version": "working paper",
            },
            "retrieved_record": {
                "title": "Local Participation",
                "authors": "Ana Rivera",
                "year": "2024",
                "doi": "10.5555/article.9",
                "version": "published article",
                "deterministic_identity": identity,
                "retrieval": {
                    "provider": "Crossref synthetic fixture",
                    "url": "https://api.example.invalid/works/fixture",
                    "retrieved_at": "2026-09-20T12:00:00Z",
                    "status": status,
                },
                "artifacts": [
                    self.artifact(self.citation_artifact, '"title":"Local Participation"')
                ] if artifacts else [],
            },
            "blind_baseline": {"label": "AMBIGUOUS"},
        }

    def response(self, contract_name: str, probability: float = 0.9) -> dict:
        contract = verify.load_contract(contract_name)
        value = {
            "model": verify.DEFAULT_MODEL,
            "answers": {
                question_id: {"type": "noul", "noul": probability}
                for question_id in contract["questions"]
            },
            "usage": {"input_tokens": 80, "output_tokens": 10},
        }
        if contract_name == "fact-check":
            value["answers"]["source_contradicts_claim"]["noul"] = 0.1
        return value

    def write_json(self, name: str, value: dict) -> Path:
        path = self.root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def invoke(self, argv: list[str]) -> tuple[int, str, str]:
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = verify.main(argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_fact_api_excludes_blind_label_and_file_paths(self):
        path = self.write_json("fact.json", self.fact_state())
        state = verify.validate_fact_state(
            verify.read_json(path)[0], path, verify.load_contract("fact-check")
        )
        payload = verify.research_api_state(state)
        serialized = json.dumps(payload)
        self.assertNotIn("blind_baseline", serialized)
        self.assertNotIn("PARTIALLY SUPPORTED", serialized)
        self.assertNotIn("source-conversion.md", serialized)
        self.assertIn("estimate was positive", serialized)

    def test_each_fact_preflight_gate_prevents_backend(self):
        cases = {
            "readiness": ("evidence", "readiness", "not_ready"),
            "citation": ("evidence", "citation_integrity", "invalid"),
            "knowledge_base": ("source", "knowledge_base_status", "missing"),
            "sufficiency": ("evidence", "sufficiency", "insufficient"),
        }
        for name, (section, field, replacement) in cases.items():
            with self.subTest(name=name):
                state = self.fact_state()
                state[section][field] = replacement
                state_path = self.write_json(f"{name}.json", state)
                out = self.root / f"{name}-result.json"
                with mock.patch.object(verify, "post_live") as post:
                    code, _, _ = self.invoke([
                        "verify", "--contract", "fact-check", "--state", str(state_path),
                        "--out", str(out), "--allow-network",
                    ])
                self.assertEqual(code, 0)
                post.assert_not_called()
                value = json.loads(out.read_text())
                self.assertEqual(value["verification_status"], "deterministic")
                self.assertIn(value["assessment"]["proposed_outcome"], {"NOT_CHECKED", "INVALID_CITATION"})

    def test_summary_insufficiency_is_not_unsupported(self):
        state = self.fact_state(kind="summary", sufficiency="insufficient", artifacts=False)
        state_path = self.write_json("summary.json", state)
        out = self.root / "summary-result.json"
        code, _, _ = self.invoke([
            "verify", "--contract", "fact-check", "--state", str(state_path),
            "--out", str(out), "--mock-response", str(self.root / "missing-mock.json"),
        ])
        self.assertEqual(code, 0)
        value = json.loads(out.read_text())
        self.assertEqual(value["assessment"]["proposed_outcome"], "NOT_CHECKED")
        self.assertNotIn("UNSUPPORTED", out.read_text())

    def test_summary_can_reach_model_when_declared_sufficient(self):
        state_path = self.write_json("summary-ready.json", self.fact_state(kind="summary"))
        mock_path = self.write_json("fact-response.json", self.response("fact-check"))
        out = self.root / "summary-ready-result.json"
        code, _, _ = self.invoke([
            "verify", "--contract", "fact-check", "--state", str(state_path),
            "--out", str(out), "--mock-response", str(mock_path),
        ])
        self.assertEqual(code, 0)
        value = json.loads(out.read_text())
        self.assertEqual(value["verification_status"], "simulation")
        self.assertEqual(value["jev"]["simulated_outcome"], "SUPPORTED")

    def test_theory_summary_with_nonapplicable_empirical_dimensions_reaches_advisory(self):
        state = self.fact_state(kind="summary")
        state["claim"].update({
            "text": "The source advances participation as a mechanism of local accountability.",
            "kind": "theoretical",
            "strength_applicable": False,
            "direction_magnitude_applicable": False,
            "omission_applicable": False,
        })
        state_path = self.write_json("theory-summary.json", state)
        mock_path = self.write_json("theory-response.json", self.response("fact-check"))
        out = self.root / "theory-summary-result.json"
        code, stdout, _ = self.invoke([
            "verify", "--contract", "fact-check", "--state", str(state_path),
            "--out", str(out), "--mode", "advisory", "--mock-response", str(mock_path),
        ])
        self.assertEqual(code, 0)
        value = json.loads(out.read_text())
        self.assertEqual(value["verification_status"], "simulation")
        self.assertEqual(value["assessment"]["proposed_outcome"], "NOT_CHECKED")
        self.assertEqual(value["jev"]["simulated_outcome"], "SUPPORTED")
        signal_ids = {item["question_id"] for item in value["jev"]["simulated_signals"]}
        self.assertEqual(
            signal_ids,
            {"source_supports_claim", "source_contradicts_claim", "scope_matches"},
        )
        self.assertIn("advisory research outcome: NOT_CHECKED", stdout)

    def test_low_support_does_not_mean_contradicted(self):
        contract = verify.load_contract("fact-check")
        state_path = self.write_json("fact-low.json", self.fact_state())
        state = verify.validate_fact_state(verify.read_json(state_path)[0], state_path, contract)
        probabilities = {question_id: 0.1 for question_id in contract["questions"]}
        probabilities["source_contradicts_claim"] = 0.1
        outcome, _, _ = verify.research_model_outcome(state, probabilities, contract)
        self.assertEqual(outcome, "REVIEW_REQUIRED")

    def test_low_scope_with_otherwise_positive_support_requires_review(self):
        contract = verify.load_contract("fact-check")
        state_path = self.write_json("fact-low-scope.json", self.fact_state())
        state = verify.validate_fact_state(verify.read_json(state_path)[0], state_path, contract)
        probabilities = {question_id: 0.9 for question_id in contract["questions"]}
        probabilities["source_contradicts_claim"] = 0.1
        probabilities["scope_matches"] = 0.1
        outcome, reasons, _ = verify.research_model_outcome(state, probabilities, contract)
        self.assertEqual(outcome, "REVIEW_REQUIRED")
        self.assertEqual(reasons, ["mixed_or_ambiguous_fact_signals"])

    def test_explicit_contradiction_signal_is_required(self):
        contract = verify.load_contract("fact-check")
        state_path = self.write_json("fact-contradiction.json", self.fact_state())
        state = verify.validate_fact_state(verify.read_json(state_path)[0], state_path, contract)
        probabilities = {question_id: 0.1 for question_id in contract["questions"]}
        probabilities["source_contradicts_claim"] = 0.9
        outcome, reasons, _ = verify.research_model_outcome(state, probabilities, contract)
        self.assertEqual(outcome, "CONTRADICTED")
        self.assertEqual(reasons, ["explicit_contradiction_signal"])

    def test_conflicting_support_and_contradiction_require_review(self):
        contract = verify.load_contract("fact-check")
        state_path = self.write_json("fact-conflict.json", self.fact_state())
        state = verify.validate_fact_state(verify.read_json(state_path)[0], state_path, contract)
        probabilities = {question_id: 0.9 for question_id in contract["questions"]}
        outcome, reasons, _ = verify.research_model_outcome(state, probabilities, contract)
        self.assertEqual(outcome, "REVIEW_REQUIRED")
        self.assertEqual(reasons, ["conflicting_support_and_contradiction_signals"])

    def test_different_work_overrides_positive_mock(self):
        state_path = self.write_json("wrong-doi.json", self.citation_state(identity="different_work"))
        mock_path = self.write_json("citation-response.json", self.response("citation-check"))
        out = self.root / "wrong-doi-result.json"
        code, _, _ = self.invoke([
            "verify", "--contract", "citation-check", "--state", str(state_path),
            "--out", str(out), "--mock-response", str(mock_path),
        ])
        self.assertEqual(code, 0)
        value = json.loads(out.read_text())
        self.assertEqual(value["assessment"]["proposed_outcome"], "DIFFERENT_WORK")
        self.assertEqual(value["verification_status"], "deterministic")
        self.assertIsNone(value["jev"]["simulated_outcome"])

    def test_different_doi_is_ambiguous_without_different_work_evidence(self):
        state_path = self.write_json("versions.json", self.citation_state(identity="ambiguous"))
        mock_path = self.write_json("versions-response.json", self.response("citation-check"))
        out = self.root / "versions-result.json"
        code, _, _ = self.invoke([
            "verify", "--contract", "citation-check", "--state", str(state_path),
            "--out", str(out), "--mock-response", str(mock_path),
        ])
        self.assertEqual(code, 0)
        value = json.loads(out.read_text())
        self.assertEqual(value["assessment"]["proposed_outcome"], "NOT_CHECKED")
        self.assertEqual(value["jev"]["simulated_outcome"], "VERIFIED")
        self.assertNotIn("DIFFERENT_WORK", value["reason_codes"])

    def test_missing_retrieved_evidence_cannot_be_verified(self):
        state_path = self.write_json("no-record.json", self.citation_state(artifacts=False))
        out = self.root / "no-record-result.json"
        code, _, _ = self.invoke([
            "verify", "--contract", "citation-check", "--state", str(state_path),
            "--out", str(out), "--allow-network",
        ])
        self.assertEqual(code, 0)
        value = json.loads(out.read_text())
        self.assertEqual(value["assessment"]["proposed_outcome"], "NOT_CHECKED")
        self.assertIn("retrieved_evidence_missing", value["reason_codes"])

    def test_unsuccessful_retrieval_prevents_live_call_despite_artifact(self):
        for status in ("not_found", "error"):
            with self.subTest(status=status):
                state_path = self.write_json(
                    f"retrieval-{status}.json",
                    self.citation_state(identity="ambiguous", artifacts=True, status=status),
                )
                out = self.root / f"retrieval-{status}-result.json"
                with mock.patch.object(verify, "post_live") as post:
                    code, _, _ = self.invoke([
                        "verify", "--contract", "citation-check", "--state", str(state_path),
                        "--out", str(out), "--allow-network",
                    ])
                self.assertEqual(code, 0)
                post.assert_not_called()
                value = json.loads(out.read_text())
                self.assertEqual(value["verification_status"], "deterministic")
                self.assertEqual(value["assessment"]["proposed_outcome"], "NOT_CHECKED")
                self.assertIn("retrieval_not_successful", value["reason_codes"])

    def test_declared_match_without_core_metadata_is_not_checked(self):
        state = self.citation_state(identity="match")
        state["retrieved_record"]["authors"] = None
        state_path = self.write_json("missing-authors.json", state)
        out = self.root / "missing-authors-result.json"
        code, _, _ = self.invoke([
            "verify", "--contract", "citation-check", "--state", str(state_path),
            "--out", str(out), "--allow-network",
        ])
        self.assertEqual(code, 0)
        value = json.loads(out.read_text())
        self.assertEqual(value["assessment"]["proposed_outcome"], "NOT_CHECKED")
        self.assertIn("identity_comparison_fields_missing", value["reason_codes"])

    def test_fabricated_excerpt_and_hash_are_rejected(self):
        for name, field, replacement in (
            ("quote", "excerpt", "text not present in the retrieved file"),
            ("hash", "sha256", "0" * 64),
        ):
            with self.subTest(name=name):
                state = self.fact_state()
                state["evidence"]["artifacts"][0][field] = replacement
                state_path = self.write_json(f"bad-{name}.json", state)
                out = self.root / f"bad-{name}-result.json"
                code, _, _ = self.invoke([
                    "verify", "--contract", "fact-check", "--state", str(state_path),
                    "--out", str(out), "--allow-network",
                ])
                self.assertEqual(code, 2)
                self.assertEqual(
                    json.loads(out.read_text())["reason_codes"],
                    ["schema_or_evidence_validation_failed"],
                )

    def test_network_request_requires_optin_and_key(self):
        state_path = self.write_json("ready.json", self.fact_state())
        no_opt_out = self.root / "no-opt.json"
        code, _, _ = self.invoke([
            "verify", "--contract", "fact-check", "--state", str(state_path), "--out", str(no_opt_out)
        ])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(no_opt_out.read_text())["verification_status"], "not_run")

        key_out = self.root / "missing-key.json"
        with mock.patch.dict(verify.os.environ, {}, clear=True), mock.patch.object(
            verify.sys, "platform", "linux"
        ):
            code, _, stderr = self.invoke([
                "verify", "--contract", "fact-check", "--state", str(state_path),
                "--out", str(key_out), "--allow-network",
            ])
        self.assertEqual(code, 2)
        self.assertIn("missing or invalid", stderr)
        self.assertFalse(json.loads(key_out.read_text())["live_verified"])

    def test_mock_is_clearly_nonlive_and_does_not_certify(self):
        state_path = self.write_json("mock-state.json", self.fact_state())
        mock_path = self.write_json("mock-response.json", self.response("fact-check"))
        out = self.root / "mock-result.json"
        code, stdout, _ = self.invoke([
            "verify", "--contract", "fact-check", "--state", str(state_path),
            "--out", str(out), "--mock-response", str(mock_path),
        ])
        self.assertEqual(code, 0)
        value = json.loads(out.read_text())
        self.assertEqual(value["verification_status"], "simulation")
        self.assertFalse(value["live_verified"])
        self.assertFalse(value["content_certified"])
        self.assertEqual(value["assessment"]["proposed_outcome"], "NOT_CHECKED")
        self.assertNotIn("SUPPORTED", stdout)
        serialized = out.read_text()
        self.assertNotIn("PARTIALLY SUPPORTED", serialized)
        self.assertNotIn("source-conversion.md", serialized)
        self.assertNotIn("estimate was positive", serialized)

    def test_doctor_supports_research_contracts_without_network(self):
        for contract_name in ("fact-check", "citation-check"):
            with self.subTest(contract=contract_name), mock.patch.object(verify, "post_live") as post:
                code, stdout, _ = self.invoke(["doctor", "--contract", contract_name])
                self.assertEqual(code, 0)
                self.assertTrue(json.loads(stdout)["contract_valid"])
                post.assert_not_called()

    def test_orchestration_contract_still_loads(self):
        contract = verify.load_contract("orchestrate")
        self.assertEqual(contract["contract"], "orchestrate")
        self.assertIn("work_complete", contract["questions"])

    def test_research_contract_rejects_missing_essential_question(self):
        value = json.loads((verify.CONTRACT_DIR / "fact-check.json").read_text())
        del value["questions"]["source_contradicts_claim"]
        contract_dir = self.root / "contracts"
        contract_dir.mkdir()
        (contract_dir / "fact-check.json").write_text(json.dumps(value), encoding="utf-8")
        with mock.patch.object(verify, "CONTRACT_DIR", contract_dir):
            with self.assertRaisesRegex(verify.ValidationError, "question ids"):
                verify.load_contract("fact-check")


if __name__ == "__main__":
    unittest.main()
