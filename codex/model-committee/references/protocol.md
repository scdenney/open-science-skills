# Model Committee Protocol

## Contents

1. Use-case gate
2. Committee brief
3. Round 1: blind proposals
4. Round 2: cross-critique and revision
5. Round 3: blinded cross-ranking
6. Decision rule
7. Output contract

## 1. Use-case gate

Choose the instrument before calling a model.

| Task shape | Route |
|---|---|
| A fact, calculation, or behavior can be settled by an authoritative source, proof, test, or experiment | Verify directly with one agent |
| Disagreement itself is the measurement and must remain interpretable | `$model-council-voting` with independent members |
| The goal is several creative approaches for user selection | `$diverge` or `$diverge-codex` |
| The specification is fixed and work is primarily execution | One suitable implementation agent |
| One consequential choice is required among defensible alternatives, with shared evidence and an explicit rubric | Model committee |
| Legal, medical, financial, safety-critical, or similarly high-stakes judgment | Committee may advise, but a qualified human decides |

A task qualifies only when all four required conditions hold:

1. **Decision:** one recommendation or plan must be returned.
2. **Contestability:** at least two defensible positions exist before seeing model outputs.
3. **Common evidence:** both members can receive materially the same evidence and constraints.
4. **Evaluability:** criteria can be declared before proposals are read.

Then require at least one value condition:

- different model-family priors are likely to expose a blind spot;
- the decision is costly enough to justify six calls; or
- the user explicitly wants deliberation as an audit trail.

Good use cases:

- architecture, API, data-model, or migration choices with real tradeoffs;
- research design, estimand, identification, robustness, or interpretation decisions;
- manuscript framing, contribution positioning, reviewer-response strategy, or revision planning;
- ambiguous root-cause diagnosis after obvious tests are exhausted;
- prompt, model, evaluation, or agent-workflow design;
- standards, governance, or policy recommendations with documented constraints;
- reconciling two already-developed plans into one executable strategy.

Poor use cases:

- lookups, summaries, translation, formatting, or deterministic transformations;
- mass classification where agreement is a reliability statistic;
- unconstrained brainstorming where no immediate decision is needed;
- tasks too underspecified to define a rubric;
- sensitive inputs that cannot be sent to both providers;
- urgent, low-value work where latency and cost exceed the expected benefit.

## 2. Committee brief

Freeze `brief.md` before round 1. Include:

```markdown
# Committee brief

## Decision required
One sentence naming the decision—not merely the topic.

## Use case
Category and why committee treatment is justified.

## Shared evidence
Facts, file paths, source excerpts, test output, and explicit uncertainties.

## Constraints
Hard requirements, exclusions, time/cost limits, and reversibility.

## Evaluation rubric
| Criterion | Weight | What success means | Disqualifier |
|---|---:|---|---|

## Tie rule
Human adjudication / compatible synthesis / weighted-score winner.

## Required output
Exact granularity and format of the final decision.
```

Weights must total 100. Use equal weights only when there is no principled reason to differ. A hard constraint is a disqualifier, not a low score.

Default tie rule:

1. unanimous ranking wins;
2. otherwise choose the higher aggregate weighted rubric score if the margin exceeds 5% of the maximum possible score;
3. within 5%, synthesize only if both revisions explicitly identify compatible components;
4. otherwise ask the human.

For high-stakes decisions, replace steps 2–4 with human adjudication.

## 3. Round 1: blind proposals

Create two prompt files before launching either call. Give both members the identical brief and this contract:

```text
You are one member of a two-model committee. Work independently. You have not
seen the other member's answer. Propose one decision that best satisfies the
brief; do not list several unranked options.

Return:
1. DECISION — one sentence.
2. REASONING — criterion-by-criterion argument grounded in shared evidence.
3. TRADEOFFS — what this choice gives up.
4. FAILURE TEST — evidence that would make the choice wrong.
5. CONFIDENCE LIMITS — unresolved facts, without a numeric confidence score.

Do not infer absent evidence. Do not appeal to model identity or authority.
```

Reject and rerun malformed responses once. Do not repair substantive reasoning as chair.

## 4. Round 2: cross-critique and revision

Give each member the common brief, both round-1 proposals, and the same contract. Label proposals `Proposal A` and `Proposal B`; do not emphasize authorship.

```text
Deliberate after reading both initial proposals.

Return:
1. STEELMAN PEER — strongest version of the other proposal.
2. CRITIQUE A — strongest evidence-based weakness in Proposal A.
3. CRITIQUE B — strongest evidence-based weakness in Proposal B.
4. REVISED DECISION — one complete candidate decision.
5. CHANGES — what you changed after reading the peer and why.
6. COMPATIBILITY — elements of the two proposals that can be combined without
   violating the brief; write NONE if no principled hybrid exists.
7. RESIDUAL DISAGREEMENT — the remaining factual or value dispute.

Concede valid points. Do not preserve your initial position merely for consistency.
```

The revised decision, not the initial proposal, advances to ranking.

## 5. Round 3: blinded cross-ranking

Extract the two revised decisions into anonymous `Candidate A` and `Candidate B`. Reverse their order between member prompts to reduce order effects. Include the brief and rubric.

```text
Score both candidates independently against the predeclared rubric.

For every criterion, assign each candidate an integer score from 0 to 5 and cite
the specific evidence or requirement supporting that score. A hard-constraint
violation is DISQUALIFIED regardless of total score.

Return:
1. SCORE TABLE — criterion, weight, A score, B score, evidence.
2. DISQUALIFIERS — candidate and violated constraint, or NONE.
3. FORCED RANK — A>B or B>A; no tie.
4. BEST OBJECTION TO YOUR RANK — one sentence.

Judge the candidates, not their presumed authors. Do not use confidence,
eloquence, length, or model identity as a criterion.
```

Normalize candidate labels before aggregation because order is reversed in one prompt.

## 6. Decision rule

Apply in order:

1. Drop any candidate with a verified hard-constraint violation.
2. If both rankings select the same candidate, select it.
3. If rankings split, compute each reviewer's weighted total for each candidate, then sum reviewer totals.
4. If the aggregate margin exceeds the precommitted threshold, select the winner.
5. Otherwise create a hybrid only from mutually compatible elements identified in round 2 and rescore it against hard constraints.
6. If no qualified winner remains, ask the human to resolve the documented fork.

Do not add bonus points for agreement. Do not average away a disqualifier. Do not let the chair's model family vote a third time.

## 7. Output contract

Write `decision.md`:

```markdown
# Committee decision

## Use case and eligibility
## Decision
## Rule applied
## Rubric result
## Why this won
## Changes produced by deliberation
## Dissent and uncertainty
## Failure test
## Next action
```

The final answer must not claim consensus when the rule selected a split-vote winner. Use precise labels: `unanimous`, `weighted-score decision`, `compatible synthesis`, or `human-adjudicated`.
