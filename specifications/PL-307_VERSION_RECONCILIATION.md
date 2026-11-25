# PL-307 version reconciliation

**Status: governing specification restored; implementation validation remains open**

## Authoritative version

The current governing claim-state specification is **PL-307 v1.0, LOCKED, effective 2026-09-10**. The complete 31-section text has been restored to:

`specifications/PL-307_v1.0_Claims_Epistemic_Status_Verification_Promotion.md`

The recovered v1.0 text supersedes the earlier v0.5 stable implementation baseline. The repository's older file labelled PL-307 v0.1 is a historical artifact and must not be treated as the current governing specification.

## Governing distinctions

PL-307 v1.0 keeps four dimensions separate:

- Workflow `status`: `proposed`, `under_review`, `system_flagged_for_review`, `completed`, `rejected`, `deprecated`.
- Epistemic status: `proposed`, `unknown`, `unresolved`, `contested`, `supported`, `known`.
- Verification level: `none`, `source_backed`, `cross_verified`, `primary_verified`.
- Promotion stage: `candidate`, `accepted`, `canonical`.

In particular, `supported` is an epistemic status; `accepted` is a promotion stage. They are not interchangeable.

Other governing requirements include:
- `supported` and `accepted` require `cross_verified` or stronger.
- `known` requires cross-verification, no unresolved contradiction, explicit primary applicability, applicable primary examination, human review, and documented scope limits.
- `primary_verified` presupposes cross-verification except for the narrow `dispositive_document` case.
- AI/OCR-extracted material evidence caps verification at `source_backed` until a human verification event independently re-examines the original source.
- Promotion is a governance event; validator eligibility does not itself promote a claim.
- Claim atomicity, append-only verification events, evidence-retraction cascades, demotion/revision, and diagnostic epistemic ceilings are mandatory.
- The solo-founder exception for public `supported`/`canonical` claims requires visible disclosure; it never permits `known`.

## Repository drift identified

Before this restoration:
- The repository's v0.1 specification was marked LOCKED despite being superseded.
- The v1.0 file contained only a placeholder.
- The claim schema already used the v1.0 promotion vocabulary (`candidate`, `accepted`, `canonical`), but the Brief and Audit compilers selected `accepted` and `canonical` without tests guarding that contract.
- The GitHub issue workflow called a separate ingester from the implementation exercised by tests, creating divergent IDs and missing idempotency in the production path.
- The issue workflow installed `jsonschema` but did not validate the records it committed.

## Changes in this branch

This branch restores the full v1.0 specification, adds regression tests for the correct separation of epistemic status and promotion stage, unifies GitHub issue ingestion behind one idempotent implementation, preserves issue metadata and requested depth, and validates inquiry/plan records before the issue workflow commits them.

This is not a claim of full PL-307 v1.0 conformance. The claim, evidence, observation, diagnostic, actor, and verification-event schemas and cross-object validator still require implementation and adversarial testing against the complete specification. No claim is promoted by this change.
