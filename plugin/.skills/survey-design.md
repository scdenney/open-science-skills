---
name: survey-design
description: Guides the design of survey instruments for experimental social science. Use when (1) writing survey questions or constructing response scales, (2) organizing survey flow and block ordering, (3) designing treatment delivery within a survey, (4) planning pretesting or cognitive interviews, (5) managing respondent burden and survey length, (6) mitigating social desirability bias in sensitive questions, or (7) choosing between direct and indirect measurement. Covers question wording, scale construction, ordering effects, attention checks, and treatment-outcome separation.
---

# Survey Instrument Designer

## Instructions

### 1. Question Construction
- **Item-Specific Wording:** Frame questions with item-specific response options rather than agree/disagree, true/false, or yes/no formats. Instead of "Do you agree that immigration benefits the economy?" use "How much does immigration benefit or harm the economy?" with a substantive scale. This reduces acquiescence bias and forces respondents to process the item content (Stantcheva 2023).
- **Open-Ended vs. Closed-Ended:** Use open-ended questions to discover respondent frames and vocabulary before designing closed-ended items. Deploy open-ended items in pilots to generate response categories, then convert to closed-ended for the main study. In the main survey, reserve open-ended items for exploratory or manipulation-check purposes.
- **Behavioral vs. Attitudinal:** Prefer behavioral measures (what respondents would do) over attitudinal measures (what respondents feel) when the research question concerns real-world consequences. Attitudinal items are appropriate when the construct of interest is itself an attitude, but note that attitude-behavior gaps are well documented.
- **Avoid Double-Barreled Questions:** Each item should measure exactly one construct. "Do you support increased immigration and refugee resettlement?" conflates two distinct policy domains. Split into separate items.
- **Avoid Leading and Loaded Language:** Avoid terms that signal a "correct" answer or carry strong normative connotations. Pilot-test whether question framing shifts responses -- if it does, the wording is a treatment, not a measure (Stantcheva 2023).
- **Numeric vs. Qualitative Response Options:** For cross-country or cross-group comparisons, prefer qualitative response options ("a lot," "somewhat," "not at all") over exact numeric quantities. Specific numbers carry different informational weight across contexts -- "$50,000 income" means different things in the US and South Korea (Stantcheva 2023).

### 2. Scale Design
- **Number of Scale Points:** Use 5- to 7-point scales for most attitudinal items. Fewer points lose discrimination; more points rarely add measurement precision and increase cognitive load. For knowledge or factual questions, binary or categorical formats are often sufficient.
- **Labeled vs. Endpoint-Only:** Label all scale points when feasible. Fully labeled scales reduce respondent uncertainty about the meaning of intermediate values and improve cross-respondent comparability.
- **Unipolar vs. Bipolar:** Match scale polarity to the construct. Bipolar scales (oppose--support) suit constructs with a natural midpoint. Unipolar scales (not at all--extremely) suit constructs with a natural zero point (e.g., frequency, intensity).
- **Feeling Thermometers:** Use with caution. Feeling thermometers (0--100) introduce measurement noise because respondents interpret the scale differently. They are useful for relative comparisons across targets within respondents but unreliable for absolute-level interpretation across respondents.
- **Index Construction:** When combining multiple items into an index, verify internal consistency (Cronbach's alpha > 0.70 as a minimum threshold). Report the construction method (additive, averaged, factor-analytic). Pre-specify index construction rules in the pre-analysis plan; do not construct indices after seeing the data.
- **Balanced Scales:** Include equal numbers of positively and negatively worded options or directional anchors. Unbalanced scales (three positive options, one negative) bias responses toward the overrepresented direction.

### 3. Survey Flow and Organization
- **Ordering Effects:** Question order affects responses through priming, anchoring, and context effects. Place general questions before specific ones when measuring broad attitudes; reverse this when specific experiences are the construct of interest.
- **Warm-Up Items:** Begin the survey with non-sensitive, low-stakes items to build respondent engagement before introducing experimental blocks or sensitive questions. Demographic items can serve this purpose but should not precede treatment blocks if they could prime identity salience.
- **Treatment Placement:** Place experimental treatments after warm-up items but before primary outcome measures. Separate treatment exposure from outcome elicitation with buffer items to reduce experimenter demand effects (Stantcheva 2023).
- **Treatment-Outcome Separation:** Insert unrelated items or a brief distractor block between treatment and outcome to reduce the salience of the treatment-outcome link. This mitigates EDE without introducing significant respondent burden.
- **Block Randomization:** Randomize the order of thematic blocks (e.g., policy attitudes, demographic items, secondary measures) across respondents to prevent systematic ordering effects. Within blocks, randomize item order for nominal response sets.
- **Comprehension Check Placement:** Place comprehension and manipulation checks after outcome elicitation, not immediately after treatment. Post-treatment comprehension checks placed before outcomes can signal the study's purpose and inflate demand effects (Stantcheva 2023).

### 4. Pretesting and Cognitive Interviewing
- **Cognitive Interview Protocols:** Conduct cognitive interviews using think-aloud protocols (respondents verbalize their reasoning while answering) and/or retrospective probing (follow-up questions about interpretation and processing). Target 5--10 respondents per round; iterate until no new comprehension problems emerge.
- **Pilot Studies vs. Soft Launches:** These serve distinct purposes. Pilot studies test content: comprehension, response distributions, treatment uptake, manipulation check performance. Soft launches test logistics: survey flow, skip logic, display rendering, timing, and platform-specific issues. Conduct both, in sequence (Stantcheva 2023).
- **Pilot Timing:** Pilot after instrument draft, before IRB submission when possible (so findings can inform the registered design), and before full deployment. Budget for at least two rounds of piloting.
- **What to Test:** Assess comprehension (do respondents interpret items as intended?), information processing (do respondents engage with treatment materials?), timing (is the median completion time within the target range?), dropout patterns (where do respondents abandon the survey?), and floor/ceiling effects (are response distributions sufficiently spread?).

### 5. Respondent Burden and Survey Length
- **Completion Time Targets:** Target 10--20 minutes for online panels. Completion rates decline sharply beyond 20 minutes. For complex experimental designs (conjoint + vignette + battery), monitor pilot timing carefully and cut secondary measures before primary ones if the survey is too long (Stantcheva 2023).
- **Attention Checks:** Embed 1--3 attention checks (instructed response items, e.g., "Select 'Strongly agree' for this item") distributed across the survey. Pre-specify exclusion rules for attention check failures in the pre-analysis plan. Report results with and without failed-attention respondents.
- **Speeding Detection:** Flag respondents completing the survey in less than one-third of the median completion time. Pre-specify whether speeders are excluded or included with a robustness check. Speeding is an indicator of satisficing, not necessarily of random responding.
- **Mobile vs. Desktop:** Design the survey for mobile-first if the platform supports it. Conjoint tables and matrix questions render poorly on mobile devices. Test rendering on both form factors during the soft launch. Report the device split in the methods section.

### 6. Sensitive Questions and Social Desirability
- **Direct vs. Indirect Measurement:** For sensitive topics (racial attitudes, immigration enforcement preferences, illicit behavior), assess whether direct questions produce valid responses. If prior evidence suggests social desirability bias, use indirect techniques: list experiments, randomized response, or endorsement experiments (Blair et al. 2020).
- **When to Use Indirect Measurement:** Consult domain-specific sensitivity estimates (Blair et al. 2020) before defaulting to indirect methods. Indirect techniques reduce statistical power substantially (a list experiment requires ~10x the sample of a direct question for equivalent precision). Use them only when the expected sensitivity bias exceeds the precision cost.
- **Neutral Framing for Direct Questions:** When using direct questions on sensitive topics, frame items neutrally. Offer a full range of socially acceptable response options. Avoid "Do you support X?" when "What is your view on X?" with a balanced scale is available.
- **Obfuscated Follow-Ups:** For factual questions where respondents may misreport, use incentive-compatible designs (monetary incentives for accurate answers) or obfuscated follow-ups that verify self-reports without making the verification salient (Stantcheva 2023).

### 7. Treatment Delivery in Surveys
- **Information Treatment Formats:** Match format to treatment complexity. Short factual corrections work as text. Complex policy information benefits from infographics or structured tables. Video treatments increase engagement but introduce confounds (narrator characteristics, production quality) and require bandwidth.
- **Vignette Construction:** Write vignettes at a "medium level of specificity" -- concrete enough to engage respondents but not so detailed that unintended confounds are introduced (Sniderman 2018). For factorial vignettes, verify that all attribute combinations produce coherent paragraphs.
- **Forced Exposure and Comprehension Gates:** When treatment uptake is critical (e.g., information experiments), use forced exposure (minimum display time before advancing) combined with comprehension gates (respondents must answer a comprehension question correctly to proceed). Report the proportion passing comprehension gates and analyze both ITT (all assigned) and per-protocol (comprehension gate passers) samples.
- **Treatment Fidelity Verification:** After the treatment block, include a brief treatment recall or comprehension item to verify that respondents processed the treatment content. Place this after outcome measures to avoid signaling the study's purpose (see Section 3 on check placement).

## Quality Checks
- [ ] **Item-Specific Scales:** Are all attitudinal items worded with item-specific response options (no agree/disagree or yes/no)?
- [ ] **No Double-Barreled Items:** Does each question measure exactly one construct?
- [ ] **Scale Polarity:** Are bipolar and unipolar scales matched to the construct?
- [ ] **Index Pre-Specified:** Are index construction rules specified in the pre-analysis plan, not post hoc?
- [ ] **Treatment-Outcome Separation:** Are buffer items placed between treatment and outcome blocks?
- [ ] **Check Placement:** Are comprehension and manipulation checks placed after outcome elicitation?
- [ ] **Cognitive Interviews:** Were cognitive interviews conducted to test item comprehension?
- [ ] **Both Pilot Types:** Were both a content pilot and a logistical soft launch conducted?
- [ ] **Completion Time:** Is the median completion time within the 10--20 minute target?
- [ ] **Attention Check Rules:** Are attention check exclusion rules pre-specified and results reported with and without exclusions?
- [ ] **Sensitivity Assessment:** For sensitive topics, was the need for indirect measurement assessed using domain-specific evidence (Blair et al. 2020)?
- [ ] **Mobile Tested:** Was the survey tested on mobile devices during the soft launch?
- [ ] **Forced Exposure:** For information treatments, are forced exposure or comprehension gates used to verify treatment uptake?
- [ ] **Neutral Framing:** Are sensitive questions framed neutrally with balanced response options?
