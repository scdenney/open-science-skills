#!/usr/bin/env bash
# Convert PDFs/docx in knowledge_base/og/**/ to Markdown in knowledge_base/md/**/
# Skips files that already have a corresponding .md in knowledge_base/md/
# Usage: ./scripts/convert-sources.sh          # incremental (new files only)
#        ./scripts/convert-sources.sh --all     # reconvert everything
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCES="$PROJECT_ROOT/knowledge_base/og"
OUTPUT="$PROJECT_ROOT/knowledge_base/md"
VENV="$PROJECT_ROOT/.venv"

FORCE=false
[[ "${1:-}" == "--all" ]] && FORCE=true

mkdir -p "$OUTPUT"

if [[ ! -d "$VENV" ]]; then
    echo "ERROR: venv not found at $VENV — run: python -m venv .venv && source .venv/bin/activate && pip install opendataloader-pdf"
    exit 1
fi

# shellcheck disable=SC1091
source "$VENV/bin/activate"

converted=0
skipped=0

# Find all PDFs recursively under og/
while IFS= read -r -d '' pdf; do
    rel="${pdf#"$SOURCES/"}"                   # e.g., conjoint-design/foo.pdf
    category_dir="$(dirname "$rel")"            # e.g., conjoint-design
    base="$(basename "$pdf" .pdf)"
    out_dir="$OUTPUT/$category_dir"
    out_md="$out_dir/$base.md"

    if [[ "$FORCE" == false && -f "$out_md" ]]; then
        skipped=$((skipped + 1))
        continue
    fi

    mkdir -p "$out_dir"
    echo "Converting $rel..."
    opendataloader-pdf "$pdf" --format markdown --output-dir "$out_dir/" || {
        echo "  WARNING: conversion failed for $rel"
        continue
    }
    converted=$((converted + 1))
done < <(find "$SOURCES" -type f -name "*.pdf" -print0)

# .docx via pandoc
while IFS= read -r -d '' docx; do
    rel="${docx#"$SOURCES/"}"
    category_dir="$(dirname "$rel")"
    base="$(basename "$docx" .docx)"
    out_dir="$OUTPUT/$category_dir"
    out_md="$out_dir/$base.md"

    if [[ "$FORCE" == false && -f "$out_md" ]]; then
        skipped=$((skipped + 1))
        continue
    fi

    mkdir -p "$out_dir"
    echo "Converting $rel..."
    pandoc "$docx" -t markdown -o "$out_md"
    converted=$((converted + 1))
done < <(find "$SOURCES" -type f -name "*.docx" -print0)

echo ""
echo "Converted: $converted  |  Skipped (already done): $skipped"
[[ $converted -eq 0 ]] && echo "Nothing new to convert."
