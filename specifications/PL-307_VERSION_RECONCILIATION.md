# PL-307 version reconciliation and implementation audit

**Status: governing specification restored; implementation conformance remains incomplete**

## Authoritative version

The current governing claim-state specification is **PL-307 v1.0, LOCKED, effective 2026-09-10**. The complete 31-section text has been restored to:

`specifications/PL-307_v1.0_Claims_Epistemic_Status_Verification_Promotion.md`

The v0.5 document was the stable pre-implementation baseline. The repository's older v0.1 specification is a historical artifact and must not be treated as the current governing specification.

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

## Existing implementation inspected

The repository already contains substantial implementation work; this audit does not treat it as absent:

- `loom_validator/validator.py` implements cross-object rules.
- `tests/test_validator_stress.py` contains adversarial unit tests.
- `scripts/validate_flint_artifacts.py` validates the Flint YAML artifact set against mapped JSON Schemas and checks cross-object references.
- Schemas exist for claims, sources, evidence, diagnostics, actors, provenance events, evidence gaps, research protocols, mechanisms, dependencies, and transitions.

The remaining gaps are narrower and concrete:

1. **Observation schema is corrupt.** `schemas/observation.schema.yaml` currently contains only the four verification-level strings (`none`, `source_backed`, `cross_verified`, `primary_verified`); it is not a JSON Schema. No separate `verification.schema.yaml` exists, although PL-307 §27 lists one.
2. **Generic validator loading is narrower than the research-record store.** `loom_validator/validator.py` scans YAML files under `artifacts/` and `tests/fixtures/`; it does not load JSON records under `research/` or validate every object against its corresponding schema.
3. **Flint validation is case-scoped.** `scripts/validate_flint_artifacts.py` validates `artifacts/flint/*.yaml`; it does not validate the Heritage draft package or the general JSON research-record store.
4. **Provenance requirements are not uniformly enforced across objects.** The schemas and validator need a coordinated pass for claim scope/provenance, source assessment for corroborating sources, actor/event references, primary-evidence applicability, and the AI/OCR human-confirmation cap.
5. **Validation must fail closed before records are committed.** The issue-ingestion workflow previously generated inquiry/plan records without running schema validation. This branch now validates those two record classes, but it does not yet validate all source/evidence/claim/protocol objects.

## Heritage election-fraud package: import blockers

The Heritage package remains a draft and is not imported by this change. Its own manifest records that no underlying court or election-authority records have yet been verified. Before import:

- Create and review the missing `PROT-0001`; it is referenced by the inquiry and claims but absent from the package.
- Resolve the source's date and source-type semantics. The date currently comes from the PDF identifier; the PDF is primary evidence of what Heritage published, but secondary evidence about the underlying cases.
- Correct extraction-method metadata where PDF text extraction was labelled `manual_copy`.
- Validate all IDs, schema fields, references, hashes, and relationships as one package before moving it into the repository.
- Keep every claim provisional; do not imply that the 1,176 headline instances equal 860 panels, persons, incidents, ballots, or affected elections.

## Changes in this branch

This branch restores the full v1.0 specification, documents the actual remaining implementation gaps, unifies GitHub issue ingestion behind one idempotent implementation, preserves issue metadata and requested depth, and validates inquiry/plan records before the issue workflow commits them.

This is not a claim of full PL-307 v1.0 conformance. No claim is promoted, no Heritage record is imported, and no underlying election case is represented as independently verified by this branch.
