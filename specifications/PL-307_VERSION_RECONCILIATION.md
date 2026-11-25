# PL-307 version reconciliation

**Status: implementation hold on unresolved normative text**

## Governing version

The Project Loom working record identifies **PL-307 v0.3 as LOCKED, effective 2026-09-08**. The repository's current files do not faithfully represent that state:

- The file named `PL-307_PL-307 — Claims, Epistemic Status, Verification & Promotion Specification.md` labels itself v0.1 and LOCKED.
- `PL-307_v1.0_Claims_Epistemic_Status_Verification_Promotion.md` is a placeholder, not a specification.
- The claim schema and output compilers use `accepted` where the locked promotion vocabulary is `supported`.

This repository state must not be interpreted as evidence that v1.0 superseded the locked v0.3 specification.

## Locked rules recovered for implementation

The following v0.3 rules are confirmed in the project record and are applied in this change set:

1. Keep four dimensions separate: workflow `status`, `epistemic_status`, `verification_level`, and `promotion_stage`.
2. Epistemic statuses: `proposed`, `unknown`, `unresolved`, `contested`, `supported`, `known`.
3. Verification levels: `none`, `source_backed`, `cross_verified`, `primary_verified`.
4. Promotion stages: `candidate`, `supported`, `canonical`.
5. `cross_verified` requires at least two independently evaluated sources; source count alone is not corroboration.
6. AI-extracted material without independent human re-examination of the source is capped at `source_backed`; human confirmation is required to remove that cap.
7. Verification eligibility does not itself promote a claim. Canonical admission remains a human governance decision.
8. Core rule: **AI may propose. Evidence must establish. Humans may promote.**

## Work deliberately not inferred

The complete authoritative v0.3 text and all accepted errata must be restored from the original locked source before implementing additional normative requirements. In particular, this change does not invent or complete the full KNOWN rule set, exception handling, verification-event schema, override semantics, demotion events, or diagnostic constraints from partial summaries.

Until that source is restored and checked, the repository must not claim full PL-307 v0.3 conformance. The v0.1 file and v1.0 placeholder remain preserved as historical repository artifacts pending an explicit versioned migration.

## Immediate implementation scope

This reconciliation changes only the promotion-stage vocabulary where it is unambiguous, unifies GitHub issue intake behind one idempotent implementation, and validates inquiry/plan records before the intake workflow commits them. It does not promote any claim or modify research findings.
