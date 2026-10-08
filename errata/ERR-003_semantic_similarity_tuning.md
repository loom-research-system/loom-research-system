---
id: ERR-003
status: open
severity: moderate
source: "PL-307 v0.5 §30 Open Questions"
imported_date: "2026-10-09"
related_spec: "PL-307 v1.0"
---
## Issue: Semantic-Similarity Tuning
PL-307 v1.0 §8 mandates an initial near-duplicate flag of ≥0.90 similarity at both document and passage levels.
## Risk
The exact NLP models and thresholds require empirical tuning to avoid false positives (flagging genuinely independent sources) or false negatives.
## Resolution Path (Phase 4 / Phase 12)
Test the 0.90 threshold against the adversarial fixture suite and the real Flint corpus.
