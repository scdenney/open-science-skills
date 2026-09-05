#!/usr/bin/env python3
"""Link Codex-native skills without replacing existing user-managed paths."""
import argparse
from pathlib import Path
import sys

SOURCE = Path(__file__).resolve().parents[2] / 'codex'


def install(names, target, dry_run=False):
    conflicts = 0
    for name in names:
        source = SOURCE / name
        destination = target / name
        if destination.is_symlink() and destination.resolve() == source.resolve():
            print(f'OK {name}: already linked')
            continue
        if destination.exists() or destination.is_symlink():
            print(f'CONFLICT {name}: preserving {destination}', file=sys.stderr)
            conflicts += 1
            continue
        if dry_run:
            print(f'WOULD LINK {name}: {destination} -> {source}')
            continue
        target.mkdir(parents=True, exist_ok=True)
        try:
            destination.symlink_to(source, target_is_directory=True)
        except FileExistsError:
            print(f'CONFLICT {name}: path appeared; preserving {destination}', file=sys.stderr)
            conflicts += 1
        else:
            print(f'LINKED {name}: {destination} -> {source}')
    return 1 if conflicts else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument('--all', action='store_true')
    selection.add_argument('--skill', nargs='+', metavar='NAME')
    parser.add_argument('--target', type=Path, default=Path.home() / '.agents/skills')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    available = {p.parent.name for p in SOURCE.glob('*/SKILL.md')}
    names = sorted(available) if args.all else list(dict.fromkeys(args.skill))
    unknown = set(names) - available
    if unknown:
        parser.error('unknown skills: ' + ', '.join(sorted(unknown)))
    try:
        return install(names, args.target.expanduser().absolute(), args.dry_run)
    except OSError as exc:
        print(f'Installation failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
