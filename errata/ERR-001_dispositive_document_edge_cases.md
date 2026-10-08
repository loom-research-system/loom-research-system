---
id: ERR-001
status: open
severity: moderate
source: "PL-307 v0.5 §30 Open Questions"
imported_date: "2026-09-12"
related_spec: "PL-307 v1.0"
---
## Issue: Dispositive-Document Edge Cases
PL-307 v1.0 allows a single primary source to satisfy `primary_verified` for `dispositive_document` claims.
## Risk
Without strict schema guarding, this carve-out may be abused to bypass the two-independent-source requirement.
## Resolution Path (Phase 2)
The schema must require explicit justification and subject-scope narrowness check.
