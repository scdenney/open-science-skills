from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "verify.py"
SPEC = importlib.util.spec_from_file_location("jev_verify", MODULE_PATH)
assert SPEC and SPEC.loader
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)
CONTRACT = verify.load_contract("orchestrate")


def response(probability: float = 0.9) -> dict:
    return {
        "model": verify.DEFAULT_MODEL,
        "answers": {
            key: {"type": "noul", "noul": probability} for key in CONTRACT["questions"]
        },
        "usage": {"input_tokens": 50, "output_tokens": 8},
    }


class FakeResponse:
    def __init__(self, value: dict, url: str = verify.ENDPOINT, status: int = 200):
        self.body = json.dumps(value).encode("utf-8")
        self.url = url
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def geturl(self):
        return self.url

    def read(self, limit: int):
        return self.body[:limit]


class SequenceOpener:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.requests = []

    def open(self, request, timeout):
        self.requests.append((request, timeout))
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.artifact = self.root / "artifact.txt"
        self.artifact.write_text("verified local artifact\n", encoding="utf-8")
        self.artifact_hash = hashlib.sha256(self.artifact.read_bytes()).hexdigest()

    def tearDown(self):
        self.temp.cleanup()

    def test_api_key_prefers_environment(self):
        with mock.patch.dict("os.environ", {"TYPESAFE_API_KEY": "env-secret"}, clear=True):
            with mock.patch.object(verify.sys, "platform", "darwin"), mock.patch.object(
                verify.subprocess, "run"
            ) as run:
                self.assertEqual(verify.get_api_key(), "env-secret")
                run.assert_not_called()

    def test_api_key_uses_macos_keychain_fallback(self):
        completed = mock.Mock(returncode=0, stdout="keychain-secret\n")
        with mock.patch.dict("os.environ", {}, clear=True):
            with mock.patch.object(verify.sys, "platform", "darwin"), mock.patch.object(
                verify.subprocess, "run", return_value=completed
            ) as run:
                self.assertEqual(verify.get_api_key(), "keychain-secret")
        self.assertEqual(run.call_args.args[0][:5], [
            "/usr/bin/security", "find-generic-password", "-s", verify.KEYCHAIN_SERVICE, "-a"
        ])
        self.assertEqual(run.call_args.kwargs["timeout"], 5)
        self.assertTrue(run.call_args.kwargs["capture_output"])

    def test_api_key_uses_linux_secret_service_fallback(self):
        completed = mock.Mock(returncode=0, stdout="secret-service-key\n")
        with mock.patch.dict("os.environ", {}, clear=True):
            with mock.patch.object(verify.sys, "platform", "linux"), mock.patch.object(
                verify.subprocess, "run", return_value=completed
            ) as run:
                self.assertEqual(verify.get_api_key(), "secret-service-key")
        self.assertEqual(run.call_args.args[0], [
            "/usr/bin/secret-tool", "lookup", "service", verify.SECRET_TOOL_SERVICE,
            "account", verify.getpass.getuser(),
        ])

    def test_api_key_ignores_unsupported_platform(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with mock.patch.object(verify.sys, "platform", "win32"), mock.patch.object(
                verify.subprocess, "run"
            ) as run:
                self.assertEqual(verify.get_api_key(), "")
                run.assert_not_called()

    def test_api_key_silently_handles_missing_keychain_item(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with mock.patch.object(verify.sys, "platform", "darwin"), mock.patch.object(
                verify.subprocess, "run", return_value=mock.Mock(returncode=44, stdout="")
            ):
                self.assertEqual(verify.get_api_key(), "")

    def manifest(self, result="pass"):
        return {
            "schema_version": verify.MANIFEST_SCHEMA_VERSION,
            "contract": "orchestrate",
            "run_id": "test-run",
            "task": {
                "objective": "Build and verify the requested runtime.",
                "acceptance_criteria": ["Targeted checks pass."],
                "scope_constraints": ["Only edit the authorized runtime directory."],
            },
            "worker_claim": "The runtime is implemented and targeted checks pass.",
            "lead_decision": {"label": "PASS"},
            "evidence": [
                {
                    "check_id": check_id,
                    "result": result,
                    "observation": f"Lead inspected evidence for {check_id}.",
                    "artifacts": []
                    if result == "not_checked"
                    else [{
                        "path": "artifact.txt",
                        "sha256": self.artifact_hash,
                        "excerpt": "verified local artifact",
                    }],
                }
                for check_id in CONTRACT["required_checks"]
            ],
        }

    def write_json(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def invoke(self, argv):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = verify.main(argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_manifest_verifies_files_and_excludes_blind_label_from_api_state(self):
        path = self.write_json("manifest.json", self.manifest())
        raw, _ = verify.read_json(path)
        manifest = verify.validate_manifest(raw, path, CONTRACT)
        state = verify.api_state(manifest)
        self.assertNotIn("lead_decision", state)
        self.assertEqual(state["task"]["objective"], "Build and verify the requested runtime.")
        self.assertEqual(state["evidence"][0]["artifacts"][0]["excerpt"], "verified local artifact")
        self.assertEqual(manifest["lead_decision"]["label"], "PASS")
        self.assertRegex(manifest["lead_decision"]["sha256"], r"^[0-9a-f]{64}$")
        self.assertNotIn("path", state["evidence"][0]["artifacts"][0])

    def test_contract_file_drives_questions_thresholds_and_hash(self):
        value = json.loads((verify.CONTRACT_DIR / "orchestrate.json").read_text())
        value["questions"] = {
            "custom_question": {
                "type": "noul",
                "instructions": "Does this test contract loading?",
                "criteria": {"true": "It does.", "false": "It does not."},
            }
        }
        value["thresholds"]["pass_min"] = 0.91
        contract_dir = self.root / "contracts"
        contract_dir.mkdir()
        (contract_dir / "orchestrate.json").write_text(json.dumps(value))
        with mock.patch.object(verify, "CONTRACT_DIR", contract_dir):
            loaded = verify.load_contract("orchestrate")
        self.assertEqual(list(loaded["questions"]), ["custom_question"])
        self.assertEqual(loaded["thresholds"]["pass_min"], 0.91)
        self.assertRegex(loaded["questions_sha256"], r"^[0-9a-f]{64}$")

    def test_missing_check_is_rejected(self):
        value = self.manifest()
        value["evidence"].pop()
        path = self.write_json("manifest.json", value)
        with self.assertRaises(verify.ValidationError):
            verify.validate_manifest(verify.read_json(path)[0], path, CONTRACT)

    def test_hash_mismatch_is_rejected(self):
        value = self.manifest()
        value["evidence"][0]["artifacts"][0]["sha256"] = "0" * 64
        path = self.write_json("manifest.json", value)
        with self.assertRaisesRegex(verify.ValidationError, "hash mismatch"):
            verify.validate_manifest(verify.read_json(path)[0], path, CONTRACT)

    def test_not_checked_cannot_cite_artifact(self):
        value = self.manifest("not_checked")
        value["evidence"][0]["artifacts"] = [
            {"path": "artifact.txt", "sha256": self.artifact_hash, "excerpt": "verified"}
        ]
        path = self.write_json("manifest.json", value)
        with self.assertRaises(verify.ValidationError):
            verify.validate_manifest(verify.read_json(path)[0], path, CONTRACT)

    def test_strict_json_rejects_nan_and_duplicate_keys(self):
        nan = self.root / "nan.json"
        nan.write_text('{"value": NaN}', encoding="utf-8")
        duplicate = self.root / "duplicate.json"
        duplicate.write_text('{"value": 1, "value": 2}', encoding="utf-8")
        for path in (nan, duplicate):
            with self.subTest(path=path.name), self.assertRaises(verify.ValidationError):
                verify.read_json(path)

    def test_strict_json_rejects_oversized_integer(self):
        path = self.root / "huge-integer.json"
        path.write_text('{"value":' + ("9" * 5_000) + "}", encoding="utf-8")
        with self.assertRaises(verify.ValidationError):
            verify.read_json(path)

    def test_lone_surrogate_excerpt_writes_escalation(self):
        value = self.manifest()
        value["evidence"][0]["artifacts"][0]["excerpt"] = "\ud800"
        manifest = self.write_json("surrogate.json", value)
        out = self.root / "surrogate-result.json"
        code, _, _ = self.invoke(
            ["verify", "--contract", "orchestrate", "--state", str(manifest), "--out", str(out)]
        )
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out.read_text())["decision"], "ESCALATE")

    def test_response_rejects_missing_out_of_range_and_unknown_type(self):
        cases = []
        missing = response()
        del missing["answers"][next(iter(CONTRACT["questions"]))]
        cases.append(missing)
        out_of_range = response()
        out_of_range["answers"][next(iter(CONTRACT["questions"]))]["noul"] = 1.1
        cases.append(out_of_range)
        wrong_type = response()
        wrong_type["answers"][next(iter(CONTRACT["questions"]))] = {
            "type": "choice",
            "noul": 0.9,
        }
        cases.append(wrong_type)
        for value in cases:
            with self.subTest(value=value), self.assertRaises(verify.ValidationError):
                verify.validate_response(value, CONTRACT)

    def test_huge_integer_probability_writes_escalation(self):
        manifest = self.write_json("manifest.json", self.manifest())
        value = response()
        value["answers"][next(iter(CONTRACT["questions"]))]["noul"] = 10**400
        mock_response = self.write_json("huge-response.json", value)
        out = self.root / "huge-result.json"
        code, _, _ = self.invoke(
            [
                "verify", "--contract", "orchestrate", "--state", str(manifest),
                "--mock-response", str(mock_response), "--out", str(out),
            ]
        )
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out.read_text())["decision"], "ESCALATE")

    def test_decision_thresholds(self):
        ids = list(CONTRACT["questions"])
        self.assertEqual(verify.model_decision({key: 0.8 for key in ids}, CONTRACT["thresholds"])[0], "PASS")
        self.assertEqual(verify.model_decision({key: 0.79 for key in ids}, CONTRACT["thresholds"])[0], "ESCALATE")
        values = {key: 0.9 for key in ids}
        values[ids[0]] = 0.2
        self.assertEqual(verify.model_decision(values, CONTRACT["thresholds"])[0], "REWORK")

    def test_mock_is_simulation_and_shadow_stdout_hides_decisions(self):
        manifest = self.write_json("manifest.json", self.manifest())
        mock = self.write_json("mock.json", response())
        out = self.root / "result.json"
        code, stdout, stderr = self.invoke(
            [
                "verify",
                "--contract",
                "orchestrate",
                "--state",
                str(manifest),
                "--out",
                str(out),
                "--mock-response",
                str(mock),
            ]
        )
        self.assertEqual((code, stderr), (0, ""))
        self.assertNotIn("PASS", stdout)
        self.assertNotIn("REWORK", stdout)
        value = json.loads(out.read_text())
        self.assertEqual(value["verification_status"], "simulation")
        self.assertFalse(value["live_verified"])
        self.assertEqual(value["decision"], "ESCALATE")
        self.assertEqual(value["jev"]["simulated_decision"], "PASS")
        serialized = out.read_text()
        self.assertNotIn("Lead inspected", serialized)
        self.assertNotIn("artifact.txt", serialized)

    def test_deterministic_failure_trumps_mock_pass(self):
        manifest = self.write_json("manifest.json", self.manifest("fail"))
        mock = self.write_json("mock.json", response())
        out = self.root / "result.json"
        code, _, _ = self.invoke(
            [
                "verify",
                "--contract",
                "orchestrate",
                "--state",
                str(manifest),
                "--out",
                str(out),
                "--mock-response",
                str(mock),
            ]
        )
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out.read_text())["jev"]["simulated_decision"], "REWORK")

    def test_missing_input_writes_sanitized_escalation(self):
        out = self.root / "result.json"
        code, stdout, _ = self.invoke(
            [
                "verify",
                "--contract",
                "orchestrate",
                "--state",
                str(self.root / "missing.json"),
                "--out",
                str(out),
            ]
        )
        self.assertEqual(code, 2)
        self.assertNotIn("PASS", stdout)
        value = json.loads(out.read_text())
        self.assertEqual(value["decision"], "ESCALATE")
        self.assertEqual(value["reason_codes"], ["schema_or_evidence_validation_failed"])

    def test_unhashable_enum_values_write_escalation_not_traceback(self):
        for field, replacement in (("result", []), ("lead_decision", {"label": {}})):
            value = self.manifest()
            if field == "result":
                value["evidence"][0]["result"] = replacement
            else:
                value[field] = replacement
            manifest = self.write_json(f"bad-{field}.json", value)
            out = self.root / f"bad-{field}-result.json"
            code, _, _ = self.invoke(
                ["verify", "--contract", "orchestrate", "--state", str(manifest), "--out", str(out)]
            )
            self.assertEqual(code, 2)
            self.assertEqual(json.loads(out.read_text())["decision"], "ESCALATE")

    def test_output_collision_refuses_overwrite(self):
        manifest = self.write_json("manifest.json", self.manifest())
        out = self.root / "result.json"
        out.write_text("keep me", encoding="utf-8")
        code, _, stderr = self.invoke(
            [
                "verify",
                "--contract",
                "orchestrate",
                "--state",
                str(manifest),
                "--out",
                str(out),
            ]
        )
        self.assertEqual(code, 2)
        self.assertIn("refusing overwrite", stderr)
        self.assertEqual(out.read_text(), "keep me")

    def test_no_backend_escalates_without_network(self):
        manifest = self.write_json("manifest.json", self.manifest())
        out = self.root / "result.json"
        code, _, _ = self.invoke(
            [
                "verify",
                "--contract",
                "orchestrate",
                "--state",
                str(manifest),
                "--out",
                str(out),
            ]
        )
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out.read_text())["verification_status"], "not_run")

    def test_adjudicate_records_only_blind_label_and_hash(self):
        result_path = self.write_json(
            "result-source.json",
            {"schema_version": verify.RESULT_SCHEMA_VERSION, "mode": "shadow", "run_id": "r1", "decision": "PASS"},
        )
        out = self.root / "adjudication.json"
        code, stdout, _ = self.invoke(
            ["adjudicate", "--result", str(result_path), "--label", "REWORK", "--out", str(out)]
        )
        self.assertEqual(code, 0)
        self.assertNotIn("PASS", stdout)
        value = json.loads(out.read_text())
        self.assertEqual(value["blind_label"], "REWORK")
        self.assertNotIn("decision", value)
        self.assertFalse(value["cli_displays_jev_decision"])

    def test_adjudicate_rejects_unhashable_mode_cleanly(self):
        with self.assertRaises(verify.ValidationError):
            verify.validate_result_for_adjudication(
                {"schema_version": verify.RESULT_SCHEMA_VERSION, "mode": [], "run_id": "r1"}
            )

    def test_live_post_uses_fixed_endpoint_auth_and_timeout(self):
        opener = SequenceOpener([FakeResponse(response())])
        value, latency = verify.post_live(
            {"state": {}, "model": verify.DEFAULT_MODEL, "questions": CONTRACT["questions"]},
            "top-secret",
            opener=opener,
        )
        request, timeout = opener.requests[0]
        self.assertEqual(request.full_url, verify.ENDPOINT)
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Authorization"), "Bearer top-secret")
        self.assertEqual(timeout, verify.TIMEOUT_SECONDS)
        self.assertGreaterEqual(latency, 0)
        self.assertEqual(value["model"], verify.DEFAULT_MODEL)

    def test_rate_limit_is_retried_with_bound(self):
        error = urllib.error.HTTPError(verify.ENDPOINT, 429, "rate", {}, None)
        opener = SequenceOpener([error, FakeResponse(response())])
        sleeps = []
        verify.post_live({}, "secret", opener=opener, sleep=sleeps.append)
        self.assertEqual(len(opener.requests), 2)
        self.assertEqual(sleeps, [0.25])

    def test_redirect_is_refused_without_retry_or_body_disclosure(self):
        error = urllib.error.HTTPError(verify.ENDPOINT, 302, "redirect", {"Location": "https://example.com"}, None)
        opener = SequenceOpener([error])
        with self.assertRaisesRegex(verify.NetworkFailure, "redirect refused"):
            verify.post_live({}, "secret", opener=opener, sleep=lambda _delay: None)
        self.assertEqual(len(opener.requests), 1)

    def test_transport_failure_retries_only_three_times(self):
        opener = SequenceOpener(
            [urllib.error.URLError("sensitive details") for _ in range(verify.MAX_ATTEMPTS)]
        )
        with self.assertRaisesRegex(verify.NetworkFailure, "bounded retries") as raised:
            verify.post_live({}, "secret", opener=opener, sleep=lambda _delay: None)
        self.assertNotIn("sensitive details", str(raised.exception))
        self.assertNotIn("secret", str(raised.exception))
        self.assertEqual(len(opener.requests), verify.MAX_ATTEMPTS)

    def test_missing_key_fails_before_open(self):
        opener = SequenceOpener([])
        with self.assertRaisesRegex(verify.NetworkFailure, "missing or invalid"):
            verify.post_live({}, "", opener=opener)
        self.assertEqual(opener.requests, [])


if __name__ == "__main__":
    unittest.main()
