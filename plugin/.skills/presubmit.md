---
name: presubmit
description: Launcher and setup wizard for the standalone presubmit CLI, an API-driven adversarial peer-review pipeline of 30-plus stages (Red Team finders, Blue Team defence, verification cascade, legal pass, copyedit) that writes one consolidated review report to disk. Verifies the install and the API key, settles where output lands, picks smoke, standard, or custom mode, launches the run, and reports where the report ended up. Use when the user asks to run presubmit, wants a deep unattended audit of a draft before submission, or needs a math or replication-code audit. The everyday in-session self-audit is paper-review-lite, and refereeing someone else's manuscript is journal-review.
argument-hint: "[path to your draft to review, or describe the setup task]"
---

# Presubmit Activator

A launcher and setup wizard for the [`presubmit`](https://github.com/scdenney/presubmit) Python CLI — the standalone, API-driven adversarial peer-review pipeline that writes a consolidated review report to disk. The review itself happens in the CLI against the Anthropic API (~30 stages, ~$5–10 per full run on a typical manuscript); this skill verifies the install and the key, settles where output lands, launches the run, and reports where the report ended up.

This is for self-audit of your own drafts pre-submission. Peer-reviewing other people's manuscripts goes through the separate `reviews/` workflow with its own agents-based `CLAUDE.md` — not here.

## Setup phase (run once per machine)

Before any per-paper invocation, verify the install and the config. Run only the steps whose check fails.

### Step 1 — Is `presubmit` installed?

```bash
command -v presubmit && presubmit --help | head -3
```

If the usage banner comes back, skip to Step 2. If not, ask the user where they keep cloned repos (that choice becomes `PRESUBMIT_DIR`, used throughout below), then:

```bash
PRESUBMIT_DIR=~/repos/presubmit   # wherever the user keeps clones

# Clone (or update) the repo
git clone https://github.com/scdenney/presubmit "$PRESUBMIT_DIR" \
  || git -C "$PRESUBMIT_DIR" pull

cd "$PRESUBMIT_DIR"

# Create a venv
python3 -m venv .venv
source .venv/bin/activate

# Install — first time pulls marker-pdf + PyTorch, ~5–10 min.
# pyproject.toml pins anthropic>=0.60 directly; verify the resolver honored it:
pip install -e .
pip show anthropic | head -2     # must be >= 0.60; if not: pip install -U 'anthropic>=0.60'
```

Confirm with `"$PRESUBMIT_DIR/.venv/bin/presubmit" --help | head -3`. The CLI lives in the venv: either source the venv each session (`source "$PRESUBMIT_DIR/.venv/bin/activate"`) or invoke the absolute binary path.

Warn the user that the **first PDF conversion** is slow — marker-pdf downloads ~3–5 GB of OCR / layout / table-recognition model weights into its local Hugging Face cache (macOS `~/Library/Caches/datalab/models/`, Linux `~/.cache/datalab/models/`), bandwidth-limited. Subsequent runs reuse the cache.

### Step 2 — Is `ANTHROPIC_API_KEY` set?

```bash
[ -n "$ANTHROPIC_API_KEY" ] && case "$ANTHROPIC_API_KEY" in sk-ant-*) echo "key OK";; *) echo "key set but unexpected prefix: ${ANTHROPIC_API_KEY:0:8}…";; esac
```

If empty, check whether it's defined in `~/.zshrc` but unsourced in the current shell:

```bash
eval "$(grep -E '^export ANTHROPIC_API_KEY=' ~/.zshrc | head -1)" 2>/dev/null && [ -n "$ANTHROPIC_API_KEY" ] && case "$ANTHROPIC_API_KEY" in sk-ant-*) echo "found in .zshrc";; esac
```

If still missing, walk the user through:

1. Generate a key at <https://console.anthropic.com/> → **Settings → API Keys → Create Key**.
2. Add to `~/.zshrc` (or equivalent shell rc), placed **above** any wrapper functions that re-set `ANTHROPIC_API_KEY` to an empty string to route the `claude` CLI to local Ollama models — those would shadow the real key:

   ```bash
   export ANTHROPIC_API_KEY="sk-ant-api03-..."
   ```

3. `source ~/.zshrc` or open a new terminal.
4. Confirm a positive credit balance on the account. presubmit fails fast on credit/billing 400s rather than burning the retry budget — an empty balance halts the run on the first call.

### Step 3 — Where should outputs live?

Read `~/.config/presubmit/config.json` for an existing `output_base`; if the path is writable, use it. Otherwise ask (`AskUserQuestion`) — "Where should presubmit reviews be stored by default?" — offering at least these plus a custom path:

- `~/presubmit-reviews/` — generic, no project-folder assumption
- `~/Documents/presubmit/` — under Documents
- `~/Documents/GitHub/pre-submission/` — for users who keep all repos under `~/Documents/GitHub/`

Write the choice to `~/.config/presubmit/config.json`:

```json
{
  "output_base": "/absolute/path/the/user/picked",
  "saved_at": "ISO 8601 timestamp"
}
```

That config file is the source of truth for this skill. Also *offer* to write `export PRESUBMIT_OUTPUT_BASE=…` to `~/.zshrc` so the bare CLI picks up the same default — ask first, never write to `.zshrc` silently.

## Per-paper run phase

### Step 1 — Slug

Derive a default slug from the input filename: extension and path stripped, lowercased, runs of non-alphanumerics collapsed to single hyphens (underscores preserved), leading/trailing hyphens and underscores trimmed. Target shape is `<lastname>_<year>_<short-title>` — e.g. `Denney_2026_What-Were-They-Thinking.pdf` → `denney_2026_what-were-they-thinking`. Confirm the proposed slug with the user (`AskUserQuestion`); allow override.

### Step 2 — Mode

Ask which run mode (`AskUserQuestion`):

- **Smoke** — `--stop-stage 2.0`. Metadata extraction + Red Team + numbers auditor. ~15–25 min on a 70-page paper, ~$1–2. Useful for verifying setup or catching show-stoppers fast.
- **Standard** — full pipeline. ~30–90 min, ~$2–4 on a 70–80-page paper (a short article of a few thousand words runs well under $2). The default for a real audit.
- **Custom** — ask for additional flags (`--code-dir`, `--math`, `--supp`, `--no-copyedit`, `--no-editor-note`, `--start-stage`, `--stop-stage`, `--skip-size-check`).

Cost depends on which of four model tiers (mechanical/forensic/adversarial/synthesis, mapped to Haiku/Sonnet/Opus/Fable) each stage routes to — see the upstream repo's README "Model tier mapping" section for the full breakdown. These are estimates, not a guarantee. The end-of-run cost report has the real total.

### Step 3 — Construct paths and run

```bash
WORK_DIR="$OUTPUT_BASE/$SLUG/presubmit_run"
mkdir -p "$WORK_DIR"
"$PRESUBMIT_DIR/.venv/bin/presubmit" "$PAPER_PATH" \
  --work-dir "$WORK_DIR" \
  -o "$OUTPUT_BASE/$SLUG/report.txt" \
  $EXTRA_FLAGS
```

Always pass both. `-o / --output` controls the *final report copy* only; without it a stray `report.txt` lands in the invoking directory. Without `--work-dir`, stage outputs go to a temp dir that gets garbage-collected.

Launch with the Bash tool's `run_in_background: true` and stream the log to a file. Tell the user the expected wall time, the `tail -f` path for the live log, and what files to expect in `$WORK_DIR` as stages complete.

### Step 4 — Report when done

1. Confirm exit code 0 and no `FATAL: Claude refused` in the log. (A `--stop-stage` smoke run also exits 0, printing `Stopped at stage N as requested`; judge it by the per-stage files in `$WORK_DIR`, since no consolidated report exists by design.)
2. Locate the consolidated report: `$WORK_DIR/<slug>_*.txt` (presubmit auto-names it `<author_title_uuid>.txt`), with a stable-named copy at the `-o` path.
3. Report wall time, total tokens (input + output across stages, at the end of the log), and the end-of-run dollar total (pricing.csv carries current Claude rates; cross-check the Anthropic console if rates have changed).
4. Offer to open the report and to write a per-paper README.md alongside the work_dir capturing invocation date, flags, models, wall time.

If the run failed:

- **`Messages.create() got an unexpected keyword argument 'thinking'`** — anthropic SDK is < 0.60. Fix: `pip install -U 'anthropic>=0.60'` in the venv.
- **`FATAL: Claude refused the request (likely safety policy)`** — a Red Team prompt tripped Claude's safety filters. The message does not name the stage; find the last `► Executing <stage>` line above it in the log, then locate that stage's prompt under `$PRESUBMIT_DIR/src/presubmit/prompts/`. Soften it to attack the manuscript's claims, not the authors. Re-run; the pipeline is resumable.
- **Marker conversion failure** — surface the specific PipelineError. Common cause: marker-pdf install incomplete; verify `pip show marker-pdf` succeeds in the venv.
- **Out-of-credit** — top up at <https://console.anthropic.com/>, then re-run. The pipeline picks up where it stopped.

## File-naming and organization convention

```
$OUTPUT_BASE/                                            (from config; user-chosen)
└── <slug>/                                              (one folder per paper)
    ├── README.md                                        (offered after the run — never silently written)
    ├── report.txt                                       (stable-named copy of the report, via -o)
    └── presubmit_run/                                   (the --work-dir)
        ├── <author_title_uuid>.txt                     ← THE main consolidated report
        ├── original_source.pdf                          (cached source)
        ├── paper.md                                     (marker conversion of source)
        ├── metadata.json
        ├── pipeline_execution.log
        ├── 00a_metadata.txt … 09c_copyedit.txt          (intermediate per-stage outputs)
        └── 10_latex_body.txt                            (body without LaTeX framing)
```

`<author_title_uuid>.txt` consolidates all stages into one file: header, disclaimer, overview, Editor's Note, Summary (Is It Credible? + Bottom Line), Potential Issues, Future Research, Copyediting, Proofreading. Read it first. The rest are intermediates — though the raw `01a_breaker.txt`, `01b_butcher.txt`, etc. carry unfiltered Red Team findings that are sometimes sharper than the consolidated version.

## When to use this skill vs. `paper-review-lite`

| | `presubmit` (this skill) | `paper-review-lite` (sister skill) |
|---|---|---|
| Where the work happens | Outside Claude Code — Python CLI calls Anthropic API | Inside Claude Code — parallel sub-agents read the paper |
| Cost | Per-token, billed to your API key (~$5–10/run) | Subscription only (no per-token bill) |
| Wall time | 30–90 min unattended | Minutes; you control each pass |
| Depth | 30+ stages: Red Team (Breaker, Butcher, Shredder, Collector, Void) + Blue Team defence + verification cascade + legal pass + copyedit + Writer Mode | ~11 sub-agents: content/argument, numbers, references, DOIs, writing, CONSORT, pre-reg, figures, archive, plus 2 cross-checkers |
| Output | Single consolidated `.txt` deliverable + ~30 intermediate files | Structured pre-submit report in-conversation + `.review-tmp/` scratch files |
| Resumable | Yes — checkpointed per stage to disk | No — single conversation pass |
| Math audit | Yes (`--math`, requires Mathpix) | No |
| Replication-code audit | Yes (`--code-dir`) | Partial (Agent 9 checks archive completeness; doesn't compare claims to code) |
| Refusal risk | Moderate (some Red Team stages adversarial enough to trip safety) | Low (single-pass personas, quote-grounded) |
| When to use | Deep audit before submission; standalone deliverable; math or code audit | Quick in-flow check; routine self-audit; no API spend |

`paper-review-lite` is the everyday tool; `presubmit` is the heavy-artillery final pass before submission.

## Known gotchas (current as of 2026-06)

1. **anthropic SDK version conflict.** presubmit's `pyproject.toml` pins `anthropic>=0.60` directly (core.py's `Messages.create(thinking=…)` needs it), but `marker-pdf 1.10.x` transitively caps anthropic at `<0.47`. pip resolves the conflict by backtracking marker-pdf to an older release, or by warning. After install, check `pip show anthropic marker-pdf`; if anthropic landed below 0.60, force it with `pip install -U 'anthropic>=0.60'` — runtime is unaffected, since presubmit doesn't use marker's optional anthropic-LLM mode.
2. **`use_search=True` is a no-op.** Stage 00a (metadata) silently degrades for published papers needing a citation lookup; fine for unpublished manuscripts.
3. **Older checkouts exit 1 on intentional `--stop-stage` runs.** Current presubmit exits 0 with `Stopped at stage N as requested`; if you see exit 1 with "did not produce a final report" after a smoke run, the install predates the fix — `git pull && pip install -e .`.
