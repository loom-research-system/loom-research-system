# Phase 3 Execution: Schema Patches + Validator Engine + Adversarial Fixtures

Before locking the validator, two schema patches are required to address the governance debt and cascade ambiguity. Then the validator engine is built, followed by the adversarial fixture suite.

## 3.0 Pre-Validator Schema Patches

### Patch A: actor.schema.yaml — Auditor Pool Governance Fields
(See repository for full YAML implementation. Added fields: classification, auditor_agreement_signed, capacity_limit, rotation_group, independence_distance, etc.)

### Patch B: provenance-event.schema.yaml — Cascade Trigger Event
Added `cascade_trigger_event` to distinguish system-initiated state changes from human-initiated ones.
New Validator Rule: `CASCADE-001` — If any claim has `status: system_flagged_for_review`, there MUST exist a corresponding `cascade_trigger_event`.

## 3.1 Validator Engine Implementation
Implemented `loom_validator/validator.py`. Enforces PL-307 v1.0 schemas and cross-object validation rules. Exit code 0 = valid, non-zero = invalid.

## 3.2 Adversarial Fixture Suite
Created 5 fixtures in `tests/fixtures/adversarial/` covering highest-severity defects:
1. Same-Source Cross-Verification (VERIFICATION-002)
2. Synthetic Reviewer Attestation (PROVENANCE-002)
3. System-Flagged Without Cascade Trigger (CASCADE-001)
4. Dispositive Document Used for Causal Claim (DISPOSITIVE-002)
5. AI Extraction Without Human Confirmation (VERIFICATION-003)

## Phase 3 Complete.
Next Step: Phase 4 — Expand Adversarial Fixture Suite to cover all 23 invalid states from PL-307 §21.
