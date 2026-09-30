"""Installer checks confined to temporary skill and runtime roots."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("jev_install", Path(__file__).parents[1] / "install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.source = self.root / "source"
        self.skills = self.root / "skills"
        self.data = self.root / "data"
        for relative in installer.SOURCE_REQUIRED_FILES:
            self.write(self.source / relative, "runtime content\n")
        (self.source / "tools/jev/verify.py").chmod(0o755)
        for relative in installer.REQUIRED_ORCHESTRATE_FILES:
            self.write(self.skills / "orchestrate" / relative, "base dependency\n")
        self.base_hash = installer.content_hash(self.skills / "orchestrate")

    def write(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_install(self, *extra):
        argv = ["install.py", "--target", str(self.skills), "--data-dir", str(self.data), *extra]
        with patch.object(installer, "source_root", return_value=self.source), \
             patch.object(installer, "git_commit", return_value="test-commit"), \
             patch("sys.argv", argv), contextlib.redirect_stdout(io.StringIO()), \
             contextlib.redirect_stderr(io.StringIO()):
            return installer.main()

    def assert_refused(self, *extra):
        with self.assertRaises(SystemExit) as raised:
            self.run_install(*extra)
        self.assertEqual(raised.exception.code, 2)

    def legacy_install(self):
        staging = self.root / "legacy"
        for relative in (
            "skills/orchestrate-ver/SKILL.md", "skills/orchestrate-ver/agents/openai.yaml",
            "tools/jev/verify.py", "tools/jev/contracts/orchestrate.json",
        ):
            self.write(staging / relative, "legacy content\n")
        (staging / "tools/jev/verify.py").chmod(0o755)
        digest = installer.content_hash(staging)
        self.data.mkdir()
        version = self.data / digest
        staging.rename(version)
        self.write(version / installer.MANIFEST, json.dumps({
            "installer": "jev-verifier", "content_hash": digest,
        }))
        link = self.skills / "orchestrate-ver"
        link.symlink_to(version / "skills/orchestrate-ver", target_is_directory=True)
        return version, link

    def test_fresh_repeat_and_upgrade_preserve_dependency_and_versions(self):
        self.assertEqual(self.run_install(), 0)
        current = self.data / "current"
        first = current.resolve()
        manifest = (first / installer.MANIFEST).read_bytes()
        provenance = json.loads(manifest)["orchestrate_dependency"]
        self.assertEqual(provenance["path"], str(self.skills / "orchestrate"))
        self.assertEqual(provenance["skill_sha256"], installer.file_hash(self.skills / "orchestrate/SKILL.md"))
        self.assertFalse((first / "skills").exists())
        self.assertEqual(self.run_install(), 0)
        self.assertEqual(current.resolve(), first)
        self.assertEqual((first / installer.MANIFEST).read_bytes(), manifest)
        self.write(self.source / "ORCHESTRATE.md", "updated runtime instructions\n")
        self.assertEqual(self.run_install(), 0)
        self.assertNotEqual(current.resolve(), first)
        self.assertTrue(installer.valid_installed_version(first, first.name))
        self.assertEqual(installer.content_hash(self.skills / "orchestrate"), self.base_hash)
        self.assertEqual(list(self.skills.iterdir()), [self.skills / "orchestrate"])

    def test_current_user_directory_and_symlink_refused(self):
        current = self.data / "current"
        current.mkdir(parents=True)
        self.write(current / "personal", "keep")
        self.assert_refused()
        self.assertEqual((current / "personal").read_text(), "keep")
        (current / "personal").unlink()
        current.rmdir()
        current.symlink_to(self.source, target_is_directory=True)
        self.assert_refused()
        self.assertEqual(current.resolve(), self.source)

    def test_migrates_only_owned_legacy_link(self):
        version, link = self.legacy_install()
        self.assertEqual(self.run_install(), 0)
        self.assertFalse(link.is_symlink())
        self.assertTrue(version.exists())
        self.assertTrue(installer.valid_installed_version(version, version.name, legacy=True))
        self.assertTrue((self.data / "current").is_symlink())

    def test_user_legacy_target_refused(self):
        link = self.skills / "orchestrate-ver"
        link.symlink_to(self.source, target_is_directory=True)
        self.assert_refused()
        self.assertEqual(link.resolve(), self.source)
        self.assertFalse(self.data.exists())

    def test_tampered_legacy_refused(self):
        version, link = self.legacy_install()
        self.write(version / "skills/orchestrate-ver/SKILL.md", "tampered")
        self.assert_refused()
        self.assertTrue(link.is_symlink())
        self.assertFalse((self.data / "current").exists())

    def test_tampered_current_and_unlinked_version_refused_even_dry_run(self):
        self.run_install()
        current = self.data / "current"
        version = current.resolve()
        self.write(version / "ORCHESTRATE.md", "tampered")
        self.assert_refused()
        current.unlink()
        self.assert_refused("--dry-run")
        self.assert_refused()
        self.assertFalse(current.exists())

    def test_dry_run_has_no_writes(self):
        self.assertEqual(self.run_install("--dry-run"), 0)
        self.assertFalse(self.data.exists())
        version, link = self.legacy_install()
        before = installer.content_hash(version)
        self.assertEqual(self.run_install("--dry-run"), 0)
        self.assertTrue(link.is_symlink())
        self.assertEqual(installer.content_hash(version), before)
        self.assertFalse((self.data / "current").exists())

    def test_missing_dependency_refused(self):
        (self.skills / "orchestrate/scripts/check-lead-runtime.sh").unlink()
        self.assert_refused()
        self.assertFalse(self.data.exists())

    def test_claude_shaped_dependency_accepted_without_the_codex_shape(self):
        # A Claude-only host has no scripts/check-lead-runtime.sh; its plugin
        # skill ships the agent definitions instead, and must satisfy the
        # dependency on its own.
        (self.skills / "orchestrate/scripts/check-lead-runtime.sh").unlink()
        for relative in installer.CLAUDE_ORCHESTRATE_FILES:
            self.write(self.skills / "orchestrate" / relative, "claude dependency\n")
        self.assertEqual(self.run_install(), 0)
        manifest = (self.data / "current").resolve() / installer.MANIFEST
        provenance = json.loads(manifest.read_text(encoding="utf-8"))["orchestrate_dependency"]
        self.assertEqual(provenance["path"], str(self.skills / "orchestrate"))

    def test_partial_dependency_of_either_shape_refused(self):
        # SKILL.md alone is not a complete skill in either library.
        for relative in installer.REQUIRED_ORCHESTRATE_FILES[1:]:
            (self.skills / "orchestrate" / relative).unlink()
        self.write(self.skills / "orchestrate/agents/deep-reasoner.md", "half\n")
        self.assert_refused()
        self.assertFalse(self.data.exists())

    def test_checkout_counterpart_resolves_for_either_library(self):
        import shutil
        for library in ("plugin/skills", "codex"):
            with self.subTest(library=library):
                shutil.rmtree(self.data, ignore_errors=True)
                checkout = self.root / "checkout" / library.replace("/", "-")
                source = checkout / "experiments" / "jev-verifier"
                shutil.rmtree(checkout, ignore_errors=True)
                shutil.copytree(self.source, source)
                shape = (installer.CLAUDE_ORCHESTRATE_FILES if library == "plugin/skills"
                         else installer.REQUIRED_ORCHESTRATE_FILES)
                for relative in shape:
                    self.write(checkout / library / "orchestrate" / relative, "counterpart\n")
                empty = self.root / "empty-skills"
                empty.mkdir(exist_ok=True)
                resolved = installer.resolve_orchestrate(empty, source)
                self.assertEqual(resolved, (checkout / library / "orchestrate").resolve())

    def test_missing_research_bundle_file_refused(self):
        missing = self.source / "tools/jev/contracts/fact-check.json"
        missing.unlink()
        self.assert_refused()
        self.assertFalse(self.data.exists())

    def test_metadata_excluded_from_hash_and_copy(self):
        before = installer.content_hash(self.source)
        for relative in (installer.MANIFEST, "__pycache__/module.pyc", ".pytest_cache/cache"):
            self.write(self.source / relative, "ignored")
        self.assertEqual(installer.content_hash(self.source), before)
        self.run_install()
        version = (self.data / "current").resolve()
        self.assertTrue(installer.valid_installed_version(version, before))
        self.assertFalse((version / "__pycache__").exists())
        self.assertFalse((version / ".pytest_cache").exists())


if __name__ == "__main__":
    unittest.main()
