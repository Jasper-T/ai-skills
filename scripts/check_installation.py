"""Inspect installed Skills; optionally remove broken links owned by this repository."""
import argparse
import os
from pathlib import Path
import stat
import sys

ROOT = Path(__file__).resolve().parents[1]


def candidate(path, source):
    """Require both lexical and resolved ownership, and a genuinely missing target."""
    if not path.is_symlink():
        return False
    raw = Path(os.path.abspath(path.parent / os.readlink(path)))
    resolved = raw.resolve()
    if source not in raw.parents or source not in resolved.parents:
        return False
    try:
        path.stat()
    except FileNotFoundError:
        return True
    return False


def inspect(target, prune=False):
    source = (ROOT / 'skills').resolve()
    target = target.expanduser().resolve()
    if target == source or target in source.parents or source in target.parents:
        raise ValueError('Installation directory overlaps repository Skills source')
    skills = sorted(p for p in source.iterdir() if (p / 'SKILL.md').is_file())
    if not skills:
        raise ValueError('No source Skills found')
    problems = 0
    for skill in skills:
        path = target / skill.name
        if path.is_symlink():
            if path.resolve() == skill.resolve() and (path / 'SKILL.md').is_file():
                print(f'OK: {skill.name}')
                continue
            print(f'WRONG LINK: {skill.name}')
        elif path.is_dir():
            print(f'DIRECTORY (content not compared): {skill.name}')
            if not (path / 'SKILL.md').is_file():
                print(f'MISSING SKILL.md: {skill.name}')
            # A real directory is not evidence of synchronization with the source.
        elif path.exists():
            print(f'CONFLICT: {skill.name}')
        else:
            print(f'MISSING: {skill.name}')
        problems += 1
    if target.exists():
        for path in sorted(target.iterdir()):
            if not candidate(path, source):
                continue
            if not prune:
                print(f'PRUNE CANDIDATE: {path.name}')
                problems += 1
                continue
            before = path.lstat()
            link = os.readlink(path)
            # Recheck the link and target immediately before unlinking.
            if not candidate(path, source):
                raise ValueError(f'Link changed during inspection: {path}')
            after = path.lstat()
            if (before.st_dev, before.st_ino, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_mtime_ns) or not stat.S_ISLNK(after.st_mode) or os.readlink(path) != link:
                raise ValueError(f'Link changed during inspection: {path}')
            path.unlink()
            print(f'PRUNED: {path.name}')
    return 1 if problems else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex') / 'skills')
    parser.add_argument('--prune', action='store_true', help='Remove only broken links pointing inside this repository Skills source')
    args = parser.parse_args()
    try:
        return inspect(args.target, args.prune)
    except (OSError, RuntimeError, ValueError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
