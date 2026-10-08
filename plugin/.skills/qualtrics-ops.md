---
disable-model-invocation: true
name: qualtrics-ops
description: Operates or audits a live Qualtrics survey through the v3 APIs without disrupting fielding. Covers publish gating, quotas, flow routing, embedded data, panel-vendor redirects, read-back verification, and a read-only pre-fielding audit. Use when publishing or patching a fielding instrument, when a quota counts without blocking, when configuring panel-vendor redirects or flow gates, or when auditing a survey before launch for consent gates, force-response completeness, quotas and redirects, anti-bot instrumentation, and language-arm symmetry.
argument-hint: '[audit | describe the live survey and the change you need to make]'
---

# Qualtrics Live-Survey Operations

## Instructions

### 1. When to use

This skill covers **operating** a survey already built and imported into
Qualtrics — publishing, quotas, flow routing, live text patches, panel-vendor
integration, security options — on an instrument that is or will be fielding
real respondents. It is not survey design or QSF construction; the question is
how to change the definition without breaking what respondents see.

Two modes. **Operations** (default): sections 2-8 govern any write to a live
instrument. **Audit mode** (`audit` as the first argument) is the read-only
pre-fielding assessment at the end.

### 2. Write safety and authorization

**Pre-authorized:** every read (definition, flow, options, quotas, versions),
backups, response exports, and staging the specific change the user asked for.

**Confirm with the user first:** publishing, activation, resetting quota
counters, switching a quota to hard-terminate, deleting responses, creating a
test survey in their account, the audit's browser walk on a live link, and
any write beyond the change they described. These reach real respondents,
vendor billing, or collected data, and several cannot be undone.

**Back up first.** Pull and save the survey definition, flow, and options as
separate JSON before any write. Qualtrics version restore is coarse, carries
data-risk caveats, and does not cover quota counters or options; your
snapshot is the only precise recovery path.

**Verify by read-back, not by absence of error.** A 200 means the API
accepted the request, not that respondents will see the result. After every
write, GET the changed object and confirm it matches intent.

**The version list is the proof a change is live**, not the publish-state
flag (see §3). The standard: your publish created a NEW published version
entry carrying your own description, paired with a read-back of the published
content where the API exposes it, since a description proves provenance, not
content.

**One writer at a time.** Confirm the survey, brand, and environment; that
nobody has the builder open; and the rollback path, before the first write.
On an actively fielding instrument, prefer a change window. Deleting or
restructuring questions and choices can invalidate collected data.

**Assert everything untouched is unchanged.** Several endpoints below are
full replace and silently wipe sibling data. Diff the whole parsed object
against the backup (the server may normalize ordering and defaults), not just
the field you meant to edit.

### 3. Publish gating — two distinct failure modes

Most flow and options edits to an active survey are **staged** until an
explicit version publish: respondents keep the old version while the API
reads back your new one. (A few option keys, availability among them, apply
immediately; assume staged and verify per key.) Question/block writes are
worse: they create no `list_versions` entry, so publish-state can report "in
sync" while the live version lags your edit.

Stage all related writes as one batch, verify the batch by read-back, then
publish ONCE, deliberately (forcing the publish if your client supports it).
Publishing after each write can expose respondents to inconsistent
intermediate versions. Reload the builder before trusting its Draft/Published
badge; it lags the API.

Publishing an **inactive** survey activates it. Treat activation as its own
decision: have the API client require an explicit activation flag so a
content publish can never launch fielding as a side effect.

### 4. Quota API

Every quota error below is silent: the write returns 200, reads back exactly
as sent, renders normally in the builder, and the quota does nothing. Check
against a platform-authored example, never against what looks right.

**If a quota counts but never blocks, check `ActionInfo` first.**
`QuotaAction: "EndCurrentSurvey"` only names the action; the nested
`ActionInfo` object fires it. A quota written with the empty stub

    "ActionInfo": {"Type": "BooleanExpression"}

counts every matching respondent and acts on none — no error at write,
publish, or runtime. The platform's own serialization is:

    "ActionInfo": {"0": {"0": {"ActionType": "EndCurrentSurvey",
                                "Type": "Expression",
                                "LogicType": "QuotaAction"},
                          "Type": "If"},
                    "Type": "BooleanExpression"}

`ActionType` repeats the `QuotaAction` value. If `count` is incrementing, the
matching logic is already correct; go straight to `ActionInfo` (the group's
`Selected` flag and `EndSurveyOptions` do not make a quota fire). To shut an
over-target cell use `Occurrences: 1`, not `0`, which no platform-authored
quota uses.

**Condition dialect.** Compound quotas that "never fire" are a hand-authoring
dialect mismatch, not a platform limit on condition count. Qualtrics's own
quota JSON uses:

- `"Conjuction"` (the legacy misspelling, permanent in the schema), not
  `"Conjunction"`, to join conditions. Single-condition quotas need no join,
  which is why they work while every compound quota sits at zero.
- `"q://{QID}/ChoiceTextEntryValue"`, not `"q://{QID}/TextEntry"`, as the
  operand for a numeric comparison on a text-entry question, with
  `ChoiceLocator` duplicating the same string.
- The **bare** field name as `LeftOperand` for `LogicType: "EmbeddedField"`
  (`{"LogicType": "EmbeddedField", "LeftOperand": "gc", "Operator":
  "EqualTo", "RightOperand": "1"}`), not the `e://Field/gc` form that is
  correct everywhere else in Qualtrics (branch and display logic, piped
  text, redirect URLs). A field verified as populated in the export with
  every quota on it at `count: 0` is this error.
- For choice conditions, both the operand the engine evaluates and the
  locator the editor renders its dropdown from. With only the operand the
  quota works but shows a blank "Select Choice…", and a later UI save of
  that blank state can overwrite live logic with nothing.
- The exact operator enum the API expects; it rejects plausible synonyms.

Written in the correct dialect, flat AND groups of three or four conditions
across different QIDs fire correctly. Before trusting any multi-condition
quota, get a real platform-exported QSF from the same account (ask the user;
an old unrelated survey works) and diff your `Logic` against its quota
objects byte for byte. This takes minutes and is the highest-value check
available. Without a reference file, hand an independent model (the
`advisor` skill) the full evidence trail — what fired, what didn't, exact
JSON of both — and ask it to reason from first principles.

**Simple vs. Cross — identify the type before reading `Logic`.** A `Simple`
quota is one cell: `Logic` is a single expression tree (dict) and
`Occurrences` is that cell's absolute target. A `Cross` quota is Qualtrics's
native interlock: `Logic` is an ARRAY of logic sets that the engine crosses
into cells, `Occurrences` is the grid TOTAL, and `Conjuction` holds each
condition's **percentage share** (`"27%"`), not And/Or — each cell's target
is `Occurrences ×` the product of its shares. Cross expresses an age × gender
× region interlock as one object instead of hundreds, so build grids with
Cross. Because its targets are shares of a total, it is awkward for rebasing
a half-filled field, where "33 slots left" is simply `Occurrences: 33` on a
Simple quota. Build with Cross; repair mid-field with Simple. When an
interlock is the goal, Cross also beats precomputing a merged embedded field.

**Design choices that avoid the problem.**

- If the instrument has not fielded and exact age is not needed, ask age as
  bands (18-29 / 30-39 / ...) and quota on plain `Selected` conditions — no
  text-entry locator, no `>=`/`<=` pair, nothing to get wrong.
- When one language arm carries most traffic (check the export), fold the
  minority arm into the majority arm's demographic quotas, sized to the
  combined remaining target, instead of splitting every quota by arm; disclose
  that the minority arm is not independently capped.

**Prove enforcement; don't infer it.** For any non-trivial quota, either
drive a real response through the matching path and confirm `count`
increments, or diff its `Logic` against a quota on the same live survey that
is already demonstrably counting. Responses created via `POST .../responses`
(import) never trigger quota evaluation, so they prove nothing either way.

To diagnose enforcement itself, do not walk a clone of the real instrument:
geo gates, duplicate-device gates, anti-automation paradata, and
session-resume cookies eject or short-circuit the walk, and stripping them
piecemeal corrupts the flow. Build a **minimal disposable survey** (with the
user's go-ahead): three quota-bearing questions on page 1, a marker question
on page 2 (reaching page 2 is the "not blocked" signal; a one-page survey
cannot show blocking), and TWO quotas — one the walk matches, one differing
in a single condition as a negative control that must stay at 0. Walk once to
fill, walk again, and change ONE variable per walk.

**What `count` can and cannot tell you.**

- It never back-counts responses collected before the quota existed. On a
  fielding survey, a new or repaired quota at 0 is not evidence it is
  broken, and it says nothing about whether an earlier broken quota let the
  sample run uneven. Recompute fill from the response export
  (`POST .../export-responses`) against the target grid before reporting
  any mid-field quota fix as verified.
- Counts can stay stale after response deletion even when the call requests
  a decrement. Before a first fielding wave, zero counters explicitly;
  mid-study, reconcile in-progress sessions and prior waves first.
- Quota-list endpoints paginate at a small page size. Follow the next-page
  cursor or an audit covers only page one.

**Quota groups.**

- Group assignment on creation is unpredictable (quotas have landed in the
  wrong group, or all in the first group, under near-identical scripts), and
  no write field targets a group. Create every quota first, then read back
  membership and fix it via the group PUT. The UI "Move to…" menu does not
  scale.
- Move order matters: a quota already in group A cannot be added to group B
  (`ESDEF44`, "already exists in Quota Group X"). PUT the source group with
  the quotas removed first, then PUT the destination with them added.
- The group update is a **full replace**: omit the quotas array and the
  membership is wiped. Resend the complete membership plus fields the API
  requires on write but omits from its list payload (e.g., a match-mode
  flag); read and write shapes differ.
- Verify by reading every group's membership and matching quota names to the
  intended structure; a group's `Name` is not proof of its `Quotas` array.

**Termination records.** Give every hard quota its own `EndSurveyOptions` at
build time. Without it, the quota inherits survey-level termination (the
respondent still exits via the survey `EOSRedirectURL`), but the response row
carries no `QuotaMet` flag, so quota terminations are indistinguishable from
consent refusals and screen-outs of the same shape. The platform's
serialization for a hard quota:

    "EndSurveyOptions": {"EndingType": "Advanced",
                          "ResponseFlag": "QuotaMet",
                          "Screenout": "Yes", "IgnoreResponse": "Yes",
                          "AnonymizeResponse": "Yes", "CountQuotas": "No",
                          "SurveyTermination": "Redirect",
                          "EOSRedirectURL": "<vendor quota-full URL>"}

When quotas are already live without `EndSurveyOptions`, retrofit the flow
bracket instead: set an embedded field to the quota-full URL immediately
BEFORE the quota-bearing block, reset it to the screen-out URL immediately
AFTER, have the survey redirect read that field, and verify by flow index.
That gets the billing-relevant vendor disposition right; mass-retrofitting
live quotas buys only forensic tidiness.

### 5. Flow mutation and routing placement

- **Anchor routing gates on block descriptions, not on a data-capture
  node.** A capture node can sit pre- or post-consent depending on the
  build, so a gate anchored to it can end up before consent — an ethics
  problem if the gate terminates. Anchor consent-dependent gates right after
  the consent block; paradata gates after every field they read is
  guaranteed to exist; questionnaire checks right after their own block,
  never at end of survey (a late termination wastes the respondent's whole
  interview).
- Know the multilingual architecture. The native translation layer keeps ONE
  block structure with per-language text; a branch-per-language build
  duplicates every block, so each gate must be duplicated into every arm
  with a fresh flow-element ID.
- **Capture before gate.** The node that writes a field must precede every
  gate that reads it. Out of order, the gate fails safe — no error, never
  fires — which is harder to notice than a routing bug that throws.
- When an embedded field carries the exit URL for the end-of-survey
  redirect, the node that SETS it must precede the terminating element
  inside the gate; termination ends flow evaluation.
- On paired-language (twin) instruments, express failure as positive
  selection of a wrong option, not "correct option not selected" — an
  unanswered field in the *other* arm also satisfies "not selected" and
  routes out the wrong arm.
- Guard geolocation terminations with "value present AND not equal to the
  excluded value." An unresolved lookup (proxy, privacy relay, VPN) must not
  satisfy a bare not-equal and terminate a legitimate respondent.
- Reserve *live* termination for signals that cannot belong to a real,
  eligible respondent: ineligibility, duplicate device or session, a hard
  machine signature. Anything scored or graded — bot-risk or fraud scores,
  attention checks, speed — belongs in analysis-side exclusion, because a
  live gate cannot be revisited after it turns someone away.

### 6. Live text edits vs. source specs

For a survey built from versioned source specs (YAML, a builder config),
patch a live typo directly against the live question — match the exact
surrounding text, replace only the intended span — since a rebuild and
repush clobbers formatting applied live since the last build. Sync the fix
back to the spec whitespace-insensitively (specs soft-wrap prose). Keep a
list of what the build pipeline does **not** emit (quality-routing branches,
vendor disclosures added live) and reapply it after every rebuild.

### 7. Panel-vendor integration

Vendor redirect logic follows one pattern regardless of vendor: a
pre-consent screen-out value, a terminal complete value, and an end-of-survey
redirect to the URL in an embedded field the vendor's entry link populated.
Bracket quota-bearing blocks with a quota-full variant (§4) so respondents
who close out a quota reach the vendor's quota-full endpoint rather than a
generic completion or termination redirect.

URL query parameters resolve into piped references at session start
regardless of where, or whether, the embedded-data declaration sits in the
flow (live-verified against redirect pipes). Declare the field anyway; that
is what makes the value reliably typed, saved, and exported.

**Before enabling any quota's hard-terminate action (`EndCurrentSurvey`) on
vendor-sourced traffic, check the vendor correspondence.** Vendors are
sometimes told in writing that an exit status (a quota-full code, say) is
deliberately unused and real-time termination is limited to a named set
(duplicate device, geo-ineligibility, automation). Inside Qualtrics the
switch is a routine config change with no warning, but it starts exercising
a redirect path the vendor expects never to see. This is a compliance
question: search the correspondence for the vendor's redirect status codes by
name, and raise it with the user before activating.

### 8. Security options and post-change checks

Treat the security/options block as read-modify-write: fetch the full
object, change only the target keys, write the whole object back, then
assert every other key is byte-identical to the backup. Options endpoints
are as prone to full-replace semantics as quota groups, and a fraud-detection
threshold or ballot-box-stuffing flag silently reset to default goes
unnoticed until an incident.

After toggling quota actions or publishing repeatedly on a fielding survey,
pull the export and confirm `Progress = 100` and `Finished = True` for every
session whose `StartDate` falls in the affected window, rather than reasoning
that nobody could have been cut off.

## Audit mode (audit)

Run this mode to *assess* a survey rather than change it — `audit` as the
first argument, or the `survey-flow-audit` alias. It reads the live
instrument as it will actually run, not as its build files say, and produces
findings, never fixes.

**Audit mode is read-only on the survey definition.** GET everything;
PUT/POST nothing, except a no-op write check for token scope if the platform
offers one. Each repair goes back through operations as a separate,
authorized change with its own backup, read-back, and publish proof. The
exception is the optional browser walk (Phase H), which creates test
*responses* and possibly test hits on a vendor dashboard; announce it and run
it only with the user's go-ahead.

**When to run:** before soft or full launch, after any live patch, when a
vendor reports a broken redirect, or when taking over a survey. Inputs: API
credentials and survey id; ideally the pre-registration or PAP (for
report-only vs. terminating posture), the vendor's integration sheet
(redirect URLs, ID parameter), and quota targets. A browser MCP (claude-in-chrome or
Playwright) enables Phase H; without it, run A-G and say so.

**Posture:** every PASS cites the object read back (flow element, option
key, quota logic), never the absence of an error. The registered design
wins: where a PAP declares an item report-only, a live branch terminating on
it is a **blocking** finding even if well built.

### Phase A — identity and publish state

- Survey id, name, and active/inactive state match intent. An inactive
  instrument scheduled for launch is fine; an active one nobody meant to open
  is a finding.
- Working definition and published version match, proven by the version list
  (§3). Staged-but-unpublished edits on a fielding survey are **blocking**.
- Response settings that shape the data: partial-response window,
  multiple-submission prevention, anonymization/IP recording, link type,
  expiration, and whether in-progress respondents stay pinned to the version
  they started.

### Phase B — consent before anything

- The first substantive screen is consent (or a language selector whose
  every arm leads first to consent).
- Nothing evaluates or acts before affirmative consent: no terminating
  gates, quality branches, or telemetry collectors on or before the consent
  page. (If the approved protocol puts a minimal eligibility screener first,
  audit it for authorization, minimization, and retention of pre-consent
  data.) Location/device capture may *write* at session start, but every
  branch that *reads* it sits after consent.
- Declining consent routes to the vendor's screen-out (or the study's stated
  exit), not a dead end or a complete.
- Consent text and configuration agree both ways: invisible scoring or
  fingerprinting (reCAPTCHA, device checks) is disclosed; promised skippable
  questions actually exist.

### Phase C — question integrity

- Classify every question: descriptive, forced, requested, or unvalidated.
  Every unvalidated answerable item must be one the design names optional
  (often right for sensitive items), and Phase B must see them.
- Attention and manipulation checks sit where the design says, with the
  registered consequence (terminate vs. record-only). Terminating on an
  attention check screens out humans while catching almost no AI agents —
  flag it as a design smell even when it matches the PAP.
- Multilingual: identify the architecture (§5). Under the translation layer,
  audit translation coverage; under branch-per-language, every item, choice
  set, validation setting, and embedded JS must exist symmetrically in each
  arm. A check present in one arm only, or "correct option NOT selected"
  logic on a twin build, is **blocking**.

### Phase D — flow structure

Walk the full flow tree at every nesting depth:

- Block order matches the intended instrument; randomizers have the intended
  settings (even presentation, subset size).
- Capture-before-gate holds for every embedded field (§5); a condition on a
  never-written field is silently dead.
- Terminating branches decode to the intended trigger; inner flow sets the
  exit redirect *before* the End-of-Survey element; flow IDs are unique; the
  terminal completion redirect node is last.
- On branched (language/arm) instruments, run structural checks per arm.

### Phase E — vendor integration

- Redirect pattern (§7): pre-consent default carrying the screen-out URL,
  terminal overwrite carrying the complete URL, end-of-survey redirecting to
  the piped field. Early leavers exit as screen-outs, completers as
  completes, quota-fulls as quota-fulls — each URL byte-exact against the
  vendor sheet.
- The vendor's respondent-ID parameter is captured and echoed on every exit
  path, including declines. A missing declaration is minor (§7); a wrong
  parameter name is fatal.
- List which vendor endpoints can receive traffic and which are dead by
  design, and check that against what the vendor was told in writing (§7).

### Phase F — quotas

- Decode every quota's logic against the live question's choices and the
  RATIFIED grid: marginal-family designs partition each frame exactly once
  with per-family targets summing to the commissioned N; interlocked or
  overlapping designs have their own structure (check the multiple-match
  setting; identify `Simple` vs. `Cross` before reading `Logic`, §4).
  Screening categories ("I don't live here") belong to no quota.
- Hard vs. soft actions match the ratified design, and group labels say
  which truthfully. For every `EndCurrentSurvey` quota, confirm `ActionInfo`
  carries the nested firing shape (§4).
- Check each condition's dialect (§4). A quota at `count: 0` on a fielding
  survey is a dialect finding until proven otherwise. Follow pagination.
- Counts read zero before fielding; once fielding, fill comes from the
  export (§4).

### Phase G — anti-automation layer

- Platform toggles (bot scoring, device fingerprinting, geo capture) are on
  where the design says, and disclosed per Phase B.
- Behavioral instrumentation (interaction paradata, honeypots, page timers)
  is present on the designated pages in every language arm.
- Live termination is limited to signals that cannot be a real person (§5).
  A scored live gate is a finding.

### Phase H — browser walk (optional, needs a browser MCP)

- Use the LIVE distribution link, not the preview (preview banners change
  rendering and skip embedded-data population), with a test vendor-ID value.
- Walk at minimum: one decline (screen-out redirect fires with the ID
  echoed), one complete per language arm (complete redirect fires), one
  mobile-viewport pass (conjoint tables and stacked layouts render without
  clipping). Where feasible: the quota-full path, one pass per experimental
  arm, an entry missing the vendor ID, and validation/back-button behavior on
  one forced item.
- Confirm no screen precedes consent and the consent page renders in the
  right language per arm.
- Clean up: delete test responses with quota decrement, then re-read quota
  counts (Phase F). In-progress partials usually cannot be deleted via API
  and must expire or be cleared in the UI.

### Audit report

Rank findings **blocking / major / minor**, each with the evidence read back
and the phase that produced it. State the live vs. working version, which
phases ran (and that H was skipped, if so), and which findings the
registered design requires leaving alone. End with test-response cleanup
confirmation if Phase H ran.

## Quality Checks

- [ ] User confirmed each publish, activation, counter reset, hard-terminate
      switch, response deletion, test survey, or out-of-scope write
- [ ] Backup (definition, flow, options as separate JSON) saved before any write
- [ ] Related writes staged as one batch, verified by read-back, then
      published once; activation only at deliberate launch
- [ ] Change proven live by a new version entry with your own description
      plus content read-back, not publish-state or the builder badge
- [ ] Full objects written and read back; untouched keys identical to backup
- [ ] Multi-condition quotas diffed against a platform-exported QSF
      (`Conjuction`, `ChoiceTextEntryValue`, bare `EmbeddedField` operand,
      operand plus `ChoiceLocator`)
- [ ] Quota type (`Simple` vs. `Cross`) identified before reading or writing
      `Logic`
- [ ] Every hard quota's `ActionInfo` populated with the nested firing shape
- [ ] Enforcement demonstrated by observed blocking on a minimal disposable
      survey with a negative control; never inferred from config review or
      from `count` moving (a count shows matching, not blocking)
- [ ] Mid-field fill verified from the response export, not `count`; group
      membership read back and matched by quota name
- [ ] Hard quotas carry `EndSurveyOptions` with `QuotaMet`, or the flow
      bracket is verified by flow index
- [ ] Vendor correspondence checked before enabling `EndCurrentSurvey` on
      vendor traffic
- [ ] After live quota toggling or repeated publishes, export checked for
      `Progress`/`Finished` across the affected window
- [ ] Gates anchored to block descriptions; capture precedes every gate
- [ ] Live terminations limited to non-scored signals; twin-language gates
      use positive wrong-selection
- [ ] Anything the build pipeline doesn't emit reapplied after a rebuild

Audit mode only:

- [ ] Nothing written to the survey definition; every PASS cites an object
      read back
- [ ] Consent first in every arm; every unvalidated item named optional
- [ ] Each vendor exit URL byte-exact, with the ID echoed on every path
- [ ] Quota counts zero pre-fielding; `ActionInfo` populated on every
      `EndCurrentSurvey` quota
- [ ] Findings ranked, phases run stated; browser-walk responses cleaned up
