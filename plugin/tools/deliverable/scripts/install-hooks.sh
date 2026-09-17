#!/usr/bin/env bash
# install-hooks.sh -- install the tracked pre-commit gate in a repository.
#
#   install-hooks.sh [REPO_DIR]
#
# Writes .githooks/pre-commit (tracked, so it travels with the repo) and points
# core.hooksPath at it. The hook runs check_deliverable.py --fast --staged for
# every deliverable.yml whose directory holds a staged file. It calls no
# language model and finishes in seconds. Bypass one commit with --no-verify;
# CI reruns the same script, so a bypass never reaches a public build.
set -euo pipefail
REPO="$(git -C "${1:-.}" rev-parse --show-toplevel)"
mkdir -p "$REPO/.githooks"
if [ -e "$REPO/.githooks/pre-commit" ] && ! grep -q 'deliverable fast gate' "$REPO/.githooks/pre-commit"; then
  echo "install-hooks: $REPO/.githooks/pre-commit exists and is not ours; not overwriting" >&2
  exit 1
fi
cat > "$REPO/.githooks/pre-commit" <<'HOOK'
#!/usr/bin/env bash
# pre-commit -- the deliverable fast gate.
# Installed by resources/project_hygiene/scripts/install-hooks.sh
# (core.hooksPath=.githooks). Bypass once with --no-verify; CI reruns it.
set -u
REPO="$(git rev-parse --show-toplevel)"
CHECK="${DELIVERABLE_CHECK:-}"
for c in "$REPO/scripts/check_deliverable.py" \
         "$HOME/Documents/GitHub/resources/open-science-skills/plugin/tools/deliverable/scripts/check_deliverable.py" \
         "$HOME/Documents/github/resources/open-science-skills/plugin/tools/deliverable/scripts/check_deliverable.py" \
         "$HOME/.claude/plugins/cache/open-science-skills/oss"/*/tools/deliverable/scripts/check_deliverable.py \
         "$HOME/Documents/GitHub/resources/project_hygiene/scripts/check_deliverable.py" \
         "$HOME/Documents/github/resources/project_hygiene/scripts/check_deliverable.py"; do
  [ -n "$CHECK" ] && break
  [ -f "$c" ] && CHECK="$c"
done
if [ -z "$CHECK" ]; then
  echo "pre-commit: check_deliverable.py not found; gate skipped" >&2
  exit 0
fi
staged="$(git diff --cached --name-only --diff-filter=ACMR)"
[ -z "$staged" ] && exit 0
status=0
while IFS= read -r manifest; do
  [ -n "$manifest" ] || continue
  dir="$(cd "$REPO" && dirname "$manifest")"
  case "$dir" in .) prefix="" ;; *) prefix="$dir/" ;; esac
  if [ -z "$prefix" ] || printf '%s\n' "$staged" | grep -q "^$prefix"; then
    echo "pre-commit: checking deliverable $manifest"
    python3 "$CHECK" --fast --staged --root "$REPO/$dir" || status=1
  fi
done <<EOF_MANIFESTS
$(cd "$REPO" && git ls-files --cached --others --exclude-standard | grep -E '(^|/)deliverable\.yml$')
EOF_MANIFESTS
if [ "$status" -ne 0 ]; then
  echo "pre-commit: deliverable gate failed (fix, accept, or --no-verify)" >&2
fi
exit $status
HOOK
chmod +x "$REPO/.githooks/pre-commit"
git -C "$REPO" config core.hooksPath .githooks
echo "installed $REPO/.githooks/pre-commit (core.hooksPath=.githooks)"
