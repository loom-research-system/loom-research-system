---
id: DIA-2026-002
category: failure
title: "0001: Synthetic Reviewer Attestation in REQ-006 v1.0"
date: "2026-09-10"
author: "Loom Founder"
related_specs: ["PL-307 v1.0", "PL-001 v1.1"]
tags: ["governance", "audit", "absolute-prohibition"]
---

## Context
During the initial drafting of REQ-006 v1.0 (Flint Water Crisis), an "External Adversarial Review" appendix was generated containing a fictional reviewer identity ("Dr. Elena Rostova"), a simulated PGP fingerprint, and a fabricated institutional affiliation.

## The Failure
This violated the **Absolute Prohibition** rule of PL-001 v1.1: *"No fabricated reviewer identities, signatures, hashes, URLs, or attestations. Ever."* The artifact was caught during internal audit before publication. 

## Root Cause
The AI generation process defaulted to completing the "external review" section of the template by hallucinating a plausible-sounding expert identity, rather than flagging the missing human reviewer as a blocker.

## Remediation / What Changed
1. The specification was immediately updated to explicitly list "synthetic reviewer attestations" as a Phase 4 adversarial fixture that the validator MUST reject (`PROVENANCE-002`).
2. The `actor.schema.yaml` was updated to require verifiable human identity fields.
3. This diary entry was created to ensure the failure is permanently recorded. The prohibition without the confession reads as a cover; documenting it reads as a lesson.
