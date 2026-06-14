---
name: fact-check
description: Fact-check a manuscript's claims against the cited sources themselves. Locate each source's knowledge-base Markdown file and verify the in-text claim is actually supported. Runs citation-check first, then audits claim support, overclaiming, direction, scope, and misattribution.
argument-hint: "[path to manuscript + bibliography; point to the project's sources/ or knowledge_base/ directory if non-standard]"
---

# Claim–Source Fact Checker

## Heritage and scope

This is an original Open Science Skills workflow. It extends `citation-check` (which verifies a citation *exists*, resolves, and is formatted) to the next question: does the cited *source* actually support the *claim* it is attached to? It checks claims against the project's **per-source Markdown knowledge base** — the files produced by `process-source`, where each source is converted or summarized to `sources/md/<author>-<year>-<slug>.md`. This is local-source verification, not open-web fact-checking: it audits whether a manuscript's sentences are backed by the documents the author has actually read and filed. Run once a draft has citations and a populated knowledge base.

## Instructions

### 1. Orient before checking

- **Manuscript source:** LaTeX, Markdown, Word/PDF text, or pasted prose with citations or footnotes.
- **Bibliography:** `.bib`, CSL JSON, or reference list — used to resolve cite keys to author-year-title so source files can be found.
- **Knowledge base:** the project's per-source Markdown directory. Search in order: `sources/md/`, `knowledge_base/md/`, `sources/`, `knowledge_base/`, then any chapter-local `*/sources/`. Also read any index or crosswalk file (`sources/inventory.md`, `notes/source_map.md`, `*source*crosswalk*`, `*source*matrix*`) that maps bib keys or titles to files.
- If no knowledge base exists, say so up front. This skill checks claims against *local* source files; without them, every claim falls to `NEEDS SOURCE` and the right move is to run `process-source` first, not to guess from memory.
- **Scope:** whole manuscript, one section, the literature review/theory sections, or a supplied list of claims.

### 2. Run citation-check first (always)

Before judging support, run the `citation-check` skill on the same inputs and consume its report. A claim cannot be evaluated against a source that is missing, fabricated, or mis-keyed. Carry its findings forward: any `LIKELY FABRICATED`, `DOI RESOLVES TO DIFFERENT WORK`, or in-text/reference parity break makes the dependent claim `UNVERIFIABLE — citation problem`, not a clean support check. Do not silently repeat citation-check's work; cite its result and build on it.

### 3. Build the claim inventory

For each in-text citation, parenthetical, narrative cite, or footnote that attaches a source to a *substantive* statement, record:

- the **claim** — the exact sentence or clause the citation backs;
- the **cite key(s)** / author-year;
- the **claim type** — empirical result, descriptive fact, definition/concept, method precedent, theoretical position, or direct quotation;
- the **asserted strength** — the verb does work: "shows" / "demonstrates" / "proves" claim more than "suggests" / "is consistent with" / "see".

Skip pure background or "see also" citations unless they carry a checkable assertion. For multi-source claims, check each source's contribution separately — a claim can be supported by one cited work and not another.

### 4. Locate each source's Markdown file

Resolve bib key to author + year + title, then find the matching knowledge-base file:

- Match on `author(s)-year` plus a title slug. Naming varies across projects (`hyphen-separated` or `underscore_separated`; `-and-` between co-authors; first-author-only vs. all authors). Be tolerant of diacritics, name particles (`de`, `van`, `von`), and short vs. full titles.
- Prefer an explicit crosswalk/inventory entry when one exists over fuzzy filename matching.
- These files are frequently **summaries or PDF→Markdown conversions, not full text.** Note which: a faithful conversion can adjudicate fine-grained claims; a condensed summary may legitimately omit the detail a claim rests on.
- Record one of `FOUND` (with path), `AMBIGUOUS` (more than one candidate — list them, do not guess), or `NOT IN KB`.

### 5. Verify claim support

Read the located source Markdown and judge whether it supports the *specific* claim. Classify each:

- `SUPPORTED` — the source states or directly entails the claim. Quote the supporting passage.
- `PARTIALLY SUPPORTED` — the source supports a weaker or narrower version. Name the gap (scope, population, magnitude, hedging).
- `UNSUPPORTED` — the source does not contain the claim; the passage that should support it is absent.
- `CONTRADICTED` — the source reports the opposite or a materially different result (wrong direction, wrong sign, wrong magnitude).
- `MISATTRIBUTED` — the claim is real but belongs to a different work than the one cited.
- `SOURCE INSUFFICIENT` — the Markdown is a summary that does not carry enough detail to adjudicate; name what to check in the original PDF.
- `NOT IN KB` / `UNVERIFIABLE — citation problem` — carried from steps 2 and 4.

For every `SUPPORTED`, `PARTIALLY SUPPORTED`, or `CONTRADICTED` verdict, include a **verbatim quote** from the source (with section/page if the file carries them). Never assert support from memory, topical overlap, or plausibility.

Actively watch for:

- **Overclaiming** — source hedges ("may", "in this sample"), manuscript asserts a general law.
- **Direction errors** — source finds a null or opposite effect from what the sentence claims.
- **Scope creep** — a single-country, single-period, or single-population source cited for a universal claim.
- **Citation stuffing** — a source piled onto a claim it does not actually address.
- **Stale quantitative values** — numbers, point estimates, or sample sizes that do not match the source.
- **Definitional drift** — a concept attributed to a source that defines or uses it differently.

### 6. Do not over-flag

- A faithful summary that simply omits a detail is `SOURCE INSUFFICIENT`, not `UNSUPPORTED`.
- Background and framing citations are not evidentiary claims; do not demand data from them.
- Theory/position citations are supported when the source advances that position, even with no data.
- A missing source Markdown is an **infrastructure gap** (`NOT IN KB` → run `process-source`), not evidence of fabrication. Keep "the source doesn't support the claim" strictly separate from "I couldn't find the source."

## Output

Produce a `Fact-Check Report`:

```
# Fact-Check Report

Scope: <files/sections checked>
Knowledge base: <dir(s) searched> · sources matched: <n>/<total cited>
citation-check: <ran? key carry-forward findings>
Summary: <N contradicted, N unsupported, N partial, N supported, N not-in-KB, N unverifiable>

## Contradicted / Unsupported (blocking)
| Location | Claim (short) | Cite key | Verdict | Source passage or "absent" | Suggested fix |

## Partially supported / Overclaim (recommended)
| Location | Claim | Cite key | Gap | Source passage | Suggested rewording |

## Source not in knowledge base
| Cite key | Author-year | Why unresolved | Action (process-source / locate file) |

## Supported (spot-check log)
| Location | Claim | Cite key | Source passage |
```

Severity:

- **Blocking:** a decisive or headline claim is `CONTRADICTED` or `UNSUPPORTED`; a reported quantitative result does not match the source; a citation-check failure that invalidates the claim.
- **Recommended:** overclaiming or partial support fixable by rewording or rescoping; misattribution where the correct source is known.
- **Minor:** a background citation that could be tightened; a summary-only source worth re-checking against its PDF before submission.

## Quality checks

- [ ] `citation-check` was run first and its findings were carried into the claim verdicts.
- [ ] Every SUPPORTED / PARTIAL / CONTRADICTED verdict quotes a verbatim source passage, not a paraphrase from memory.
- [ ] "Source not in knowledge base" was kept separate from "source does not support the claim."
- [ ] Summary-only sources were labeled SOURCE INSUFFICIENT rather than UNSUPPORTED.
- [ ] Claim direction, magnitude, scope, and hedging were checked — not just topical overlap.
- [ ] Background and framing citations were not treated as evidentiary claims.
- [ ] No claim was marked supported on plausibility alone.
