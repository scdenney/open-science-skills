#!/usr/bin/env bash
# install.sh — Selective installer for open-science-skills
# Installs one or more skills into a Claude Code skills directory.
#
# Usage:
#   bash scripts/install.sh                    # interactive
#   bash scripts/install.sh --all              # install all skills
#   bash scripts/install.sh --skill conjoint-design survey-design
#   bash scripts/install.sh --target ~/.claude/skills   # custom target
#
# Default target: ./.claude/skills (project-level, current directory)

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
DEFAULT_TARGET="./.claude/skills"

# Parse arguments
TARGET=""
SELECTED_SKILLS=()
INSTALL_ALL=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)        INSTALL_ALL=true; shift ;;
    --target)     TARGET="$2"; shift 2 ;;
    --skill)      shift; while [[ $# -gt 0 && "$1" != --* ]]; do SELECTED_SKILLS+=("$1"); shift; done ;;
    *)            echo "Unknown argument: $1"; exit 1 ;;
  esac
done

[[ -z "$TARGET" ]] && TARGET="$DEFAULT_TARGET"

# Discover available skills
AVAILABLE=()
for dir in "$SKILLS_DIR"/*/; do
  [[ -f "$dir/SKILL.md" ]] && AVAILABLE+=("$(basename "$dir")")
done

if [[ ${#AVAILABLE[@]} -eq 0 ]]; then
  echo "No skills found in $SKILLS_DIR" >&2
  exit 1
fi

# Interactive selection if no flags given
if [[ "$INSTALL_ALL" == false && ${#SELECTED_SKILLS[@]} -eq 0 ]]; then
  echo ""
  echo "Available skills:"
  echo ""
  for i in "${!AVAILABLE[@]}"; do
    printf "  [%2d] %s\n" "$((i+1))" "${AVAILABLE[$i]}"
  done
  echo "  [ a] All skills"
  echo ""
  read -rp "Select skills to install (e.g. 1 3 5, or 'a' for all): " SELECTION

  if [[ "$SELECTION" == "a" || "$SELECTION" == "all" ]]; then
    INSTALL_ALL=true
  else
    for num in $SELECTION; do
      idx=$((num - 1))
      if [[ $idx -ge 0 && $idx -lt ${#AVAILABLE[@]} ]]; then
        SELECTED_SKILLS+=("${AVAILABLE[$idx]}")
      else
        echo "Invalid selection: $num" >&2
      fi
    done
  fi
fi

# Resolve final list
if [[ "$INSTALL_ALL" == true ]]; then
  SELECTED_SKILLS=("${AVAILABLE[@]}")
fi

if [[ ${#SELECTED_SKILLS[@]} -eq 0 ]]; then
  echo "No skills selected. Exiting."
  exit 0
fi

# Install
echo ""
echo "Installing to: $TARGET"
mkdir -p "$TARGET"

for skill in "${SELECTED_SKILLS[@]}"; do
  src="$SKILLS_DIR/$skill/SKILL.md"
  dst="$TARGET/$skill/SKILL.md"
  if [[ ! -f "$src" ]]; then
    echo "  ✗ $skill — not found, skipping"
    continue
  fi
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  echo "  ✓ $skill"
done

echo ""
echo "Done. Skills installed to $TARGET"
echo "Restart Claude Code (or open a new session) to load the new skills."
