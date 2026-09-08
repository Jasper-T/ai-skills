import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASH = os.environ.get('SKILLS_TEST_BASH', '/bin/bash')
spec = importlib.util.spec_from_file_location('validate_skills', ROOT / 'scripts/validate_skills.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class Workflows(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skills-tests-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / 'source repo'
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                        GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid',
                        CODEX_HOME=str(self.base / 'client'), GIT_TERMINAL_PROMPT='0')
        # Ensure the install subprocess launched by update uses the selected Bash.
        self.bin = self.base / 'bin'
        self.bin.mkdir()
        (self.bin / 'bash').symlink_to(shutil.which(BASH) or BASH)
        self.env['PATH'] = str(self.bin) + os.pathsep + self.env['PATH']

    def run_cmd(self, *args, cwd=None, ok=True):
        result = subprocess.run(args, cwd=cwd or self.repo, env=self.env,
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(result.returncode == 0, ok, result.stdout)
        return result.stdout

    def install(self, target, *args, ok=True):
        return self.run_cmd(BASH, 'scripts/install.sh', '--target', str(target), *args, ok=ok)

    def git(self, *args, cwd=None):
        return self.run_cmd('git', *args, cwd=cwd)

    def test_install_preflight_and_paths(self):
        target = self.base / 'client skills'
        (target / 'skill-repo-sync').mkdir(parents=True)
        self.install(target, ok=False)
        self.assertEqual([p.name for p in target.iterdir()], ['skill-repo-sync'])
        alias = self.base / 'alias'
        alias.symlink_to(self.repo / 'skills')
        for path in [self.repo, self.repo / 'skills', self.repo / 'skills/nested', alias]:
            self.install(path, '--force', ok=False)
        self.assertTrue((self.repo / 'skills/code-modification/SKILL.md').is_file())

    def test_backup_idempotence_and_failure(self):
        target = self.base / 'client skills'
        self.install(target)
        self.assertIn('0 installed, 3 already current', self.install(target))
        for _ in range(2):
            self.install(target, '--copy', '--force')
        backup = self.base / '.client skills.backups'
        self.assertEqual(len(list(backup.glob('*/original'))), 6)
        self.assertEqual(len(list(target.iterdir())), 3)
        fake = self.bin / 'cp'
        fake.write_text('#!/bin/sh\nexit 73\n')
        fake.chmod(0o755)
        output = self.install(target, '--copy', '--force', ok=False)
        self.assertIn('Original content preserved at:', output)
        self.assertIn('0 installed', output)
        self.assertEqual(len(list(backup.glob('*/original'))), 7)

    def test_help_and_arguments_do_not_call_git(self):
        marker = self.base / 'called'
        fake = self.bin / 'git'
        fake.write_text('#!/bin/sh\ntouch "' + str(marker) + '"\nexit 99\n')
        fake.chmod(0o755)
        self.run_cmd(BASH, 'scripts/update.sh', '--help')
        for args in [('--unknown',), ('--target',), ('--target', ''), ('--target', '--force')]:
            self.run_cmd(BASH, 'scripts/update.sh', *args, ok=False)
        self.assertFalse(marker.exists())

    def test_update_git_states_and_empty_arguments(self):
        self.git('init', '-b', 'main')
        self.git('add', '.')
        self.git('commit', '-m', 'fixture')
        remote = self.base / 'remote.git'
        self.git('init', '--bare', str(remote))
        self.git('remote', 'add', 'origin', str(remote))
        self.git('push', '-u', 'origin', 'main')
        self.run_cmd(BASH, 'scripts/update.sh')
        self.assertTrue((self.base / 'client/skills/code-modification/SKILL.md').is_file())
        dirty = self.repo / 'dirty'
        dirty.write_text('local')
        self.assertIn('uncommitted', self.run_cmd(BASH, 'scripts/update.sh', ok=False))
        dirty.unlink()
        self.git('checkout', '--detach')
        self.assertIn('detached HEAD', self.run_cmd(BASH, 'scripts/update.sh', ok=False))
        self.git('checkout', '-b', 'no-upstream')
        self.assertIn('no upstream', self.run_cmd(BASH, 'scripts/update.sh', ok=False))
        self.git('checkout', 'main')
        worktree = self.base / 'worktree'
        self.git('worktree', 'add', '-b', 'linked', str(worktree))
        self.git('branch', '--set-upstream-to=origin/main', cwd=worktree)
        self.assertTrue((worktree / '.git').is_file())
        self.run_cmd(BASH, 'scripts/update.sh', '--target', str(self.base / 'other skills'), cwd=worktree)
        peer = self.base / 'peer'
        self.git('clone', '-b', 'main', str(remote), str(peer))
        (peer / 'remote-change').write_text('remote')
        self.git('add', '.', cwd=peer)
        self.git('commit', '-m', 'remote fixture', cwd=peer)
        self.git('push', cwd=peer)
        self.run_cmd(BASH, 'scripts/update.sh')
        self.assertTrue((self.repo / 'remote-change').exists())
        for directory, filename in [(self.repo, 'local-only'), (peer, 'remote-only')]:
            (directory / filename).write_text(filename)
            self.git('add', '.', cwd=directory)
            self.git('commit', '-m', filename, cwd=directory)
        self.git('push', cwd=peer)
        head = self.git('rev-parse', 'HEAD')
        self.run_cmd(BASH, 'scripts/update.sh', '--target', str(self.base / 'absent'), ok=False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), head)
        self.assertFalse((self.base / 'absent').exists())
        self.assertEqual(self.git('status', '--porcelain'), '')

    def test_metadata_detects_broken_references(self):
        self.assertEqual(validator.validate(self.repo), [])
        skill = self.repo / 'skills/code-modification'
        path = skill / 'agents/openai.yaml'
        path.write_text(path.read_text().replace('$code-modification', '$missing-skill'))
        self.assertTrue(validator.validate(self.repo))
        shutil.copy(ROOT / 'skills/code-modification/agents/openai.yaml', path)
        with (skill / 'SKILL.md').open('a') as out:
            out.write('\n[missing](references/absent.md)\n')
        self.assertTrue(validator.validate(self.repo))


if __name__ == '__main__':
    unittest.main()
