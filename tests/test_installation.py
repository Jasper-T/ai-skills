import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/check_installation.py'


class Installation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo'
        self.source = self.repo / 'skills'
        (self.source / 'current').mkdir(parents=True)
        (self.source / 'current/SKILL.md').write_text('skill')
        self.target = self.base / 'installed'
        self.target.mkdir()
        spec = importlib.util.spec_from_file_location('check_installation', SCRIPT)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.module.ROOT = self.repo

    def test_missing_wrong_and_directory(self):
        self.assertEqual(self.module.inspect(self.target), 1)
        p = self.target / 'current'
        p.symlink_to(self.base / 'missing')
        self.assertEqual(self.module.inspect(self.target), 1)
        p.unlink()
        p.mkdir()
        self.assertEqual(self.module.inspect(self.target), 1)
        (p / 'SKILL.md').write_text('local')
        self.assertEqual(self.module.inspect(self.target, True), 1)
        self.assertEqual((p / 'SKILL.md').read_text(), 'local')

    def test_prune_ownership_and_idempotence(self):
        (self.target / 'current').symlink_to(self.source / 'current')
        stale = self.target / 'old'
        stale.symlink_to(os.path.relpath(self.source / 'old', self.target))
        external = self.target / 'external'
        external.symlink_to(self.base / 'absent')
        valid = self.target / 'alias'
        valid.symlink_to(self.source / 'current')
        directory = self.target / 'other'
        directory.mkdir()
        # A lexical prefix alone must not establish ownership.
        prefix = self.target / 'prefix'
        prefix.symlink_to(self.repo / 'skills-other/absent')
        # A path under source that escapes through a symlink is not owned.
        (self.source / 'escape').symlink_to(self.base)
        escape = self.target / 'escape'
        escape.symlink_to(self.source / 'escape/absent')
        self.assertEqual(self.module.inspect(self.target), 1)
        self.assertTrue(stale.is_symlink())
        self.assertEqual(self.module.inspect(self.target, True), 0)
        self.assertFalse(stale.is_symlink())
        for p in (external, valid, prefix, escape):
            self.assertTrue(p.is_symlink())
        self.assertTrue(directory.is_dir())
        self.assertEqual(self.module.inspect(self.target, True), 0)

    def test_source_overlap_and_recheck(self):
        for p in (self.source, self.repo, self.source / 'nested'):
            with self.assertRaises(ValueError):
                self.module.inspect(p, True)
        stale = self.target / 'old'
        stale.symlink_to(self.source / 'old')
        with patch.object(self.module, 'candidate', side_effect=[True, False]):
            with self.assertRaises(ValueError):
                self.module.inspect(self.target, True)
        self.assertTrue(stale.is_symlink())

    def test_cli_default_and_errors(self):
        env = dict(os.environ, CODEX_HOME=str(self.base / 'client'))
        result = subprocess.run([sys.executable, '-B', str(SCRIPT)], env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('MISSING:', result.stdout)
        self.assertFalse((self.base / 'client').exists())
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--target'], capture_output=True)
        self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
