#!/usr/bin/env python3
"""Guard the Codex orchestrate topology and opt-in Jev routing surface."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "codex" / "orchestrate" / "SKILL.md"
RUNTIME = "${JEV_VERIFIER_HOME:-$HOME/.local/share/oss-experiments/jev-verifier/current}"


class CodexOrchestrateRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")

    def test_route_is_opt_in_and_jev_is_the_default_provider(self):
        section = self.text.split("## Optional Jev routing (`--route`)", 1)[1]
        section = section.split("\n## ", 1)[0]
        self.assertIn("$orchestrate --route <task>", section)
        self.assertIn("--route jev <task>", section)
        self.assertIn("$orchestrate --route --verify <task>", section)
        self.assertIn("Without `--route`", section)
        self.assertIn("no Jev route call", section)
        self.assertIn(f"{RUNTIME}/ROUTE.md", section)

    def test_verify_is_independent_and_composable(self):
        section = self.text.split("## Optional Jev verification (`--verify`)", 1)[1]
        section = section.split("\n## ", 1)[0]
        self.assertIn("$orchestrate --verify <task>", section)
        self.assertIn("--route` and `--verify` are independent and composable", section)
        self.assertIn("Apply `proposed` items", self.text)
        self.assertIn(f"{RUNTIME}/ORCHESTRATE.md", section)

    def test_normal_workflow_selects_topology_without_forcing_worktrees(self):
        self.assertIn("## Choose the execution topology", self.text)
        for option in ("native `spawn_agent` workers", "one-shot CLI call", "`$spawn`", "Keep work in the lead"):
            with self.subTest(option=option):
                self.assertIn(option, self.text)
        self.assertIn("A different model alone does not require a worktree", self.text)

    def test_router_cannot_claim_unavailable_models_or_override_user_pins(self):
        self.assertIn("a user-specified effort or model pins the lead and takes precedence", self.text)
        self.assertIn("so no model name is sent", self.text)
        self.assertIn("never launch an `unavailable` item under another executor", self.text)
        self.assertIn("run your own plan and say Jev did not shape it", self.text)

if __name__ == "__main__":
    unittest.main()
