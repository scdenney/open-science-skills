---
name: journal-review
description: "Draft a referee report on someone else's manuscript for a journal editor, using a claim ledger, five adversarial finders, a Blue Team that tests their evidence in both directions, a Chief Reviewer synthesis, a Tone Guard legal pass, and a quote check. Use when the user has been asked to referee a manuscript; self-audits go to paper-review-lite or presubmit, author responses to referee-response."
---

# Journal Article Peer Review

## Heritage and scope

This is the in-session, Codex-native referee-drafting tool. It produces a **referee report you would send to a journal editor and the authors** — third-party referee work, not the author's own pre-submission audit.

The eight-agent design is adapted from the [`presubmit`](https://github.com/scdenney/presubmit) pipeline (itself a port of `reviewer2` / isitcredible.com, Apache-2.0). Four adversarial finders (Breaker, Butcher, Shredder, Void) come from that lineage; **Situator**, the fifth, is added here because literature placement is typically the weakest element of automated reviews and the single most important judgment a human reviewer brings. Blue Team filters finder errors; Chief Reviewer writes the report; Tone Guard sanitizes for legal risk.

The claim ledger, the two-direction Blue Team, the burden rule, the robustness-sentence check, and the quote check are adapted from the same author's successor suite, [`research_skills`](https://github.com/isitcredible/research_skills) (MIT), whose `review` → `audit-review` → `review-digest` pipeline records claim by claim what a paper's evidence establishes rather than collecting issues by persona. The target-parameter check, the cheap-shot test, the mechanism audit for empirical defences, and the rule against imported premises come from reviewer2's final release (v2.0.0). The replication machinery of `research_skills` (executing the deposit, cell-by-cell reproduction, data forensics) is not ported: referees rarely have a package, and self-audits route the package through `replication-package`.

## Delegation gate

Run the multi-agent path only when the user explicitly invokes `$journal-review` or asks for subagents/parallel reviewers. If the skill loads implicitly, perform the review sequentially in the lead context or ask before spawning agents.

## What this produces

A markdown referee report: **Recommendation** (*Reject* / *Major Revision* / *Minor Revision* / *Accept with minor changes* / *Accept*), **Summary** (the claim and the design, not the critique), **Major Concerns** (3–6 numbered paragraphs, which determine the recommendation), **Additional Concerns** (3–8 shorter items that matter but do not drive the decision), and **Suggestions for Revision** (a coherent revision plan, not a punch list). Confidential comments to the editor are optional and live in a separate file. Full template and length budget in Phase 3.

Not a long exhaustive issue list, and not a takedown.

## Setup (do this yourself before launching agents)

1. Identify a slug for the manuscript: `<first-author-surname>_<short-title>_<submission-id>`. Example: `Kim_divided_views_JAS-26-0243`.
2. Create the working directory: `mkdir -p <reviews-folder>/<slug>/` (ask the user once where reviews should live — e.g. `~/reviews/` — and reuse that convention thereafter).
3. Copy the manuscript PDF into the slug folder as `manuscript.pdf`. If the editor's invitation letter or the user's notes are available, save them as `context.md` in the same folder.
4. Read the manuscript yourself once before writing agent prompts. Determine: empirical or theoretical or qualitative; design family (conjoint, list experiment, observational, RCT, ethnography); whether SI / replication archive exists; rough page count and section structure. This shapes which agents will produce useful output (see "When to skip a finder agent" below).
5. Extract the text once: `pdftotext -layout manuscript.pdf manuscript.txt`. The Phase 5 quote check searches this file.
6. Write the claim ledger, `<slug>/claims.md`. Go through the title, abstract, introduction, and conclusion sentence by sentence and give each load-bearing claim a row: `ID | claim (verbatim) | page | centrality`. Centrality is `headline` (the title, the abstract, or a contribution the introduction or conclusion states), `supporting` (an estimate, test, robustness check, or mechanism claim a headline rests on), or `peripheral` (an implication, interpretation, or policy claim the paper does not test). A sentence that makes two claims gets two rows. Every agent receives this file as `{{CLAIMS}}`, so each issue is an issue with something the paper asserts.

## Phase 1 — Five finder agents in two waves

**Runtime constraint.** Codex's subagent tool reports 4 concurrency slots *including the lead*, so at most 3 subagents run at once no matter how many are queued. Five finders therefore cannot be one parallel batch. Run them in two waves:

- **Wave A (3 slots):** Breaker, Butcher, Shredder — the three that read the manuscript's own machinery and do not depend on each other.
- **Wave B (2 slots):** Void, Situator — launched once Wave A's agents have written their files and released their slots. Both are absence-and-placement judgments, so nothing is lost by their running second; do not pass them Wave A's findings, since blind finders are the point.

Each agent's prompt is the role block below, with `{{MANUSCRIPT}}` replaced by the manuscript path and `{{CONTEXT}}` replaced by the target-journal name plus any editor's-letter excerpts and reviewer notes. Each agent writes its raw findings to `<slug>/agent_<n>_<name>.md`.

If a finder is skipped under "When to skip a finder agent" below, refill the wave rather than leaving a slot idle — the wave split is a capacity constraint, not a grouping the roles depend on.

### Agent 1 — The Breaker

> You are **The Breaker**. You interrogate the fundamental validity of the attached manuscript: its theoretical basis and research design. Other reviewers scrutinize evidence and execution; your role is deeper — examine the intellectual foundations (premises, frameworks, questions chosen) and ask whether the entire argumentative structure is sound.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
> Claim ledger: {{CLAIMS}}
>
> **Foundations.** Is the theoretical framework contested and is this acknowledged? Are disputed premises treated as obvious? Does the framework predetermine the findings? Would a scholar from a competing tradition reject the framing entirely? Is this the right method for the question, or the right question for the method? Is there slippage between the construct (what we care about) and the operationalization (what was measured)? If a causal identification strategy is named (DiD, RDD, IV, quasi-experiment), does the actual specification satisfy its requirements — if the label were removed, how strong would the evidence look? Does the proposed mechanism operate *within* the boundaries that define exposure and comparison groups? Does the design recover the parameter the conclusions invoke? An estimate of one quantity (an intent-to-treat effect, a local effect at a cutoff, a reduced form, an AMCE) offered as evidence for another (the effect of treatment received, a population average, a structural parameter, majority preference) is a gap even when the estimate itself is sound.
>
> **Argument.** Circular reasoning, non sequiturs, equivocation, false dichotomies, scope creep, inconsistent hedging (confident in abstract, cautious in results), bait-and-switch, straw-manning of alternatives.
>
> **Extrapolation.** If coefficients are multiplied into population-level claims, do the study's own auxiliary analyses (dose-response, heterogeneity) contradict the required assumptions?
>
> **So what?** Even if answered definitively, would the answer matter? Is the plausible effect size large enough to be worth knowing about?
>
> **Steelman first.** Before attacking, write one sentence stating the authors' position in its strongest form. Attack what is actually there, not a misreading.
>
> Output 5–10 issues in this format:
> ```
> ISSUE: <short title>
> CLAIMS: <claim-ledger IDs it bears on, or NEW: <verbatim claim, page> for a claim the ledger missed>
> DESCRIPTION: <1–3 sentences. Explain your logic.>
> QUOTE: <verbatim span from the manuscript, with page>
> ```
> Do not grade severity; the Chief Reviewer weighs issues after the Blue Team has ruled on the evidence. Quality over quantity. **Guards:** No figure interpretation. Critique the work, not the author. Do not use "fabricated", "deceptive", "deliberately", "lied".

### Agent 2 — The Butcher

> You are **The Butcher**. You dissect the empirical machinery of the attached manuscript: the design choices, the measures, the analytical decisions. You ask not just whether it was executed cleanly, but whether it was capable of answering the question posed.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
> Claim ledger: {{CLAIMS}}
>
> **Design.** Method-question fit. Construct validity. Adjustment-induced confounding (could weights / matching / IV introduce rather than remove bias?). Boundary-mechanism alignment. Design-label verification. Streetlight problem. Null-result distinguishability. Model dependence.
>
> **Results integrity.** Internal consistency (do tables match text and reported tests?). Specification sensitivity. Outlier / influence dependence. Robustness checks (do they test anything threatening?).
>
> **Claim alignment.** Does the abstract claim what the results actually show? Selective emphasis (nulls buried while one coefficient does all the work). Causal language from correlational designs. Generalizing from narrow samples to broad populations. Confidence intervals that overlap "no meaningful effect."
>
> **Practical significance.** Translate headline coefficients into real-world units. Statistical vs. practical significance with large n. Variance explained. Relative vs. absolute effects. Benchmark comparisons.
>
> **Robustness sentences.** Find every sentence of the form "results are robust / similar / unchanged / not sensitive to X". For each, open the exhibit it cites and check every outcome the sentence covers. Classify it `SUPPORTED`, `QUALIFIED` (holds for some outcomes or columns only), `CONTRADICTED` (a cited cell changes sign, loses significance at the paper's own threshold, or moves materially), or `UNRESOLVED` (the cited exhibit is missing or does not show the comparison). List them all under `ROBUSTNESS SENTENCES:` before your issues, supported ones included, or write `NONE FOUND` with the search terms you used. Each `QUALIFIED` or `CONTRADICTED` sentence is also an issue.
>
> **Steelman first.** State the authors' methodological choice in its strongest form before attacking. Distinguish design from execution.
>
> Output 5–10 issues in the same format as The Breaker. **Guards:** No figure interpretation. Verify table readings coordinate-style: list the exact column headers, trace each datapoint row → column, and check for narrative inversion (text says "A high, B low" but table shows reverse).

### Agent 3 — The Shredder

> You are **The Shredder**. Forensic procedural auditor. You verify what was claimed to have been done is actually documented. You work only with what's in the PDF — no external lookups. If it's not documented, that itself is a finding.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
> Claim ledger: {{CLAIMS}}
>
> **Internal consistency.** Sample-size arithmetic (n in methods vs. n in results vs. n in tables; exclusions accounted for). Timeline logic. Methods–results alignment. Statistical consistency (df ↔ sample size; reported test statistics yield reported p-values; CIs match point estimates and SEs). Cross-reference integrity.
>
> **Procedural claims vs. documentation.** Blinding/masking actually described? Randomization method specified? Pre-registration deviations acknowledged? Independence claims. Ethical approvals.
>
> **Model specification transparency.** Functional-form justification. Parameter sources. Calibration targets. Degrees-of-freedom accounting. Identification strategy clearly stated. Specification-plausibility check.
>
> **Sensitivity and validation.** Did they vary parameters that actually matter? In-sample fit only or genuine out-of-sample? Assumption testing or assertion?
>
> **Documentation gaps.** Unreported standard procedures. Missing justifications. Absent robustness checks where conventionally expected. Undocumented exclusions. Reproducibility information.
>
> Output 5–10 issues in the same format. **Guards:** "Not documented" ≠ "did not happen" — be precise.

### Agent 4 — The Void

> You are **The Void**. You analyze what isn't in the attached manuscript and ask why. Other reviewers critique what is written; you identify standard or decisive evidence that is conspicuously absent.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
> Claim ledger: {{CLAIMS}}
>
> **Core principle — "the dog that didn't bark."** When standard evidence is missing, the often-correct interpretation is that it was omitted because it was inconvenient. Do not be captured by the authors' framing. Authors often preempt criticism by acknowledging limitations that make them look conservative ("if anything, we underestimate..."); ignore this framing. Your job is to find omissions that would make the findings *weaker, smaller, or disappear entirely* — not omissions that would make the "true effect" even larger.
>
> Check these voids and flag significant ones: confound, reverse causation, robustness, selection, measurement, false conservatism, effect-size, framework, method, spillover, boundary, baseline, alternative-explanation, benchmark, base-rate.
>
> Before flagging something as missing, check appendices, supplementary materials, and footnotes. An omission you missed is not an omission they made. Distinguish *standard omission* (conventionally expected but not provided), *strategic omission* (would threaten the conclusions), *innocent omission* (not relevant). Focus on the first two and say which.
>
> Output 5–10 issues in the same format. **Guards:** Absence ≠ falsity.

### Agent 5 — The Situator

> You are **The Situator**. Other agents scrutinize methods and logic. Your job is different: does this manuscript actually advance on existing work, or is it re-stating what the literature already shows?
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
> Claim ledger: {{CLAIMS}}
>
> **This is the most important assessment for a disciplinary journal.** A paper with a clean design but no added knowledge should not be published; a paper with messy execution but a genuinely novel contribution might still warrant revision.
>
> Steps:
>
> 1. Read the introduction and literature review carefully. List the specific prior works the authors cite as closest to their contribution. Note where the authors claim their "gap" or "contribution."
> 2. Evaluate the gap claim. For each prior work cited: does the authors' summary match what that work actually argues or finds? Does the claimed distinction from that work survive scrutiny?
> 3. Check your own knowledge of the field. Are there adjacent papers (published 2015–present) that the authors do not cite but that substantially overlap with the contribution? Name them with first-author + year + venue. If you are not confident about the venue, say so — do not invent.
> 4. Identify the novel contribution. Write one sentence stating precisely what this manuscript adds to the literature that was not already known. If you cannot produce that sentence honestly, say so.
> 5. Characterize the contribution type: *theoretical advance*, *empirical advance* (new data / identification / decisive test), *replication or extension* (valuable but should be framed as such), *incremental* (variant with no clear added knowledge), or *redundant* (already established in the cited literature).
>
> Output:
> ```
> CLOSEST PRIOR WORKS (as cited by authors):
> - <citation> — <what it actually argues/finds> — <does authors' summary match?>
>
> POTENTIALLY MISSING PRIOR WORKS:
> - <citation with confidence note> — <why relevant>
>
> CLAIMED GAP: <quote or paraphrase>
> GAP VERDICT: <holds / partly holds / does not hold — with one-sentence reason>
>
> NOVEL CONTRIBUTION (one sentence): <...>
> CONTRIBUTION TYPE: <one of the five>
>
> ISSUES (same format as other agents, for the review): <...>
> ```
>
> **Guards.** Do not invent citations. Do not assert specific factual details (years, geographic coverage, variables included/excluded) about external sources unless you are highly confident. If in doubt, phrase as "appears to overlap with..." and note the uncertainty.

### When to skip a finder agent

- **Theory or conceptual paper** — skip the Shredder; lean on Breaker and Situator. Adjust the report template to omit empirical-machinery concerns.
- **Pure ethnography or interpretive qualitative work** — Butcher and Void checklists assume quantitative social science. Use as scaffolding only; expect to write more of the report yourself.
- **Outside your expertise** — the Situator cannot replace field knowledge. If you do not know the literature, decline the review rather than running this skill.

## Phase 2 — Blue Team filter

Spawn after both waves have finished and all five finder files exist. Blue Team runs alone — it needs every finder's output, so it cannot share a wave with any of them.

> You are the **Blue Team**. You test the finders' evidence in both directions: where they err against the authors, and where they err in the authors' favour. A filter that only defends the authors removes valid attacks along with invalid ones. Ruling that a sound issue stands is as useful as ruling a bad one out.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
> Claim ledger: {{CLAIMS}}
> Finder outputs: {{FINDER_OUTPUTS}}
>
> **Against the authors.** Classify each issue:
> - **Type A — Finder misread.** Critique depends on a misread (misquoted number, misinterpreted regression, confused interaction with main effect, ignored log transformation, mixed coefficients across specifications, imputed factual detail about an external source the manuscript does not state). *Most important to flag.* The most damaging misread is the cheap shot: an attack the manuscript's own definitions, stated conditions, or wording deflect in one line. Ask of every issue whether it would survive the authors pointing at their own text. Restate the issue on the correct reading; it drops only if no concern survives that reading. A restatement may rest only on premises the manuscript establishes: if the concern survives only with a premise you supply (a reinterpretation of one of its quantities, a claim that some method is "standard", an inference the paper does not license), it falls.
> - **Type B — Acknowledged.** The manuscript itself explicitly acknowledges this as a limitation and addresses it (in a robustness check, a caveat, or a footnote). Mentioning is not acknowledging — the text must flag it as a problem for its own argument. Quote the acknowledgement.
> - **Type C — Clerical.** Presentation issues. Apply charity.
> - **Type D — Structural.** Misinterpreted regression coefficients, wrong functional forms, mathematical contradictions in the model's own terms. Cannot be explained away.
> - **Type E — Visual evidence.** Issue depends on interpreting a figure or extracting a data point from inside a plot. Dismiss.
> - **Type F — Feature not bug.** The "issue" is intrinsic to the argument; the finder misunderstood.
> - **Type G — Other / no plausible defense.** Issue appears genuine.
> - **Type H — Empirically addressed.** The manuscript runs a test that bears on the concern (a robustness check, placebo, alternative specification or sample, formal test) without necessarily acknowledging it as a limitation. Search the robustness sections and the whole appendix before ruling. Give the test with its label, its result with numbers, and the link to the specific mechanism the concern names. A test often closes an adjacent threat and leaves the named one open; say so when it does, and name the residual.
>
> **In the authors' favour.** Then check what the finders let through, and enter each as an `ADD` item in the finder format: evidence for a claim held to a lower bar than evidence against it (a balance or placebo test that could not have failed, an estimate called precise without the inference level the design requires); an uninformative estimate read as support; a fault filed against a peripheral sentence when it bears on a headline claim, or split across issues so that none carries it; a rescue elsewhere in the paper that carries the same defect; a `headline` claim that no finder tested.
>
> **Claim rulings.** For every `headline` and `supporting` row of the claim ledger, give a provisional ruling: `holds` (stands as printed), `narrower` (stands only in a narrower scope, size, population, or precision than printed, which the paper does not flag), or `not established` (its evidence does not deliver it, whether or not anything refutes it). Give the kernel that survives and what the claim asserts beyond it.
>
> Output for each issue: `ISSUE n: <title>; TYPE: <A–H>; DEFENSE: <with quote if A/B/F; test, result and mechanism link if H>; RULING: KEEP / KEEP-RESTATED: <corrected wording> / DROP`. Keep G and strong D; restate an A whose concern survives; drop E, F, a cleanly acknowledged B, an H whose test closes the named mechanism with no material residual, and an A with nothing left. Then the `ADD` items. Then the claim rulings as a table, `ID | holds | kernel | not established | issues it rests on`. **Rules:** Rule on evidence, never on severity. Don't introduce anything factually incorrect. Justify "standard" claims (sometimes a low standard *is* the problem). Explain "conservative" logic.

## Phase 3 — Chief Reviewer synthesis

Spawn after Blue Team has written its file.

> You are the **Chief Reviewer**. You write the final referee report for the attached manuscript.
>
> Manuscript: {{MANUSCRIPT}}
> Target journal and reviewer notes: {{CONTEXT}}
> Claim ledger: {{CLAIMS}}
> Finder outputs: {{FINDER_OUTPUTS}}
> Blue Team triage: {{BLUE_TEAM}}
>
> **Your job is judgment, not compilation.**
>
> 1. **Decide a recommendation** using the rubric in the "Recommendation rubric" section below. Be honest.
> 2. **Consolidate first, then choose.** If two or more finder agents flagged the same underlying issue (Breaker on framing + Butcher on overclaiming + Void on missing alternatives can all describe one critique), merge them into one Major Concern with the strongest framing and best supporting quote. The reader should not see the same complaint restated three times as three separate concerns — that's a parallel-finder artifact and undermines the report's credibility.
> 3. **Choose 3–6 Major Concerns** that determine the recommendation. Weigh issues by the claims they reach: one that leaves a `headline` claim not established comes before one that narrows it, and both before issues that touch only `supporting` or `peripheral` claims. Demote an issue the authors could dismiss by pointing at their own text, and deepen the ones the headline argument rests on. Prefer issues that survived Blue Team filtering and cannot be answered by a footnote. Each Major Concern says which claim it bears on, whether that claim is narrower or not established, and what survives.
> 4. **Choose 3–8 Additional Concerns** that are real but not decisive.
> 5. **Write Suggestions for Revision as a coherent plan, not a punch list.** Where possible, identify the single addition (often one analysis, one robustness check, one figure) that would convert the strongest Major Concern into a supporting result rather than a refutation. Distinguish suggestions that require new analysis from those that require only rewriting. Where two Major Concerns are coupled (fixing one resolves the other), say so explicitly.
> 6. **Account for every kept issue** in `<slug>/coverage.md`. Open it with the final claim ledger, `ID | centrality | holds | kernel`, departing from the Blue Team's ruling only with a stated reason. Then one line per KEEP, KEEP-RESTATED, or ADD item: `<issue> → Major n`, `→ Additional`, `→ Suggestions only`, or `— excluded: <reason>`. A `headline` claim ruled not established that reaches no Major Concern needs its reason written there.
>
> **Output structure:**
> ```markdown
> # Reviewer Report
>
> **Manuscript:** <title>
> **Journal:** <target>
>
> **Recommendation:** <Reject | Major Revision | Minor Revision | Accept with minor changes | Accept>
>
> ---
>
> ## Summary
>
> <One tight paragraph (~150 words). What is the paper, what does it claim, what is the design. Direct quotes sparingly. Do not editorialize — save that for Major Concerns. Do not list findings.>
>
> ## Major Concerns
>
> ### 1. <short assertive heading>
>
> <One paragraph (~120–200 words). Open with the concern in one sentence. Then: what the paper claims or does, why it is a problem for the headline claims, brief citation (page or table number, with direct quote if decisive). State the critique in your own voice.>
>
> ### 2. ...
>
> [3–6 total]
>
> ## Additional Concerns
>
> - **<short label>:** <1–2 sentences, concrete.>
>
> [3–8 total]
>
> ## Suggestions for Revision
>
> 1. <Concrete action tied to a Major Concern.>
> ```
>
> **Voice.** Senior peer. Firm where the evidence warrants, fair everywhere. Hedge appropriately ("suggests," "appears," "raises questions about") for interpretive claims; do not hedge arithmetic errors (state them directly). Cite with author surnames only (Smith; Smith and Jones; Smith et al.). Page numbers with "p." / "pp." at sentence end.
>
> **Hard rules:**
> - No bullet points in Summary or Major Concerns prose — paragraphs only. Additional Concerns and Suggestions may be bulleted or numbered.
> - Only use bold for issue headings, not inside prose.
> - If the paper acknowledges a limitation and partly addresses it, say so.
> - Do not refer to the agents, the workflow, or "potential issues" — the report must be self-contained.
> - Do not impute intent. Never write "fabricated," "lied," "fraud," "deceptive," "dishonest," "deliberately."
> - The burden rule in "Quality rails" governs the wording: "the evidence does not establish X", never "X is false" unless an estimate excludes X.
> - Total length: 1,200–2,000 words. Shorter is better than longer if the critique is tight.

## Phase 4 — Tone Guard sanitization

Spawn on the Chief Reviewer's draft.

> You are the **Tone Guard**. Sanitize the draft referee report for language that could be defamatory, imputes intent, or attacks character rather than work.
>
> Draft report: {{DRAFT_REPORT}}
>
> Flag and rewrite sentences that cross these lines:
> 1. **Imputed intent.** "Conveniently," "designed to," "strategy to," "cherry-picked to," "p-hacked," "hidden," "buried," "obscured," "concealed," "glossed over," "smuggled." Fix: describe outcome or location, not intent. ("The exclusion *risks* inflating significance.")
> 2. **Fraud accusations.** "Manipulated," "fabricated," "lied," "dishonest," "misconduct," "fraudulent," "falsified." Fix: describe the discrepancy. ("The reported data could not be reconciled with the stated methodology.")
> 3. **Competence attacks.** "Incompetent," "lazy," "clueless," "amateurish," "careless," "sloppy," "shoddy," "slapdash," "bogus." Fix: attack the artifact, not the architect.
> 4. **Unsubstantiated absolutes.** "Proves," "demonstrates misconduct," "clearly shows bad faith" applied to interpretation. Fix: probabilistic language.
>
> **Exception.** Arithmetic errors stated directly: "The stated 131% increase is arithmetically incorrect; the actual increase is 189%."
>
> Output the sanitized report in full, with a short HTML-comment log at the bottom listing each change: `<!-- Changed "X" → "Y" (imputed intent). -->`. If nothing changed, end with `<!-- No issues found. -->`.

After reviewing the change log, **delete the HTML comments from `referee_report.md`** — that file goes to the editor and authors.

## Phase 5 — Strip AI tells from the prose

After Tone Guard the report is legally clean but may still read as machine-drafted. Two routes:

- **If the user has an academic prose linter installed** (Steven's `$sci-edit` at `~/.claude/skills/sci-edit/`, or any equivalent), run it on `<slug>/referee_report.md` and apply its suggestions to the Major Concerns paragraphs first; those are what the editor and authors read.
- **Otherwise apply this inline pass yourself** and say in the final summary that no external linter ran. Read the Major Concerns and Suggestions paragraphs once each and fix: hedge stacks (keep one hedge per claim); negative parallelism ("not X but Y") and triadic lists used for rhythm rather than content; em dashes (replace with a period or a comma); colons and semicolons where a period would do; sentence-initial connectives (Moreover, Furthermore, Therefore, Notably); template phrases ("it is worth noting", "this raises the question", "the real question is"); significance inflation (crucial, critical, pivotal, underscore, delve, multifaceted, robust used as praise); synonym cycling of a key term; and any sentence that describes the paper instead of stating a concern. Keep the referee's claims, page citations, and quoted passages untouched.

Then run the quote check, which finds every quoted span of 20 or more characters in the report in the manuscript text (an elided quote is checked part by part):

```bash
python3 - <slug>/referee_report.md <slug>/manuscript.txt <<'PY'
import re, sys, unicodedata
def norm(s):
    s = unicodedata.normalize('NFKC', s).replace('\u00ad', '').replace('-\n', '')
    s = re.sub(r'[\u2018\u2019]', "'", s)
    return re.sub(r'\s+', ' ', s).lower()
report, text = (open(p, encoding='utf-8').read() for p in sys.argv[1:3])
text = norm(text)
quotes = re.findall(r'["\u201c]([^"\u201d]{20,}?)["\u201d]', report)
missing = [q for q in quotes
           if any(norm(part).strip(' .,;:') not in text
                  for part in re.split(r'\.\.\.|\u2026|\[\.\.\.\]', q) if part.strip())]
print(f'{len(quotes) - len(missing)}/{len(quotes)} quotes found verbatim')
for q in missing: print('NOT FOUND:', q)
PY
```

A `NOT FOUND` line is either a paraphrase presented as a quotation (requote from the page or drop the quotation marks) or extraction noise such as a split hyphenation or a table cell (check the page). Resolve every one before the report goes out.

Either route leaves the report in the reviewer's own measured register: short declarative sentences, one concern per paragraph, no rhetorical questions.
## Phase 6 — Optional confidential editor note

After the main report is final, ask the user whether to also generate the confidential editor note. If yes, single-pass:

> You are writing confidential comments to the editor for {{MANUSCRIPT}} at {{CONTEXT}}. The referee report to the authors is attached. Produce a 100–200 word note covering: (1) honest overall assessment of the paper's suitability for this venue, (2) anything you chose not to say to the authors but the editor should know, (3) any conflict of interest or gaps in your expertise. Avoid repeating the referee report. Do not impute intent. Do not include anything you would not be comfortable with the authors eventually seeing if leaked.

Save as `<slug>/editor_confidential.md`.

## Recommendation rubric

- **Reject.** At least one of: (a) no identifiable novel contribution (Situator verdict: redundant), (b) a critical design flaw that no revision can fix without a new study, (c) the headline claims are not established, and the kernel that survives would remove the paper's reason for existence.
- **Major Revision.** At least two major concerns of Type G (no plausible defense), OR a single critical issue that is fixable (e.g., misidentified identification strategy that can be honestly re-labeled, a core robustness check that is missing, a literature placement problem that requires honest reframing). The paper could plausibly become acceptable after substantive work.
- **Minor Revision.** All major concerns are fixable with additional analysis or rewriting — no new data collection, no restructuring of the argument, and no `headline` claim is left not established. Situator verdict is at least empirical advance or replication/extension honestly framed.
- **Accept with minor changes.** Only polish-level concerns remain (exposition, additional robustness for reassurance, small table fixes).
- **Accept.** Rare. No concerns of consequence.

**Reservations about resubmission.** If you recommend Major Revision but suspect the paper may not be salvageable even with effort, state this explicitly: "Major Revision (with reservations about resubmission)." Fair to authors and to the editor.

## Quality rails (apply to every agent)

- **The burden is the paper's, and a test must be able to count.** The strongest critique is that the evidence does not establish a claim; never assert the opposite claim. Write that a result "disappears", "fails", or is "refuted" only when an estimate excludes the paper's figure. An interval containing both zero and the paper's estimate is uninformative: say what the data cannot tell apart, with the interval. A null is informative only for the range it excludes. The same bar applies in the authors' favour: a balance, placebo, or robustness test supports a claim only if it could have detected the violation it is meant to rule out (an equivalence test, not a failure to reject), and an estimate called precise or robust is held to the inference level the design requires.
- **No figure interpretation.** No issue, claim, or citation can be based on visually reading a figure or extracting a data point from inside one. Use only text, tables, and figure captions. (LLMs systematically misread plots.)
- **The black-box rule for external sources.** You can only see what the manuscript says about a cited work. Do not assert specific factual attributes (years, geographic coverage, variables included/excluded, numerical values, frequencies, procedures) about an external source unless the manuscript itself states them. Phrase uncertainty openly.
- **OCR awareness.** If something looks wildly inconsistent with the surrounding text (a coefficient with the wrong sign, garbled number, implausible year), treat as a possible OCR/PDF-extraction artifact. Note the uncertainty rather than building the critique on it.
- **Human in the loop.** Chief Reviewer's output is a *draft*. The user reads, cross-checks every quoted passage against the PDF, edits freely before sending. Agents produce candidates; the user produces the report.

## Output checklist (last-mile, before the user sends)

- [ ] Quote check run and every `NOT FOUND` resolved against the page. Agents occasionally paraphrase as though quoting.
- [ ] `coverage.md` accounts for every kept issue, and each Major Concern names the claim it bears on.
- [ ] Tone Guard's HTML-comment change log deleted from `referee_report.md`.
- [ ] Every page citation correct, and given as the printed page number rather than the PDF viewer's page index (they differ whenever front matter is unnumbered). Agents sometimes cite the wrong page.
- [ ] Summary describes the paper, not the critique. Recognizable to the authors as a fair characterization.
- [ ] Major Concerns ordered by importance, not by the order agents produced them.
- [ ] Additional Concerns do not duplicate Major Concerns at lower volume.
- [ ] Suggestions for Revision map 1:1 onto Major Concerns where possible. An unmapped Major Concern is either not major, or the suggestion is missing.
- [ ] Recommendation consistent with the body. A Reject recommendation should not be followed by "fix X and Y" suggestions.
- [ ] Phase 5 tell-removal applied to Major Concerns prose at minimum (external linter or the inline pass).

## File layout

```
<reviews-folder>/<slug>/
├── manuscript.pdf
├── manuscript.txt                  (pdftotext extract, read by the quote check)
├── claims.md                       (claim ledger, written in Setup)
├── context.md                      (target journal, editor's letter, your notes — optional)
├── agent_1_breaker.md
├── agent_2_butcher.md
├── agent_3_shredder.md
├── agent_4_void.md
├── agent_5_situator.md
├── agent_6_blue_team.md
├── referee_report_draft.md         (Chief Reviewer output)
├── coverage.md                     (final claim ledger + disposition of every kept issue)
├── referee_report.md               (after Tone Guard + Phase 5 — this is what you send)
└── editor_confidential.md          (optional, never sent to authors)
```

## When NOT to use this skill

- **Self-audit of your own draft.** Use `$paper-review-lite` or the heavier external `presubmit` CLI.
- **Papers outside your expertise, or paper types the finders do not fit.** See "When to skip a finder agent" above; for a literature you do not know, decline the review.
- **Conflicts.** If you know the authors personally, sit on a committee with them, or have a citation/funding relationship, the workflow cannot sanitize that.
