#!/usr/bin/env python3
"""Check repeatable, non-overwriting Codex skill installation."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'plugin/scripts/install-codex.py'


class Installer(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / 'skills'

    def run_install(self, *args):
        return subprocess.run(['python3', str(SCRIPT), '--target', str(self.target), *args],
                              capture_output=True, text=True)

    def test_preview_install_and_repeat(self):
        args = ['--skill', 'orchestrate', 'model-committee']
        self.assertEqual(self.run_install(*args, '--dry-run').returncode, 0)
        self.assertFalse(self.target.exists())
        for _ in range(2):
            result = self.run_install(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            for name in args[1:]:
                self.assertTrue((self.target / name).is_symlink())
                self.assertEqual((self.target / name).resolve(), ROOT / 'codex' / name)

    def test_conflicts_preserved_and_missing_links_installed(self):
        self.target.mkdir()
        (self.target / 'orchestrate').mkdir()
        marker = self.target / 'orchestrate/custom.md'
        marker.write_text('custom work')
        (self.target / 'advisor').symlink_to(self.target / 'missing-source')
        (self.target / 'spawn').write_text('existing file')
        result = self.run_install('--skill', 'orchestrate', 'advisor', 'spawn', 'model-committee')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(marker.read_text(), 'custom work')
        self.assertTrue((self.target / 'advisor').is_symlink())
        self.assertFalse((self.target / 'advisor').exists())
        self.assertEqual((self.target / 'spawn').read_text(), 'existing file')
        self.assertTrue((self.target / 'model-committee/SKILL.md').is_file())

    def test_invalid_selection_is_rejected_before_writing(self):
        result = self.run_install('--skill', 'orchestrate', '../escape')
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.target.exists())

    def test_all_matches_source_catalog(self):
        result = self.run_install('--all')
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = {p.parent.name for p in (ROOT / 'codex').glob('*/SKILL.md')}
        self.assertEqual({p.name for p in self.target.iterdir()}, expected)


if __name__ == '__main__':
    unittest.main()
