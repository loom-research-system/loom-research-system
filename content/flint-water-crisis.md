---
title: "Flint Water Crisis: Source and Provenance Audit"
date: 2026-10-27
tags: [flint, water-crisis, provenance-audit, working-draft, sample-invalidation]
loom_spec: "PL-307"
research_status: "ANALYSIS_COMPLETE_PENDING_CLAIM_PROMOTION"
---

# Flint Water Crisis: Source and Provenance Audit

**Public status: Working research record — substantive documentary analysis completed; claim promotion remains bounded by unresolved source questions.**

This record tracks the research question and the source-and-provenance work required before Loom publishes a fully promoted substantive case artifact. The earlier audit correctly rejected placeholder hashes and unsupported claims. The current record now contains a separate forensic analysis of the January–June 2015 Lead and Copper Rule (LCR) sample exclusions and the reported 100-to-60 change.

## Research question

How did decisions about Flint's water supply, water treatment, institutional responsibilities, technical information, and corrective action interact over time—and what does the available record establish about the pathway from decision to public outcome?

The question is deliberately open. The case analysis distinguishes established facts, competing accounts, mechanism hypotheses, and unresolved issues.

## Core claim to test

**Candidate claim:** Corrosion-control treatment was not in place at the outset of the April 2014 switch to the Flint River as a water source.

This remains a separate research target. The current source record contains strong evidence on the later 2015 monitoring and sample-invalidation episode, but that evidence should not be silently substituted for the corrosion-control claim.

## Completed forensic analysis: January–June 2015 LCR reporting

A focused analysis of the original and revised LCR forms, the MDEQ FOIA appeal response, and the later EPA Michigan program review has now been completed.

The analysis establishes the following bounded findings:

1. The original Flint LCR report, dated July 28, 2015, carried handwritten changes from 100 to 60 required samples and from 71 to 69 samples taken. Its comments stated that 175 sample bottles had been distributed, that the minimum had not been reached, and that the City was continuing to solicit samples. fileciteturn439file1L30-L32
2. The revised August 20, 2015 form reported 60 required samples and 69 samples taken and stated that the report was revised after a conference call with DEQ staff, that two samples were removed for not meeting sample criteria, and that the required number was reduced to 60 because of population. fileciteturn439file0L13-L15
3. MDEQ's September 28 FOIA appeal response independently places the conference call between July 28 and August 20 and states that the available material concerning the rationale for invalidating the two samples consisted of handwritten notes and two laboratory sample reports. fileciteturn438file2L100-L132
4. The later EPA 2016 Michigan Drinking Water Program Review found that Flint's population was 99,763 and that, based on that population, 60 samples were required. It also found that MDEQ's records did not clearly document when the population change took effect in the relevant state system. citeturn1search26turn1search0
5. The EPA review found that two samples from the initial list of 71 were excluded from the final 90th-percentile calculation and that both excluded sites were above the lead action level. It identified a Grand Traverse Avenue site documented as a business and a Browning Avenue site documented as having a whole-house filter. EPA found the Browning Avenue record insufficient to resolve whether the filter justified exclusion and identified additional excluded samples and scenarios in which the 90th percentile could have exceeded the action level. citeturn2search33turn2search0

### Current forensic conclusion

The strongest supported finding is **not** that the 100-to-60 change was itself improper. The later EPA review provides a documented population basis for 60 samples, while also identifying poor documentation of when the population change took effect.

The more consequential finding concerns the **two excluded above-action-level samples**. The record establishes that they were excluded and that the contemporaneous documentation did not adequately preserve the rationale and approval for the invalidations. EPA's later review identified unresolved factual questions that could change the resulting 90th-percentile lead value.

The evidence therefore supports a finding about **institutional record quality and unresolved sample-invalidation decisions**, but it does not by itself establish intentional manipulation or improper motive.

Full analysis: `content/flint-lcr-sample-invalidation-analysis.md`.

## Source records currently verified

- Flint Water Advisory Task Force Final Report, March 21, 2016 — exact captured PDF hash recorded in the Flint source manifest.
- EPA Region 5, *High Lead Levels in Flint, Michigan — Interim Report*, June 24, 2015 — exact captured PDF hash recorded in the Flint source manifest.
- Original Flint Lead and Copper Report, July 28, 2015 — exact captured source object recorded in the Flint source manifest.
- Revised Flint Lead and Copper Report, August 20, 2015 — exact captured source object recorded in the Flint source manifest.
- MDEQ FOIA Appeal Response, September 28, 2015 — exact captured PDF hash recorded in the Flint source manifest.

## Required work before final promotion

- [x] Retrieve and inspect the original and revised LCR forms.
- [x] Retrieve and inspect the MDEQ FOIA appeal response.
- [x] Identify an authoritative retrospective review of the January–June 2015 sample exclusions.
- [x] Test the 100-to-60 change against the documented population and applicable sampling requirement.
- [x] Separate the documentary fact of exclusion from any claim about intent.
- [ ] Retrieve and inspect the two laboratory sample reports referenced in the FOIA appeal response.
- [ ] Retrieve and inspect the handwritten MDEQ notes that document the contemporaneous rationale for the two exclusions.
- [ ] Build final atomic claim/evidence records for the sample-invalidation findings.
- [ ] Record actual verification and promotion events under PL-307.
- [ ] Update the public case page only after the claim-level records and remaining primary evidence are complete.

## Provenance warning

An earlier draft included hash-shaped placeholder values, asserted a completed audit, and represented repeated founder entries as separate verification actions. Those statements are not accepted as proof of retrieval, cryptographic provenance, or independent review. They must not be carried forward as established audit facts.

No placeholder hash is a valid substitute for hashing the exact source object. No validator result substitutes for examining the source. No publication label upgrades a claim's evidentiary status.

## Current conclusion

**The Flint case has now moved beyond source retrieval into claim-level forensic analysis.** The documentary chain around the 2015 LCR revision is supported. The 100-to-60 change has a documented population basis but an incompletely documented administrative timing. The two excluded above-action-level samples are the stronger forensic finding: EPA later determined that MDEQ's file lacked adequate documentation of the invalidation decisions and identified unresolved scenarios capable of changing the compliance result.

Intentional manipulation remains unestablished. The next evidentiary step is to inspect the underlying laboratory reports and handwritten notes referenced by the FOIA record, then encode the resulting atomic claims and verification events.
