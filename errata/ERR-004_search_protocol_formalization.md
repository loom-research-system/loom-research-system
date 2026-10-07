---
id: ERR-004
status: open
severity: high
source: "PL-307 v0.5 §30 Open Questions"
imported_date: "2026-10-08"
related_spec: "PL-307 v1.0"
---
## Issue: Search-Protocol Formalization
PL-307 v1.0 requires `unknown` claims to reference a `search_protocol_id`, but the structure is not formally defined.
## Risk
Without a concrete template, `unknown` can become a convenient dump for difficult questions.
## Resolution Path (Phase 2)
Define a mandatory `Research Protocol` schema that includes databases searched, query strings, and exclusion criteria.
