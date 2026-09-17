#!/usr/bin/env bash
# check.sh - lightweight package consistency checks for open-science-skills.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
import json
import subprocess
import sys
from pathlib import Path
import yaml

for path in [Path("plugin/.claude-plugin/plugin.json"), Path(".claude-plugin/marketplace.json")]:
    with path.open(encoding="utf-8") as f:
        json.load(f)
print("json ok")

skills = sorted(Path("plugin/skills").glob("*/SKILL.md")) + sorted(Path("codex").glob("*/SKILL.md"))
for path in skills:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"missing frontmatter: {path}"
    metadata = yaml.safe_load(text.split("---", 2)[1])
    assert metadata.get("name") == path.parent.name, f"name mismatch: {path}"
    assert isinstance(metadata.get("description"), str) and metadata["description"].strip(), f"missing description: {path}"
    # Anthropic caps a skill description at 1024 characters. Over the cap the
    # skill is rejected at load, and nothing upstream says so out loud.
    n = len(metadata["description"])
    assert n <= 1024, f"description is {n} chars, over the 1024 cap: {path}"
for path in Path("codex").glob("*/agents/openai.yaml"):
    yaml.safe_load(path.read_text(encoding="utf-8"))
print(f"yaml ok: {len(skills)} skills and Codex UI metadata")

# Glob rather than a hardcoded list: a newly bundled helper must be guarded the
# day it is added. SyncThing's 777 + core.fileMode false hides a bad mode locally,
# so the tracked mode in the index is the only thing worth asserting.
helpers = sorted(
    str(p) for root in ("plugin/skills", "plugin/tools", "codex")
    for pat in ("*.sh", "*.py") for p in Path(root).rglob(pat)
)
assert helpers, "no bundled helper scripts found -- glob is wrong"
for name in helpers:
    entry = subprocess.check_output(["git", "ls-files", "-s", "--", name], text=True)
    assert entry, f"helper is untracked: {name}"
    assert entry.startswith("100755 "), f"helper must be tracked executable: {name}"
    if name.endswith(".sh"):
        subprocess.run(["bash", "-n", name], check=True)
    else:
        subprocess.run([sys.executable, "-m", "py_compile", name], check=True)
print(f"helper syntax and executable modes ok: {len(helpers)} scripts")
tool = Path("plugin/tools/deliverable")
if tool.is_dir():
    for sub in ("scripts", "kinds"):
        assert (tool / sub).is_dir(), f"deliverable toolchain is missing {sub}/"
    assert (tool / "scripts" / "check_deliverable.py").exists(), "lint scripts need check_deliverable.py as a sibling"
    assert list((tool / "kinds").glob("*.md")), "no kind profiles"
    print(f"deliverable toolchain ok: {len([x for x in (tool/"scripts").iterdir() if x.is_file()])} scripts, {len(list((tool/'kinds').glob('*.md')))} kind profiles")

PY

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

find plugin/skills -mindepth 2 -maxdepth 2 -name SKILL.md \
  | sed 's#plugin/skills/##; s#/SKILL.md$##' \
  | sort > "$tmpdir/skills"

# Every skill is its own slash command: Claude Code registers plugin skills as
# /oss:<name> directly. A command file that shares a skill's name therefore
# registers a SECOND, duplicate menu entry. So plugin/commands/ holds only alias
# commands -- thin wrappers that invoke an existing skill with a preset parameter
# (e.g. model-committee's chair) -- and no command may share a skill's name.
cat > "$tmpdir/aliases" <<'ALIASES'
diverge-codex
fair-check
model-committee-astra
model-committee-opus
model-committee-sol
paper-review-lite-codex
post-ocr-cleanup
survey-flow-audit
verify
vlm-ocr-evaluation
vlm-ocr-pipeline
ALIASES

find plugin/commands -maxdepth 1 -name '*.md' \
  | sed 's#plugin/commands/##; s#.md$##' \
  | sort > "$tmpdir/commands-all"

# Every declared alias must exist as a command file.
missing_aliases="$(comm -13 "$tmpdir/commands-all" "$tmpdir/aliases")"
if [ -n "$missing_aliases" ]; then
  echo "alias command declared but missing from plugin/commands: $missing_aliases" >&2
  exit 1
fi

# ...and every command file must be a declared alias. Anything else is either an
# undeclared alias or a duplicate of a skill's own slash command.
undeclared="$(comm -23 "$tmpdir/commands-all" "$tmpdir/aliases")"
if [ -n "$undeclared" ]; then
  echo "command file is not a declared alias: $undeclared" >&2
  exit 1
fi

# No command may collide with a skill name, which would register a duplicate entry.
collisions="$(comm -12 "$tmpdir/commands-all" "$tmpdir/skills")"
if [ -n "$collisions" ]; then
  echo "command duplicates a skill's own slash command: $collisions" >&2
  exit 1
fi

find plugin/.skills -maxdepth 1 -name '*.md' \
  | sed 's#plugin/.skills/##; s#.md$##' \
  | sort > "$tmpdir/flat"

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
  # Every skill is on demand. Implicit invocation costs context in every session
  # whether or not the skill is used; a name is the cheaper trigger.
  if ! sed -n '1,8p' "$src" | grep -q "^disable-model-invocation: true$"; then
    echo "skill is not on-demand (missing disable-model-invocation): $skill" >&2
    exit 1
  fi
done < "$tmpdir/skills"

# The Codex library states the same policy in its own dialect.
while IFS= read -r skill; do
  yml="codex/$skill/agents/openai.yaml"
  if ! grep -q "allow_implicit_invocation: false" "$yml"; then
    echo "codex skill is not on-demand: $skill" >&2
    exit 1
  fi
done < <(find codex -mindepth 1 -maxdepth 1 -type d ! -name assets | sed 's#codex/##' | sort)

count="$(wc -l < "$tmpdir/skills" | tr -d ' ')"
if ! grep -q "Claude_skills-$count-" README.md; then
  echo "README Claude skills badge does not match count $count" >&2
  exit 1
fi

codex_count="$(find codex -mindepth 1 -maxdepth 1 -type d ! -name assets | wc -l | tr -d ' ')"
if ! grep -q "Codex_skills-$codex_count-" README.md; then
  echo "README Codex skills badge does not match count $codex_count" >&2
  exit 1
fi

# The two manifests and the README prose must agree with the directory count.
for f in plugin/.claude-plugin/plugin.json .claude-plugin/marketplace.json; do
  if ! grep -q "$count \(Claude Code \)\?skills" "$f"; then
    echo "$f description does not say $count skills" >&2
    exit 1
  fi
done
v1="$(python3 -c 'import json;print(json.load(open("plugin/.claude-plugin/plugin.json"))["version"])')"
v2="$(python3 -c 'import json;print(json.load(open(".claude-plugin/marketplace.json"))["plugins"][0]["version"])')"
if [ "$v1" != "$v2" ]; then
  echo "version mismatch: plugin.json $v1 vs marketplace.json $v2" >&2
  exit 1
fi
if ! grep -q "^## \[$v1\]" CHANGELOG.md; then
  echo "CHANGELOG.md has no entry for $v1" >&2
  exit 1
fi

echo "package ok: $count Claude skills, $codex_count Codex skills, v$v1"
