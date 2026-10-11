---
title: "Development Roadmap"
date: 2026-10-09
tags: [roadmap, development]
---

# Loom is still being built

Loom is not presenting itself as a finished research institution. We are building the infrastructure needed to investigate government implementation rigorously—and we are publishing that development process as we go.

We follow a strict development principle: **Specification → Implementation → Artifact → Adversarial Test → Public Description.** 

We do not claim a capability is operational until it has survived adversarial testing.

---

## What works today
These components are specified, implemented, and actively used in our case reconstructions:
- **Research framework:** The core ontology and conceptual framework for tracing policy divergence.
- **Evidence and provenance standards:** Rules for how sources are retrieved, hashed, and linked to claims.
- **Development capture:** A local API for preserving development discussions, decisions, and failures.
- **Initial case reconstruction:** The Flint Water Crisis case study serves as our first end-to-end implementation test.
- **Claims and verification specification:** The PL-307 specification governing epistemic status and promotion.

## What we are building
These components are specified and actively under development:
- **Machine-readable research records:** Formal YAML/JSON schemas for all research objects.
- **Automated validation:** A mechanical validator that rejects invalid epistemic states (e.g., "known" claims with unresolved contradictions).
- **Adversarial testing:** A suite of intentional "bad" data designed to break the validator and prove it works.
- **Human audit procedures:** Defining the roles, independence requirements, and governance events for human reviewers.
- **Correction and demotion:** Workflows for challenging and downgrading previously promoted claims.
- **Public provenance:** The "Trace the Evidence" UI layer that exposes the audit trail to readers.

## What we won't claim yet
Loom does not currently claim that its research corpus is fully operational, independently audited, or automatically verified. 

We will not call research "independently verified" until the underlying human audit process actually supports that claim. The roadmap is deliberately designed so that those claims can only be made after the corresponding capabilities have been demonstrated.

---

## The Complete Technical Phases
For those interested in the engineering details, the full 14-phase development roadmap is maintained in our repository:
- **Phase 0:** Freeze the Epistemic Baseline
- **Phase 1:** Establish the Living Research Record
- **Phase 2:** Define the Machine-Readable Research Objects
- **Phase 3:** Build the Validator
- **Phase 4:** Adversarial Testing
- **Phase 5:** Establish Human Audit Governance
- **Phase 6:** Reconstruct the Flint Water Crisis *(In Progress)*
- **Phase 7:** Four-Person Adversarial Audit
- **Phase 8:** Demonstrate Correction and Demotion
- *(Phases 9-14: Publication, API, Automation, and External Credibility)*

**[View the raw technical roadmap in our GitHub repository →](https://github.com/loom-research-system/loom-research-system/blob/main/specifications/PL-001_v1.1_Implementation_Roadmap_Governance_Control.md)**
