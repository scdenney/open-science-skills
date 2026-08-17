---
name: qualtrics-ops
description: Operate a live Qualtrics survey via the v3 APIs without breaking fielding. Publish gating, quotas, flow routing, embedded data, panel-vendor redirects, and read-back verification.
argument-hint: "[describe the live survey and the change you need to make]"
---

# Qualtrics Live-Survey Operations

## Instructions

### 1. When to use

This skill covers **operating** a survey already built and imported into
Qualtrics — publishing, quotas, flow routing, live text patches, panel-vendor
integration, security options — on an instrument that is or will be fielding
real respondents. It is not survey design or QSF construction; assume the
survey definition already exists and the question is how to change it without
breaking what respondents currently see.

### 2. Non-negotiables

**Backups first, always.** Pull and save the survey definition (and flow and
options as separate JSON) before any write. Qualtrics version restore exists
but is coarse and carries data-risk caveats; your pre-change snapshot is the
only *precise* recovery path, and the only one that covers objects (quota
counters, options) outside version history.

**Verify by read-back, never by absence of error.** A 200 response proves the
API accepted the request, not that respondents will see the result. After
every write, GET the changed object back and confirm it matches intent.

**The version list is the proof a change is live**, not the publish-state
flag. Question/block writes create no version-history entry, so publish-state
can report "in sync" while the live version still lags behind your edit. The
standard: your publish call created a NEW published version entry carrying
your own description — and, because a description proves provenance rather
than content, pair it with a read-back of the published content where the API
exposes it.

**One writer at a time.** Confirm you are on the right survey, brand, and
environment, that no one has the builder open concurrently, and that you know
the rollback path before the first write. On an actively fielding instrument,
prefer a change window; and remember the platform's own warning that deleting
or restructuring questions and choices can invalidate already-collected data.

**Assert everything untouched is unchanged**, not just that your target
changed — compare parsed structures, since the server may normalize ordering
and defaults. Several of the traps below are full-replace endpoints that
silently wipe sibling data; catching that requires diffing the whole object
against the pre-change backup, not just checking the field you meant to edit.

### 3. Publish gating — two distinct failure modes

Most flow and options edits to an active survey are **staged**, not live,
until an explicit version publish — respondents keep getting the old version
while the API happily reads back your new one. (A few option keys apply
immediately, availability among them; treat "staged until published" as the
safe default assumption and verify per key.) Question/block writes are worse: they
create no `list_versions` entry at all, so publish-state can say "in sync"
immediately after a write that hasn't actually gone anywhere near respondents.
Stage all related writes for a change as one batch, verify the batch by
read-back, then publish ONCE, deliberately (forcing the publish if your client
supports it) — publishing after every individual write can expose respondents
to internally inconsistent intermediate versions. Reload the builder UI before
trusting its Draft/Published badge — it lags the API.

Publishing an **inactive** survey activates it. Treat activation as a
separate, deliberate decision from publishing a change — have your API client
require an explicit activation flag so a routine content publish can never
launch fielding as a side effect.

### 4. Quota API

- **The actual root cause of "compound quota logic never fires" is a
  hand-authoring dialect mismatch, not a platform limit on condition count —
  and getting this wrong once already cost a full day of live-fielding churn
  across two surveys, so read this one carefully.** Qualtrics's own
  internally-generated quota JSON uses `"Conjuction"` (not `"Conjunction"` —
  a legacy misspelling baked permanently into the schema) as the key joining
  multiple conditions, and `"q://{QID}/ChoiceTextEntryValue"` (not
  `"q://{QID}/TextEntry"`) as the operand/locator for a numeric comparison
  against a text-entry question, with `ChoiceLocator` duplicating the same
  string. Hand-write either one with the "obviously correct" English
  spelling or the intuitive-looking locator and the quota accepts the write
  (200 OK), reads back exactly as sent, renders correctly in the builder UI's
  condition editor, and then matches nobody, ever, with no error anywhere —
  because the engine simply doesn't recognize the key/locator and silently
  drops that half of the condition. This produced the exact symptom pattern
  that looks like "compound conditions never fire": single-condition quotas
  (no `Conjuction` needed) counted correctly the whole time; every
  age-range and multi-choice-OR quota sat at zero, on multiple live
  production surveys, for over a week, undetected. **The fix, once
  diagnosed, is to write compound conditions in the correct dialect, not to
  avoid them.** A same-day rebuild using the verified dialect — including
  three- and four-condition flat AND groups spanning multiple different
  QuestionIDs (age range AND gender-selected AND region-selected in one
  group) — fired correctly and counted real respondents within the hour.
  **Do not hand-guess this dialect from documentation or from what "looks
  right."** Find a real, platform-exported QSF from the same account (or ask
  the user for one — even an unrelated old survey works) and diff your
  generated `Logic` block against its quota objects byte-for-byte before
  trusting anything with more than one condition; this is the single highest-
  leverage check available and takes minutes. Absent a reference file, the
  fallback is the advisor-consult pattern: hand a second, independent model
  the full evidence trail (what fired, what didn't, exact JSON of both) and
  ask it to reason from first principles rather than guessing again yourself
  — that is what actually surfaced this dialect mismatch after multiple
  failed self-directed attempts.
- **`LogicType: "EmbeddedField"` quota conditions take the BARE field name as
  `LeftOperand`, not the `e://Field/...` piped reference** — and getting this
  wrong is silent, like every other quota-dialect error. A platform-authored
  Cross quota carries `{"LogicType": "EmbeddedField", "LeftOperand": "gc",
  "Operator": "EqualTo", "RightOperand": "1"}` — just `"gc"`. Writing
  `"e://Field/gc"` (the form that is correct everywhere else in Qualtrics:
  Branch logic, display logic, piped text, redirect URLs) produces a quota
  that accepts the write, reads back intact, and matches nobody. This was
  learned expensively: a Branch-precompute design (merge a value into one
  flat embedded field, then quota on equality) was built at ~130 quota
  objects across two live surveys, with the field VERIFIED correctly
  populated in the response export for real respondents, and every one of
  those quotas read `count: 0` — because all of them used the `e://Field/`
  prefix. Do not conclude from a failure like that that embedded-field quota
  logic is unsupported; check the operand format against a platform-authored
  example first. Note also that when the goal is an interlock, `LogicType:
  "Cross"` (below) is the native mechanism and usually beats precomputing a
  merged field at all.
- **`LogicType: "Cross"` is Qualtrics's native interlock quota, and it is a
  different object shape from `Simple` — know which one you are reading.**
  A Simple quota is one cell: `Logic` is a single expression tree (a dict)
  and `Occurrences` is that cell's absolute target. A Cross quota is a whole
  grid: `Logic` is an ARRAY of logic sets, the engine crosses the sets to
  generate cells, and `Occurrences` is the TOTAL across the grid. In a Cross
  quota the `Conjuction` key does not hold `"And"`/`"Or"` — it holds that
  condition's **percentage allocation** (`"27%"`, `"29%"`), and each cell's
  effective target is `Occurrences x` the product of its shares. So the same
  misspelled key means two completely different things depending on quota
  type; do not pattern-match one onto the other. Choosing between them:
  Cross expresses an age x gender x region interlock as ONE object instead
  of hundreds, which is decisive when building a grid up front. But because
  Cross targets are percentages of a total, it is poorly suited to rebasing
  a partially-collected field — "this cell has 33 slots left of 473" is
  trivial as a Simple quota's absolute `Occurrences: 33` and awkward as a
  share of a total that is already half filled. Build with Cross; repair
  mid-field with Simple.
- **Sidestep the whole range-comparison problem at design time by asking age
  as a categorical band question rather than a numeric text entry.** A
  platform-authored reference survey that quotas cleanly on age does it with
  a multiple-choice item (18-29 / 30-39 / 40-49 / 50-59 / 60+) and plain
  `Selected` conditions — no `ChoiceTextEntryValue` locator, no
  `>=`/`<=` pair, no compound condition, nothing to get wrong. If the
  instrument is not yet fielded and the analysis does not need exact age,
  this is strictly the safer design.
- **For a bilingual/multi-arm instrument, don't reflexively split every
  marginal quota by arm.** If one arm carries the overwhelming majority of
  traffic (check the actual split from the response export, don't assume),
  splitting age/gender/etc. into one quota per arm doubles the object count
  and produces a nonsensical-looking result on screen (a demographic quota
  that appears to depend on survey language). Fold the minority arm into the
  majority arm's quota instead — check only the majority-language question,
  size it to the full combined remaining target — and accept that the
  minority arm isn't independently capped by that specific quota. Disclose
  the tradeoff; don't build the split by default.
- Before trusting ANY quota with more than a trivial condition, prove the
  engine actually fires it: create it, then either drive one real or preview
  response through the matching path and confirm `count` increments, or —
  cheaper — diff its `Logic` shape against a quota on the same live survey
  that is *already* demonstrably counting; identical shape, live proof either
  way. Note preview/import responses are not reliable for this: a response
  created via `POST .../responses` (import) does not trigger quota
  evaluation at all — that's expected, uninformative behavior, not a signal
  either way.
- **A quota's `count` never back-counts responses collected before the quota
  existed.** It only increments on new submissions from creation forward.
  On a survey that has been fielding for a while, a freshly created or
  freshly fixed quota reading 0 or low is not evidence it's broken — and,
  the more dangerous direction, it is also not evidence a *previous* broken
  quota didn't already let the sample run uneven. Either way, `count` cannot
  tell you the true current composition of an already-fielding survey.
  Pull the actual response export (`POST .../export-responses`) and recompute
  fill directly from respondents' real answers against your target grid —
  that's the only number that reflects who has actually been collected, and
  it's required reading before reporting "verified" on any quota fix applied
  mid-field.
- **Quota creation's group auto-assignment is flaky, not just
  "always goes to the first group" — confirmed empirically across two
  surveys built with near-identical scripts.** There is no field to target a
  specific group on write. In one run, three sequential `create_quota_group`
  calls (Age, Gender, Region) resulted in Gender's quotas silently landing in
  the Age group while Region correctly got its own; in another run on a
  different survey, all three groups' quotas landed in the very first group
  regardless of creation order. Do not assume any particular assignment
  pattern, and do not rely on the UI's "Move to…" menu for anything beyond a
  handful of objects — it does not scale. Instead: create every quota first
  (accept whatever group it lands in), THEN read back the actual membership
  and fix it programmatically via the group PUT below. **Order matters when
  fixing it**: a quota already listed in group A's membership cannot be added
  to group B's membership directly — the API returns `ESDEF44` ("already
  exists in Quota Group X"). PUT the *source* group first with a shrunk
  membership list (removing the quotas you're about to move), THEN PUT the
  destination group with them added. Verify final state by reading back every
  group's membership and matching quota names against your intended
  structure — the group's own `Name` field is not proof its `Quotas` array
  is what you think it is.
- The quota-group update endpoint is a **full replace**: omit the quotas array
  and the group's membership is silently wiped. Always resend the complete
  membership plus any fields the API requires on write but omits from its own
  list payload (e.g. a match-mode flag) — write-shape and read-shape are not
  the same contract.
- Choice-based quota conditions need both the operand the evaluation engine
  reads AND the locator the editor UI renders its dropdown from. Write only
  the operand and the condition still *works* but displays as an empty
  "Select Choice…" in the UI — and a later UI-side save of that blank state
  can overwrite live quota logic with nothing.
- Confirm the exact operator enum the API expects (vendors sometimes reject a
  plausible-looking synonym) rather than assuming from REST convention.
- **Give every hard quota its own `EndSurveyOptions` at build time.** A quota
  created without one inherits the survey-level termination settings, which
  works — the respondent still exits and still hits whatever redirect the
  survey-level `EOSRedirectURL` resolves to — but the resulting response row
  carries **no `QuotaMet` flag**, so afterwards you cannot tell a
  quota-terminated respondent from any other early exit except by inferring
  it from their answer pattern. On an instrument that also produces
  consent-refusal and screen-out rows of the same shape (demographics
  answered, no outcome data), that inference gets genuinely fiddly. The
  platform's own serialization for a hard quota looks like:

      "EndSurveyOptions": {"EndingType": "Advanced",
                            "ResponseFlag": "QuotaMet",
                            "Screenout": "Yes", "IgnoreResponse": "Yes",
                            "AnonymizeResponse": "Yes", "CountQuotas": "No",
                            "SurveyTermination": "Redirect",
                            "EOSRedirectURL": "<vendor quota-full URL>"}

  Note this **supersedes an earlier claim in this skill that the API accepts
  no per-quota redirect** — a platform-exported reference survey carries
  `EOSRedirectURL` inside `EndSurveyOptions` on its quota objects, so the
  quota-full URL can live on the quota itself rather than being bracketed in
  the flow. Treat the old claim as untested rather than true; it dates from
  the same period as the compound-logic misdiagnosis above.
- **The flow-bracket pattern remains the right retrofit** when quotas are
  already live without `EndSurveyOptions`: set an embedded field to the
  quota-full exit URL immediately BEFORE the block holding the quota-bearing
  questions, reset it to the screen-out URL immediately AFTER, and have the
  survey-level end-of-survey redirect read that field. Verify by mapping flow
  indices — the setter must precede the block, the reset must follow it. This
  gets the vendor disposition right (which is the billing-relevant half) even
  though the response row stays unflagged. Retrofitting `EndSurveyOptions`
  onto many live quota objects is a mass mutation on a fielding survey; if the
  bracket is already correct, the remaining benefit is forensic tidiness only,
  and is usually not worth the write.
- Quota counts can retain stale values after response deletion even when the
  deletion call requests a decrement. Before a FIRST fielding wave, zero the
  counters explicitly rather than trusting the decrement flag; mid-study,
  reconcile in-progress sessions and prior-wave records first — resetting a
  live counter is destructive and needs explicit authorization.
- Quota-list endpoints paginate at a small page size — always follow the
  next-page cursor, or an audit silently covers only the first page of quotas.

### 5. Flow mutation and routing placement

- **Anchor routing gates on block descriptions, not on a data-capture node.**
  A capture node's position can vary across instruments (some run it
  pre-consent, some post-), so a gate anchored to "wherever that node sits"
  can end up before consent on some builds — ethics-relevant if the gate is a
  termination. Anchor each gate type to a stable semantic point instead:
  consent-dependent gates immediately after the consent block; paradata-based
  gates after the point where every field they read is guaranteed to exist;
  questionnaire-anchored checks right after their own block, never held to
  end-of-survey (a late termination costs the respondent the whole length of
  interview for nothing).
- Know which multilingual architecture you have. Qualtrics' native
  translation layer keeps ONE block structure with per-language text; a
  branch-per-language build duplicates every block per arm. On the latter,
  duplicate each gate into every arm with a fresh flow-element ID — one gate
  does not cover all arms.
- **Capture-before-gate order is load-bearing.** The node that writes a field
  must precede every gate that reads it. Get the order wrong and the gate
  fails *safe* — no error, no fire, just silently dead — which is far more
  dangerous than a routing bug that throws.
- When the exit URL is carried in an embedded-data field consumed by the
  end-of-survey redirect, the node that SETS the field must precede the
  terminating element inside the gate — the termination ends flow evaluation,
  so anything ordered after it never executes.
- On paired-language (twin) instruments, never express a failure condition as
  "the correct option was not selected" — an unanswered field in the
  respondent's *other* language arm also satisfies "not selected" and routes
  out the wrong arm entirely. Express failure as positive selection of a wrong
  option instead.
- Guard any geolocation-based termination with an explicit "value present and
  not equal to the excluded value," not just "not equal to." An unresolved
  lookup (proxy, privacy relay, corporate VPN) must not silently satisfy a
  bare not-equal check and terminate a legitimate respondent.
- Reserve *live* termination for signals that cannot belong to a real,
  eligible respondent: ineligibility, duplicate device/session, a hard machine
  signature. Anything that is scored or graded on a continuum — a bot-risk
  score, a fraud score, an attention-check failure, response-speed outliers —
  belongs in analysis-side exclusion criteria, not a live termination branch,
  because a live gate can't be revisited once it has turned away a respondent.

### 6. Live text edits vs. source specs

When a survey is built from versioned source specs (YAML, a survey-builder
config, etc.), a live typo or wording fix still often needs to go directly
against the live question via a targeted patch — matching exact surrounding
text and replacing only the intended span — rather than a full spec rebuild
and repush, because a rebuild will clobber any manual formatting or ordering
that was applied directly in the live tool since the last build. When syncing
the fix back into the source spec afterward, match whitespace-insensitively:
prose in structured source formats commonly soft-wraps, so a byte-for-byte
diff against live text produces false mismatches.

Keep an explicit list of anything the build pipeline does **not** emit (e.g.
quality-routing branches, vendor-specific disclosures added live) — a rebuild
silently drops these, so they must be reapplied by hand after every rebuild
and repush.

### 7. Panel-vendor integration basics

Redirect logic for panel-vendor traffic follows a stable pattern regardless of
vendor: a pre-consent screen-out value, a terminal complete value, and an
end-of-survey redirect to whichever URL parameter carries the vendor's
completion redirect — typically piped from an embedded-data field the vendor's
entry link populated. Bracket any quota-bearing block with a quota-full
redirect variant so respondents who close out a quota mid-survey get routed to
the vendor's quota-full endpoint rather than falling through to a generic
completion or termination redirect.

**URL query parameters resolve into piped references at session start
regardless of where (or whether) the embedded-data declaration sits in the
flow** — live-verified against redirect pipes. Declare the field anyway:
declaration is what makes the value reliably typed, saved, and exported, and
downstream logic easier to read.

(Panel vendors vary — a generic panel-vendor redirect endpoint is the concept
that matters here, not any particular vendor's API shape.)

**Before enabling ANY quota's hard-terminate action (`EndCurrentSurvey`) on a
survey running through a panel vendor, check prior vendor correspondence for
an explicit statement of which real-time termination paths are in use.**
Vendors are sometimes told directly — in an email, not just implied by
default config — that a given exit status (a quota-full redirect code,
say) is deliberately *not* used, with real-time termination limited to a
named, narrower set of conditions (duplicate device, geo-ineligibility,
automation detection). Flipping a quota to hard-terminate is, from inside
Qualtrics, a purely internal config change with a green checkmark and no
warning — but it silently starts exercising a redirect path the vendor's
system was told to expect never to see. This is a compliance question, not
a technical one, and the fix isn't a Qualtrics setting: read the actual
correspondence (search for the vendor's redirect status codes by name, not
just "quota") before assuming a hard quota is safe to activate on a live
vendor-sourced field.

### 8. Security options

Treat the survey's security/options block as read-modify-write: fetch the
full current object, change only the target keys, and write the whole object
back — then assert every key you did not intend to touch is byte-identical to
the pre-change value. Options endpoints are as prone to full-replace semantics
as the quota-group endpoint above, and a security setting silently reset to a
default (e.g. a fraud-detection threshold, a ballot-box-stuffing prevention
flag) is the kind of regression that goes unnoticed until an incident, not at
write time.

**After any live toggling of quota actions or repeated publishes on a
fielding survey, verify no real respondent was actually affected — don't
just reason about it.** Pull the response export, filter to sessions with
`StartDate` inside the affected window, and check `Progress`/`Finished`
across all of them. A clean 100/`Finished=True` for every session is
checkable proof nobody was cut off mid-survey by a config change in flight;
don't rely on "the targets never should have hit zero" reasoning alone when
the actual data is one export call away.

## Quality Checks

- [ ] Pre-change backup saved (survey definition + flow + options as separate
      JSON) before any write
- [ ] Publish issued after every quota/question/flow write, with activation
      (`allow_activation`/equivalent) triggered only at deliberate launch, never
      as a side effect
- [ ] Change verified live via `list_versions` showing a version with your own
      description — not via publish-state or the builder UI badge alone
- [ ] Full object read back post-write; every untouched key confirmed
      byte-identical to the backup
- [ ] Quota-group and options writes sent as complete objects (full
      membership / full key set), never partial
- [ ] Any quota with more than one condition is diffed byte-for-byte against
      a real, platform-exported QSF's quota `Logic` shape (`Conjuction`
      spelling, `ChoiceTextEntryValue` locator) before being trusted —
      never hand-authored from the "obviously correct" spelling
- [ ] Any `LogicType: "EmbeddedField"` quota condition uses the BARE field
      name as `LeftOperand` (`"gc"`), never the `e://Field/` piped form that
      is correct everywhere else in Qualtrics
- [ ] Quota type identified before reading or writing `Logic`: `Simple` =
      one cell, dict-shaped logic, absolute `Occurrences`; `Cross` = a grid,
      array-of-logic-sets, `Occurrences` is the total and `Conjuction` holds
      a percentage share, not And/Or
- [ ] Fill verified against a real response export, never against `count`
      alone, on any survey that was already fielding before the quota was
      created or fixed
- [ ] Quota-group membership read back post-write and matched by quota name
      against intended structure, not assumed from creation-time order
- [ ] Every hard quota built with its own `EndSurveyOptions`
      (`ResponseFlag: "QuotaMet"`) so terminations are identifiable in the
      response data; if quotas are already live without it, the flow-bracket
      pattern is verified instead by mapping flow indices around the
      quota-bearing block
- [ ] Prior vendor correspondence checked for any stated real-time
      termination agreement before enabling a quota's `EndCurrentSurvey`
      action on a vendor-sourced field
- [ ] After any live quota-action toggling, response export checked for
      `Progress`/`Finished` across the affected window — not just reasoned
      about
- [ ] Choice-based conditions carry both the evaluation operand and the
      UI locator
- [ ] Routing gates anchored to stable block descriptions, not data-capture
      node position; capture nodes confirmed to precede every gate that reads
      them
- [ ] Live terminations limited to non-scored eligibility/fraud signals;
      anything scored or graded routed to analysis-side exclusion instead
- [ ] Twin-language gates expressed as positive wrong-selection, never as
      "not selected"
- [ ] Anything the build pipeline doesn't emit re-applied after any rebuild +
      repush
