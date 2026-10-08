from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "verify.py"
SPEC = importlib.util.spec_from_file_location("jev_route_verify", MODULE_PATH)
assert SPEC and SPEC.loader
verify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify)
CONTRACT = verify.load_contract("route")
SAMPLES = MODULE_PATH.parent / "samples"
THRESHOLDS = CONTRACT["thresholds"]

ALL_AVAILABLE = {key: True for key in verify.ROUTE_EXECUTORS}
QUIET = {key: 0.05 for key in verify.ROUTE_QUESTION_IDS}


def response(**probabilities) -> dict:
    values = {**QUIET, **probabilities}
    return {
        "model": verify.DEFAULT_MODEL,
        "answers": {key: {"type": "noul", "noul": value} for key, value in values.items()},
        "usage": {"input_tokens": 40, "output_tokens": 6},
    }


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def state(self, harness="claude", lead_model="claude-opus-5-5", lead_effort="medium",
              available=None, **constraints):
        return {
            "schema_version": verify.ROUTE_STATE_SCHEMA_VERSION,
            "contract": "route",
            "run_id": "route-test",
            "task": {
                "objective": "Rename one helper across the suite and update its call sites.",
                "acceptance_criteria": ["Every call site uses the new name."],
                "scope_constraints": ["Do not change behaviour."],
            },
            "harness": harness,
            "lead": {"model": lead_model, "effort": lead_effort},
            "available": {**ALL_AVAILABLE, **(available or {})},
            "constraints": {"model": None, "effort": None, "topology": None, **constraints},
            "blind_baseline": {"lead_choice": "fast-worker does the rename"},
        }

    def plan(self, state=None, **probabilities):
        validated = verify.validate_route_state(state or self.state(), CONTRACT)
        values = {**QUIET, **probabilities}
        return verify.route_plan(validated, values, THRESHOLDS)

    def items(self, detail):
        return {item["executor"]: item for item in detail["items"]}

    def write_json(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def invoke(self, argv):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = verify.main(argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def run_route(self, state, name="result.json", extra=()):
        state_path = self.write_json("state.json", state)
        out = self.root / name
        code, stdout, stderr = self.invoke(
            ["route", "--state", str(state_path), "--out", str(out), *extra]
        )
        return code, json.loads(out.read_text()), stdout, stderr

    def run_live(self, state, answer, name="live.json"):
        state_path = self.write_json("state.json", state)
        out = self.root / name
        seen = []

        def fake_post(payload, api_key):
            seen.append(payload)
            return answer, 7

        with mock.patch.object(verify, "post_live", fake_post), mock.patch.object(
            verify, "get_api_key", return_value="test-key"
        ):
            code, stdout, stderr = self.invoke(
                ["route", "--state", str(state_path), "--out", str(out), "--allow-network"]
            )
        return code, json.loads(out.read_text()), seen, stdout, stderr

    # --- what is sent ---------------------------------------------------------

    def test_one_request_carries_the_task_and_no_model_names(self):
        _, _, seen, _, _ = self.run_live(self.state(), response())
        self.assertEqual(len(seen), 1)
        sent = seen[0]["state"]
        self.assertEqual(set(sent), {"contract", "run_id", "task"})
        text = json.dumps(sent)
        for local_only in ("opus", "haiku", "fable", "gpt-", "available", "lead_choice"):
            with self.subTest(local_only=local_only):
                self.assertNotIn(local_only, text)

    # --- mapping the task profile ---------------------------------------------

    def test_mechanical_task_goes_to_the_fast_worker_under_the_current_lead(self):
        outcome, _, detail = self.plan(task_mostly_mechanical=0.95)
        self.assertEqual(outcome, "PLAN_PROPOSED")
        worker = self.items(detail)["fast_worker"]
        self.assertEqual((worker["model"], worker["effort"]), ("haiku", "medium"))
        self.assertEqual(worker["status"], "proposed")
        self.assertEqual(detail["lead"], {"model": "claude-opus-5-5", "effort": "medium", "status": "keep"})

    def test_quiet_profile_keeps_the_work_in_the_lead(self):
        outcome, _, detail = self.plan()
        self.assertEqual(outcome, "PLAN_PROPOSED")
        self.assertEqual(detail["items"], [])
        self.assertTrue(detail["keep_in_lead"])

    def test_deep_judgment_suggests_the_premier_lead_without_switching_it(self):
        _, reasons, detail = self.plan(task_needs_deep_judgment=0.92)
        self.assertEqual(detail["lead"], {"model": "fable", "effort": "xhigh", "status": "switch_suggested"})
        self.assertIn("lead_change_suggested", reasons)

    def test_a_premier_session_is_kept_by_family_not_exact_id(self):
        state = self.state(lead_model="claude-fable-5-1", lead_effort="xhigh")
        _, _, detail = self.plan(state, task_needs_deep_judgment=0.92)
        self.assertEqual(detail["lead"]["status"], "keep")

    def test_unclear_judgment_raises_lead_effort_rather_than_the_model(self):
        _, _, detail = self.plan(task_needs_deep_judgment=0.5)
        self.assertEqual(detail["lead"], {"model": "claude-opus-5-5", "effort": "high", "status": "change_effort"})

    def test_parallel_units_fan_out_through_workflow_when_available(self):
        _, _, detail = self.plan(task_parallelizable=0.9)
        self.assertIn("workflow", self.items(detail))
        _, _, detail = self.plan(self.state(available={"workflow": False}),
                                 task_parallelizable=0.9, task_needs_deep_judgment=0.9)
        self.assertEqual(self.items(detail)["deep_reasoner"]["purpose"],
                         "run the independent units in parallel")

    def test_high_stakes_adds_a_cross_vendor_check_per_harness(self):
        _, _, detail = self.plan(task_high_stakes=0.9)
        self.assertEqual(self.items(detail)["cross_vendor_peer"]["model"], "gpt-6-astra")
        _, _, detail = self.plan(self.state(harness="codex", lead_model="gpt-6.1-sol",
                                            lead_effort="high"), task_high_stakes=0.9)
        self.assertEqual(self.items(detail)["cross_vendor_peer"]["model"], "fable")

    def test_a_spawned_peer_runs_on_the_lead_model(self):
        _, _, detail = self.plan(task_outlives_session=0.9)
        peer = self.items(detail)["spawn_peer"]
        self.assertEqual((peer["model"], peer["effort"]), ("claude-opus-5-5", "medium"))

    # --- failing closed -----------------------------------------------------------

    def test_unconfirmed_executor_is_reported_not_substituted(self):
        state = self.state(available={"cross_vendor_peer": False})
        outcome, reasons, detail = self.plan(state, task_high_stakes=0.95)
        self.assertEqual(outcome, "PLAN_PROPOSED")
        self.assertEqual(self.items(detail)["cross_vendor_peer"]["status"], "unavailable")
        self.assertEqual(len(detail["items"]), 1)
        self.assertIn("some_executors_unavailable", reasons)

    def test_unclear_signal_needs_review(self):
        outcome, reasons, detail = self.plan(task_high_stakes=0.5)
        self.assertEqual(outcome, "REVIEW_REQUIRED")
        self.assertEqual(reasons[0], "unclear_task_signal")
        self.assertEqual(detail["unclear_signals"], ["task_high_stakes"])
        self.assertEqual(self.items(detail)["cross_vendor_peer"]["status"], "review")

    def test_premier_lead_unavailable_is_reported(self):
        state = self.state(available={"premier_lead": False})
        _, reasons, detail = self.plan(state, task_needs_deep_judgment=0.9)
        self.assertEqual(detail["lead"]["status"], "unavailable")
        self.assertIn("premier_lead_unavailable", reasons)

    def test_user_pins_win(self):
        state = self.state(model="opus", effort="high")
        _, reasons, detail = self.plan(state, task_needs_deep_judgment=0.95)
        self.assertEqual(detail["lead"], {"model": "opus", "effort": "high", "status": "pinned"})
        self.assertIn("user_pin_applied", reasons)
        state = self.state(topology="lead")
        _, reasons, detail = self.plan(state, task_mostly_mechanical=0.95)
        self.assertEqual(self.items(detail)["fast_worker"]["status"], "excluded_by_pin")
        self.assertIn("topology_pin_excluded_items", reasons)

    # --- boundaries ---------------------------------------------------------------

    def test_mock_routing_is_simulation_only_and_proposes_no_plan(self):
        mock_path = self.write_json("mock.json", response(task_mostly_mechanical=0.95))
        code, result, stdout, _ = self.run_route(
            self.state(), extra=("--mock-response", str(mock_path), "--mode", "advisory")
        )
        self.assertEqual(code, 0)
        self.assertEqual(result["route_status"], "simulation")
        self.assertEqual(result["recommendation"]["outcome"], "NOT_CHECKED")
        self.assertIsNone(result["recommendation"]["lead"])
        self.assertEqual(result["recommendation"]["items"], [])
        self.assertEqual(result["jev"]["simulated_outcome"], "PLAN_PROPOSED")
        self.assertIn("proposed delegations: 0", stdout)

    def test_live_route_records_the_plan_and_still_certifies_nothing(self):
        code, result, _, stdout, _ = self.run_live(self.state(), response(task_mostly_mechanical=0.95))
        self.assertEqual(code, 0)
        self.assertEqual(result["route_status"], "live")
        self.assertTrue(result["live_assessed"])
        self.assertEqual(result["recommendation"]["outcome"], "PLAN_PROPOSED")
        self.assertFalse(result["recommendation"]["applied"])
        self.assertFalse(result["completion_verified"])
        self.assertEqual(result["jev"]["calls"], 1)
        self.assertEqual(result["jev"]["signals"]["task_mostly_mechanical"]["reading"], "yes")

    def test_missing_backend_blocks_the_route_claim(self):
        code, result, _, _ = self.run_route(self.state())
        self.assertEqual(code, 2)
        self.assertEqual(result["route_status"], "not_run")
        self.assertEqual(result["reason_codes"], ["network_not_enabled_and_no_mock_supplied"])
        self.assertEqual(result["recommendation"]["outcome"], "NOT_CHECKED")

    def test_credential_failure_blocks_rather_than_recommending(self):
        state_path = self.write_json("state.json", self.state())
        out = self.root / "blocked.json"
        with mock.patch.object(verify, "get_api_key", return_value=""):
            code, _, stderr = self.invoke(
                ["route", "--state", str(state_path), "--out", str(out), "--allow-network"]
            )
        self.assertEqual(code, 2)
        result = json.loads(out.read_text())
        self.assertEqual(result["reason_codes"], ["live_routing_failed"])
        self.assertFalse(result["live_assessed"])
        self.assertIsNone(result["recommendation"]["lead"])
        self.assertIn("missing or invalid", stderr)

    def test_route_and_completion_states_cannot_be_crossed(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            verify.build_parser().parse_args(
                ["verify", "--contract", "route", "--state", "s.json", "--out", "o.json"]
            )
        manifest = json.loads((SAMPLES / "mock-pass-manifest.json").read_text())
        code, result, _, _ = self.run_route(manifest, name="crossed.json")
        self.assertEqual(code, 2)
        self.assertEqual(result["reason_codes"], ["schema_or_state_validation_failed"])

    def test_route_result_is_not_adjudicable_as_a_completion_result(self):
        mock_path = self.write_json("mock.json", response())
        _, result, _, _ = self.run_route(self.state(), extra=("--mock-response", str(mock_path)))
        with self.assertRaises(verify.ValidationError):
            verify.validate_result_for_adjudication(result)

    def test_contract_shape_rejects_foreign_question_ids(self):
        value = json.loads((verify.CONTRACT_DIR / "route.json").read_text())
        questions = value["questions"]
        questions["unexpected_question"] = questions.pop("task_high_stakes")
        contract_dir = self.root / "contracts"
        contract_dir.mkdir()
        (contract_dir / "route.json").write_text(json.dumps(value))
        with mock.patch.object(verify, "CONTRACT_DIR", contract_dir):
            with self.assertRaisesRegex(verify.ValidationError, "check or question ids"):
                verify.load_contract("route")

    def test_state_rejects_an_unknown_harness_executor_or_effort(self):
        broken_harness = self.state()
        broken_harness["harness"] = "cursor"
        broken_executor = self.state()
        broken_executor["available"]["gpu_cluster"] = True
        broken_effort = self.state()
        broken_effort["lead"]["effort"] = "ultra"
        for value in (broken_harness, broken_executor, broken_effort):
            with self.subTest(value=value), self.assertRaises(verify.ValidationError):
                verify.validate_route_state(copy.deepcopy(value), CONTRACT)

    def test_bundled_samples_stay_loadable(self):
        for name in ("route-state.json", "route-unavailable-state.json"):
            with self.subTest(sample=name):
                raw, _ = verify.read_json(SAMPLES / name)
                verify.validate_route_state(raw, CONTRACT)
        raw, _ = verify.read_json(SAMPLES / "route-mock-response.json")
        verify.validate_response(raw, CONTRACT)


if __name__ == "__main__":
    unittest.main()
