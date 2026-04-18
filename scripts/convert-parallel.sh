#!/usr/bin/env bash
# Parallel PDF -> Markdown conversion for the knowledge base.
# Uses xargs -P to run N conversions concurrently.
# Usage: ./scripts/convert-parallel.sh [N]     # default: 4 workers
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCES="$PROJECT_ROOT/knowledge_base/og"
OUTPUT="$PROJECT_ROOT/knowledge_base/md"
VENV="$PROJECT_ROOT/.venv"

WORKERS="${1:-4}"

# shellcheck disable=SC1091
source "$VENV/bin/activate"

convert_one() {
    local pdf="$1"
    local rel="${pdf#"$SOURCES/"}"
    local category_dir
    category_dir="$(dirname "$rel")"
    local base
    base="$(basename "$pdf" .pdf)"
    local out_dir="$OUTPUT/$category_dir"
    local out_md="$out_dir/$base.md"

    if [[ -f "$out_md" ]]; then
        return 0
    fi

    mkdir -p "$out_dir"
    echo "[start] $rel"
    if timeout 600 opendataloader-pdf "$pdf" --format markdown --output-dir "$out_dir/" 2>/dev/null; then
        echo "[done]  $rel"
    else
        echo "[fail]  $rel  (timeout or error)"
    fi
}

export -f convert_one
export SOURCES OUTPUT

find "$SOURCES" -type f -name "*.pdf" -not -path "*/_deferred/*" -print0 \
    | xargs -0 -n 1 -P "$WORKERS" bash -c 'convert_one "$0"'

echo ""
echo "All conversions attempted."
