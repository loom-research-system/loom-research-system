---
project: Project Loom
artifact_id: PL-205
title: Cross-Case Comparison Method
version: v0.1
status: Draft
layer: Methodology
owner: Project Loom
created: 2026-07-11
updated: 2026-07-11
depends_on:
  - "[[PL-201 Loom Analysis Protocol]]"
supersedes: []
superseded_by: []
related:
  - "[[PL-501 Cross-Case Comparison Matrix]]"
  - "[[PL-502 Pattern Reports]]"
purpose: Define the method for systematic comparison across Loom case studies.
scope: Applied after every set of cases to identify emerging patterns and generate testable hypotheses.
---

# Cross-Case Comparison Method

## Comparison Variables

Derived from the [[PL-201 Loom Analysis Protocol|Analysis Protocol]]:

1. Policy design assessment
2. Authority alignment
3. Dependency concentration
4. Implementation debt (by type and severity)
5. Veto fragility
6. Execution fragility
7. Adaptive capacity
8. Outcome classification
9. Primary diagnostic classification
10. Level of analysis

## Method

1. After each case study, score the case across all comparison variables.
2. Update the [[PL-501 Cross-Case Comparison Matrix]].
3. When patterns persist across 5+ cases with diverse configurations, generate a [[PL-502 Pattern Reports|Pattern Report]].

## Emerging Patterns (n=3)

1. High dependency concentration correlates with implementation vulnerability.
2. High implementation debt predates failure in both failure cases.
3. Low fragility in both dimensions correlates with implementation success.
4. Capacity domain analysis prevents overgeneralization.

---

## Change Log

| Version | Date | Changes | Rationale |
|---------|------|---------|-----------|
| v0.1 | 2026-07-11 | Initial Cross-Case Comparison Method | Formalize cross-case analysis after first three cases |