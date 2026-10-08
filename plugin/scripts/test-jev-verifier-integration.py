#!/usr/bin/env python3
"""Guard the opt-in Jev verification sections in the Claude skill library.

The verifier itself is an experiment under experiments/jev-verifier; these tests
cover only the Claude-side surface: that the opt-in is documented, that the
default invocation stays Jev-free, that each skill defers to the shared runtime
instead of restating it, and that an absent runtime or credential is reported as
blocked rather than passed.
"""
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "jev-verifier-claude-code.md"
BUNDLE = ROOT / "experiments" / "jev-verifier"
HEADING = "## Optional Jev verification (--verify)"
ROUTE_HEADING = "## Optional Jev routing (--route)"
RUNTIME_DEFAULT = "${JEV_VERIFIER_HOME:-$HOME/.local/share/oss-experiments/jev-verifier/current}"
# skill -> the shared-runtime file that is authoritative for its contract
SKILLS = {
    "orchestrate": "ORCHESTRATE.md",
    "fact-check": "FACT-CHECK.md",
    "citation-check": "CITATION-CHECK.md",
}
ENDPOINT = "api.typesafe.ai"


def read(path):
    return path.read_text(encoding="utf-8")


def section_of(text, heading, label):
    if heading not in text:
        raise AssertionError(f"{label}: no {heading!r} section")
    return re.split(r"\n## ", text.split(heading, 1)[1], maxsplit=1)[0]


class Sections(unittest.TestCase):
    def section(self, skill):
        text = read(ROOT / "plugin" / "skills" / skill / "SKILL.md")
        self.assertIn(HEADING, text, f"{skill}: no opt-in section")
        body = text.split(HEADING, 1)[1]
        return re.split(r"\n## ", body, maxsplit=1)[0]

    def test_opt_in_syntax_is_claude_native(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                section = self.section(skill)
                self.assertIn(f"/oss:{skill} --verify <task>", section)
                self.assertIn(f"/oss:{skill} --verify jev <task>", section)
                # The other library's `$skill` dialect must not leak in here.
                self.assertNotIn(f"${skill} --verify", section)

    def test_default_invocation_makes_no_call(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                # Emphasis marks vary between the three sections; the claim does not.
                plain = self.section(skill).replace("*", "").replace("`", "")
                self.assertIn("no Jev call", plain)

    def test_defers_to_shared_runtime(self):
        for skill, contract in SKILLS.items():
            with self.subTest(skill=skill):
                section = self.section(skill)
                self.assertIn(f"{RUNTIME_DEFAULT}/{contract}", section)
                for other in set(SKILLS.values()) - {contract}:
                    self.assertNotIn(f"{RUNTIME_DEFAULT}/{other}", section)
                self.assertIn("authoritative", section)
                # The runtime owns the wire format; the skills must not restate it.
                self.assertNotIn(ENDPOINT, section)

    def test_setup_pointer_is_the_installed_bundle_not_a_repo_path(self):
        # An installed skill is a standalone directory: anything it points at
        # must resolve from the installed bundle, not from a repo checkout.
        for skill in SKILLS:
            with self.subTest(skill=skill):
                section = self.section(skill)
                self.assertIn(f"{RUNTIME_DEFAULT}/README.md", section)
                # The bundle path itself contains a directory segment, so drop
                # it before looking for repo-relative paths in what is left.
                rest = section.replace(RUNTIME_DEFAULT, "")
                self.assertNotIn(DOC.name, rest)
                self.assertNotRegex(rest, r"\b(docs|experiments|plugin)/")

    def test_installed_bundle_ships_the_setup_it_promises(self):
        # The skills send users to the bundle README for install and
        # credentials; it has to actually carry both, for a Claude-only host.
        readme = read(BUNDLE / "README.md")
        self.assertIn("--target ~/.claude/skills", readme)
        for needle in ("TYPESAFE_API_KEY", "Login Keychain", "secret-tool"):
            self.assertIn(needle, readme)
        # The shared runtime must not prescribe one library's skills.
        self.assertNotRegex(readme, r"\$(orchestrate|fact-check|citation-check)")
        self.assertNotIn("Use the existing Codex skills", readme)

    def test_missing_runtime_or_credential_is_blocked(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                section = self.section(skill)
                self.assertIn("TYPESAFE_API_KEY", section)
                self.assertIn("**blocked**", section)
                self.assertIn("never", section.lower())
                self.assertIn("mock", section)

    def test_no_credential_is_solicited_or_embedded(self):
        paths = [ROOT / "plugin" / "skills" / s / "SKILL.md" for s in SKILLS] + [DOC]
        for path in paths:
            with self.subTest(path=path.name):
                text = read(path)
                self.assertNotRegex(text, r"TYPESAFE_API_KEY\s*=\s*\S")
                self.assertNotRegex(text, r"(?i)paste (your |the )?(api )?key")

    def test_flat_skill_copies_are_in_sync(self):
        for skill in SKILLS:
            with self.subTest(skill=skill):
                self.assertEqual(
                    read(ROOT / "plugin" / "skills" / skill / "SKILL.md"),
                    read(ROOT / "plugin" / ".skills" / f"{skill}.md"),
                )


class RouteSection(unittest.TestCase):
    """The opt-in routing surface, which orchestrate alone carries."""

    def setUp(self):
        self.skill = read(ROOT / "plugin" / "skills" / "orchestrate" / "SKILL.md")
        self.section = section_of(self.skill, ROUTE_HEADING, "orchestrate")

    def test_routing_is_offered_by_orchestrate_only(self):
        for skill in set(SKILLS) - {"orchestrate"}:
            with self.subTest(skill=skill):
                self.assertNotIn(
                    ROUTE_HEADING, read(ROOT / "plugin" / "skills" / skill / "SKILL.md")
                )

    def test_opt_in_syntax_is_claude_native(self):
        self.assertIn("/oss:orchestrate --route <task>", self.section)
        self.assertIn("/oss:orchestrate --route jev <task>", self.section)
        self.assertNotIn("$orchestrate --route", self.section)

    def test_default_invocation_makes_no_call(self):
        plain = self.section.replace("*", "").replace("`", "")
        self.assertIn("no Jev call", plain)

    def test_defers_to_the_shared_route_contract(self):
        self.assertIn(f"{RUNTIME_DEFAULT}/ROUTE.md", self.section)
        self.assertIn(f"{RUNTIME_DEFAULT}/README.md", self.section)
        self.assertIn("authoritative", self.section)
        # The runtime owns the wire format and the repo layout is not installed.
        self.assertNotIn(ENDPOINT, self.section)
        rest = self.section.replace(RUNTIME_DEFAULT, "")
        self.assertNotRegex(rest, r"\b(docs|experiments|plugin)/")

    def test_route_and_verify_stay_separate_claims(self):
        self.assertIn("independent and composable", self.section)
        self.assertIn("/oss:orchestrate --route --verify <task>", self.section)
        self.assertIn("never evidence that work was completed", self.section)
        # And the completion section says the same thing from its own side.
        verify_section = section_of(self.skill, HEADING, "orchestrate")
        self.assertIn("separate state, contract, and checkpoint", verify_section)
        self.assertIn("Parse `--route`, `--verify`", self.skill)

    def test_jev_profiles_the_task_and_no_model_name_is_sent(self):
        plain = self.section.replace("*", "")
        self.assertIn("Jev profiles the task; the plan is built locally", plain)
        self.assertIn("No model name leaves the machine", plain)
        self.assertIn("fable`/`opus`/`haiku` aliases", plain)

    def test_availability_is_the_harness_s_and_fails_closed(self):
        plain = self.section.replace("*", "")
        self.assertIn("You declare what this session can launch", plain)
        self.assertIn("comes back `unavailable`", plain)
        self.assertIn("never launch one under another executor's name", plain)

    def test_the_plan_is_shown_before_anything_launches(self):
        plain = self.section.replace("*", "")
        self.assertIn("Record your own plan before reading the result", plain)
        self.assertIn("let the user change it before anything launches", plain)
        self.assertIn("Apply `proposed` items", plain)

    def test_user_pins_win_and_the_live_lead_is_not_switchable(self):
        plain = self.section.replace("*", "").replace("`", "")
        self.assertIn("take precedence", plain)
        self.assertIn("--effort auto is implicit only while routing", plain)
        self.assertIn("cannot switch the model this session is already running on", plain)

    def test_missing_runtime_or_credential_is_blocked(self):
        self.assertIn("TYPESAFE_API_KEY", self.section)
        self.assertIn("**blocked**", self.section)
        self.assertIn("never", self.section.lower())
        self.assertIn("mock", self.section)


class TopologyPolicy(unittest.TestCase):
    """Ordinary orchestration must choose a topology, and not default to a worktree."""

    def setUp(self):
        text = read(ROOT / "plugin" / "skills" / "orchestrate" / "SKILL.md")
        self.section = section_of(
            text.split("## Run the loop", 1)[1],
            "### Topology",
            "orchestrate",
        )

    def test_every_supported_topology_is_named(self):
        for needle in ("stays with the lead", "Agent", "Workflow", "codex-peer.sh"):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.section)

    def test_the_lead_is_the_default_and_a_worktree_is_not(self):
        plain = self.section.replace("*", "")
        self.assertIn("the work stays with you", plain)
        self.assertIn("a worktree is not the starting point", plain)
        self.assertIn("Isolation alone is not a reason to leave the session", plain)

    def test_the_stated_decision_dimensions_are_all_present(self):
        for dimension in ("Coupling", "Duration", "Parallelism", "Isolation",
                          "Persistence", "Harness support"):
            with self.subTest(dimension=dimension):
                self.assertIn(f"**{dimension}**", self.section)
        self.assertIn("does this session actually have the mechanism", self.section)


class SetupDoc(unittest.TestCase):
    def setUp(self):
        self.text = read(DOC)

    def test_documents_both_credential_stores_and_the_env_fallback(self):
        for needle in ("TYPESAFE_API_KEY", "TypeSafe Jev API", "Login Keychain",
                       "secret-tool", "typesafe-jev"):
            self.assertIn(needle, self.text)

    def test_states_experimental_status_and_blocked_behavior(self):
        self.assertIn("experiment", self.text.lower())
        self.assertIn("blocked", self.text)
        self.assertIn("JEV_VERIFIER_HOME", self.text)

    def test_documents_the_routing_opt_in_and_its_boundary(self):
        self.assertIn("/oss:orchestrate --route <task>", self.text)
        self.assertIn("Claude Code declares which executors it can launch", self.text)
        self.assertIn("not a calibrated model router", self.text)
        self.assertIn("uncalibrated", self.text)
        self.assertIn("launches nothing", self.text)

    def test_discloses_what_a_route_request_actually_sends(self):
        self.assertIn("only the task", self.text)
        self.assertIn("no model name", self.text)


if __name__ == "__main__":
    unittest.main()
