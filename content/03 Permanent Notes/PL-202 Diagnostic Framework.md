---
project: Project Loom
artifact_id: PL-202
title: Diagnostic Framework
version: v1.0
status: Working
layer: Methodology
owner: Project Loom
created: 2026-07-11
updated: 2026-07-11
depends_on:
  - "[[PL-201 Loom Analysis Protocol]]"
supersedes: []
superseded_by: []
related:
  - "[[PL-203 Capacity Assessment Framework]]"
purpose: Define the standardized diagnostic sequence applied in every Loom case study.
scope: The analytical engine embedded within the Protocol. Can be extracted and used independently for rapid assessment.
---

# Diagnostic Framework

## Diagnostic Sequence

1. **Policy Diagnosis** — Was the policy objective sufficiently defined and matched to the mechanism chosen?
2. **Governance Diagnosis** — Were responsibility and authority aligned across the implementing network?
3. **Dependency Diagnosis** — Where were critical dependencies concentrated? Did they have redundancy?
4. **Capacity Diagnosis** — Which capacity domains were sufficient? Which were insufficient?
5. **Debt Diagnosis** — What implementation debt existed before the stress event?
6. **Fragility Diagnosis** — Was the failure driven by veto fragility, execution fragility, or both?
7. **Outcome Analysis** — At what stage did implementation succeed, degrade, or break?
8. **Intervention Design** — What would improve the probability of achieving the intended outcome?

## Diagnostic Classifications

- **Policy design failure** — the mechanism could not produce the objective
- **Authority failure** — the implementing institution lacked the necessary authority
- **Capacity failure** — the institution lacked specific capabilities required
- **Dependency failure** — a critical dependency broke without redundancy
- **Fragility failure** — an external actor or condition disrupted the pathway
- **Debt revelation** — accumulated structural weakness made failure likely
- **Adaptive failure** — the system could not diagnose and correct course
- **Recovery success** — the system failed initially but demonstrated adaptive capacity
- **Design adequacy question** — governance performed adequately; policy design limitations explain outcome

---

## Change Log

| Version | Date | Changes | Rationale |
|---------|------|---------|-----------|
| v1.0 | 2026-07-11 | Initial Diagnostic Framework | Extracted from [[PL-201 Loom Analysis Protocol]] v1.1 |