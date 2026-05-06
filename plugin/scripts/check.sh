#!/usr/bin/env bash
# check.sh - lightweight package consistency checks for open-science-skills.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
import json
from pathlib import Path

for path in [Path("plugin/.claude-plugin/plugin.json"), Path(".claude-plugin/marketplace.json")]:
    with path.open(encoding="utf-8") as f:
        json.load(f)
print("json ok")
PY

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

find plugin/skills -mindepth 2 -maxdepth 2 -name SKILL.md \
  | sed 's#plugin/skills/##; s#/SKILL.md$##' \
  | sort > "$tmpdir/skills"

find plugin/commands -maxdepth 1 -name '*.md' \
  | sed 's#plugin/commands/##; s#.md$##' \
  | sort > "$tmpdir/commands"

find plugin/.skills -maxdepth 1 -name '*.md' \
  | sed 's#plugin/.skills/##; s#.md$##' \
  | sort > "$tmpdir/flat"

if ! diff -u "$tmpdir/skills" "$tmpdir/commands"; then
  echo "skill/command mismatch" >&2
  exit 1
fi

if ! diff -u "$tmpdir/skills" "$tmpdir/flat"; then
  echo "skill/.skills mismatch" >&2
  exit 1
fi

while IFS= read -r skill; do
  src="plugin/skills/$skill/SKILL.md"
  flat="plugin/.skills/$skill.md"
  if ! diff -q "$src" "$flat" >/dev/null; then
    echo "flat skill is stale: $skill" >&2
    exit 1
  fi
  if ! sed -n '1,8p' "$src" | grep -q "^name: $skill$"; then
    echo "frontmatter name mismatch: $skill" >&2
    exit 1
  fi
  if ! sed -n '1,8p' "$src" | grep -q "^description:"; then
    echo "missing description: $skill" >&2
    exit 1
  fi
done < "$tmpdir/skills"

count="$(wc -l < "$tmpdir/skills" | tr -d ' ')"
if ! grep -q "skills-$count-blue" README.md; then
  echo "README skill badge does not match count $count" >&2
  exit 1
fi

echo "package ok: $count skills"
