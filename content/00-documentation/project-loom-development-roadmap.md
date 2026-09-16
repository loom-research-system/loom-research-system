---
title: Project Loom — Research & Contributor Roadmap
description: Detailed development roadmap for researchers, auditors, developers, and contributors
---

# Project Loom — Research & Contributor Roadmap

**Stage: Building the foundation**

This is the detailed roadmap for people who want to understand how Loom is being constructed, inspect the methodology, contribute research or technical work, or participate in testing and audit.

For a plain-language explanation, start with **[What Loom Is Building](roadmap)**.

Project Loom is being built as a research system, not as an AI answer generator. The roadmap therefore tracks the development of the research infrastructure itself: specifications, evidence handling, provenance, validation, adversarial testing, human audit, and public research outputs.

The status language is deliberately conservative. A capability is not described as working merely because it has been specified or demonstrated once.

## Development principle

> **Specification → implementation → artifact → adversarial test → public description**

Loom follows four corresponding rules:

- Do not add a capability until there is a record of how it is supposed to behave.
- Do not call a capability working until implementation and testing demonstrate that it behaves that way.
- Do not call research verified until its evidence is inspectable.
- Do not call a governance event human until a human actually performed it.

## Current state

### Working now

- **Loom ontology and research framework** — the core concepts and analytical structure are being developed and tested against cases.
- **Claims, verification, and promotion specification** — PL-307 defines how claims move through proposed, supported, and canonical states while keeping epistemic status, verification level, and workflow status separate.
- **Evidence and provenance requirements** — source retrieval, evidence registration, verification events, contradiction handling, and correction/demotion are being formalized.
- **Flint Water Crisis case** — Flint is the first case being reconstructed through the newer evidence and provenance model.
- **Local Loom Capture API MVP** — a working local capture layer records observations and artifacts with structured metadata and SHA-256 hashes. Capture does not decide whether something is true or promote it into the research corpus.

### Under development

- Machine-readable schemas for research objects.
- A validator that checks claims, evidence, provenance, epistemic status, and promotion eligibility.
- Adversarial tests designed to expose fabrication, provenance failures, scope drift, contradiction handling failures, and other weaknesses.
- Human audit governance for the four-person audit group.
- Reconstruction of Flint from retrieved primary and secondary sources.
- Correction and demotion workflows that preserve the history of changes.
- Automated provenance and research/process infrastructure.

### Not yet claimed

Loom does **not** yet claim to be fully operational, independently audited, automatically verified, or capable of producing verified research without human review.

## Roadmap

### Phase 0 — Freeze the Epistemic Baseline
**Status: In progress**

Lock the core rules governing claims, evidence, verification, promotion, contradictions, provenance, and correction. PL-307 v0.5 is the current design baseline pending implementation validation and incorporation of its recorded errata.

### Phase 1 — Establish the Living Research Record
**Status: Partially operational**

Create the persistent record of research requests, sources, evidence, claims, reviews, corrections, provenance events, failures, and development decisions. The first local Capture API MVP is working and provides the early capture layer.

### Phase 2 — Define Machine-Readable Research Objects
**Status: Specification underway**

Turn Loom's research objects into explicit schemas so that the system can validate them rather than relying on prose conventions alone.

### Phase 3 — Build the Validator
**Status: Planned**

Implement machine checks for schema validity, provenance requirements, contradiction rules, verification levels, promotion eligibility, scope drift, and related integrity constraints.

### Phase 4 — Adversarial Testing
**Status: Planned**

Attack the system deliberately. Tests will include fabricated reviewers, false provenance, placeholder evidence presented as real evidence, contradictory sources, scope mismatches, duplicate or syndicated sources, unsupported claims, and other failure conditions.

### Phase 5 — Human Audit Governance
**Status: Not yet established**

Define the actual human audit process, including auditor roles, independence and conflict requirements, audit boundaries, review records, and sign-off rules. Loom will not describe prospective auditors as an existing audit institution.

### Phase 6 — Reconstruct Flint
**Status: In progress**

Rebuild the Flint case using the research model rather than relying on previously drafted case material. The first real source has been located; retrieval, hashing, evidence extraction, and human confirmation remain part of the work.

### Phase 7 — Four-Person Adversarial Audit
**Status: Planned**

Run the implemented system through adversarial review by the four-person human audit group. The purpose is to determine where the system still fails, not to manufacture a successful audit result.

### Phase 8 — Demonstrate Correction and Demotion
**Status: Planned**

Show that a claim can be challenged, corrected, reassessed, or demoted while preserving an inspectable record of what changed and why.

### Phase 9 — Publish the First Genuine Loom Research Artifact
**Status: Planned**

Publish a research artifact only after its evidence, provenance, verification, review, and promotion requirements have actually been satisfied.

### Phase 10 — Publish How Loom Research Works
**Status: Planned**

Document the implemented research process publicly so that readers can see how evidence becomes a claim and how a claim becomes eligible for promotion. This description will be based on demonstrated system behavior, not an aspirational architecture.

### Phase 11 — Loom Process & Provenance API
**Status: Planned**

Extend the capture layer into a process and provenance API capable of exposing the research record, verification events, and relationships among research objects.

### Phase 12 — Controlled Automation
**Status: Planned**

Automate bounded research and documentation tasks without allowing automation to bypass evidence, provenance, verification, or human governance gates.

### Phase 13 — Public Research Infrastructure
**Status: Planned**

Make the research infrastructure broadly inspectable and usable while preserving the distinction between public presentation and the underlying research system of record.

### Phase 14 — External Research & Institutional Use
**Status: Future**

Explore use by external researchers and institutions only after the underlying research and governance mechanisms have been demonstrated internally.

## What contribution means

Loom is being built in public, but contribution does not mean simply adding text to the website. Contributions need to fit the research and provenance model.

### Researchers

Researchers can contribute by:

- locating and registering relevant sources;
- extracting evidence with precise source locations;
- testing whether Loom concepts explain documented cases;
- identifying counterexamples and contradictory evidence;
- proposing ontology or methodology changes with supporting evidence;
- reviewing case reconstructions; and
- challenging claims that appear stronger than their evidence supports.

### Auditors

Auditors will test whether Loom's research and governance mechanisms behave according to their specifications. Auditor roles, independence requirements, conflicts of interest, review boundaries, and sign-off procedures are being established before the audit process is treated as operational.

### Developers

Developers can contribute to the research infrastructure itself, including schemas, validators, provenance systems, capture and process APIs, automated tests, and public interfaces.

Technical contributions must preserve the central separation between **capture, evidence, verification, and promotion**. Automation must not silently become an epistemic authority.

### Case researchers

Case researchers can help reconstruct individual cases from source material. The expected contribution is not a polished narrative alone; it is a traceable research record showing sources, evidence, claims, contradictions, and unresolved questions.

## What contributors should not do

Contributors should not:

- invent sources, reviewers, attestations, hashes, signatures, or governance events;
- treat an AI-generated statement as verified evidence;
- describe an unretrieved document as inspected;
- silently replace a flawed research record instead of recording the correction;
- promote a claim merely because it sounds plausible; or
- describe planned infrastructure as operational.

The system is specifically being designed to make these failures detectable.

## What progress means here

Progress in Loom is not measured only by the number of pages, case studies, or features produced.

A new capability becomes meaningful when there is a traceable relationship between:

**what was specified → what was built → what artifact was produced → what test was run → what failed → what was corrected → what can now be claimed publicly.**

That record is part of the research infrastructure itself.

## What comes next

The immediate work is to move from specification toward validation:

1. incorporate the known PL-307 errata without silently changing the baseline;
2. correct the documented synthetic-reviewer failure record and related fixtures;
3. complete real-source retrieval and evidence registration for Flint;
4. build the machine-readable research objects and validator;
5. establish the four-person human audit process;
6. run adversarial tests before describing the resulting capabilities as operational.

## Contribution pathway

The contribution process will become more formal as the research infrastructure is implemented. For now, the most useful contributions are **evidence, criticism, reproducible tests, case reconstruction, schema/validator work, and documented challenges to existing assumptions**.

The project will distinguish between:

- a suggestion;
- a proposed research object;
- an implemented change;
- a verified research result; and
- a human governance decision.

Those are different things and will not be collapsed into one status simply because they appear on the same website.

*This roadmap is a living project record. Statuses should change when the underlying work changes, not simply when a page is written.*
