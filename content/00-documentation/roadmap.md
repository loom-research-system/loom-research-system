---
title: What Loom Is Building
description: A plain-language guide to what Project Loom is, what is being built now, and what comes next
---

# What Loom Is Building

Project Loom is building a research system for understanding **why policies and public programs sometimes fail between being announced and actually working**.

It is not a chatbot that simply gives you an answer. Loom is being designed so that important statements can be traced back to the evidence behind them, checked, challenged, corrected, and reviewed by people.

## Where Loom is right now

Loom is still being built.

Right now, the work is focused on:

- defining the concepts Loom uses to study implementation and governance;
- building rules for how evidence becomes a research claim;
- recording where sources came from and whether they were actually retrieved;
- testing ways to catch mistakes, unsupported claims, fabricated evidence, and misleading provenance;
- rebuilding the Flint Water Crisis case using the newer research model; and
- building software that can capture research material and preserve its history.

Some pieces already work. Other pieces are specifications or prototypes being tested. Loom does not yet describe itself as fully operational or independently audited.

## What happens when Loom studies something?

At a simple level, the process looks like this:

**Question → Sources → Evidence → Claim → Checking → Human review → Published research**

The important part is that each step leaves a record.

For example, finding a document online is not the same as verifying what the document says. A source that cannot actually be retrieved cannot simply be treated as verified evidence.

Likewise, an AI system can help find or organize information, but an AI-generated statement is not automatically a fact in Loom.

> **AI may propose. Evidence must establish. Humans may promote.**

## What is being built next?

### 1. A research record

Loom is creating a structured record of sources, evidence, claims, reviews, corrections, and research decisions so that the history of the work can be inspected rather than reconstructed from memory.

### 2. Automated checks

A validator will check whether research objects follow Loom's rules. It will look for problems such as missing evidence, unresolved contradictions, unsupported promotion, scope mismatches, and broken provenance.

### 3. Adversarial testing

The system will be deliberately tested with bad and misleading inputs. The goal is not to demonstrate that Loom never fails. The goal is to discover how it fails and make those failures visible.

### 4. Human audit

Four people will participate in the human audit process once the governance rules are established. The audit is intended to test the system, not to provide a ceremonial approval.

### 5. The Flint reconstruction

The Flint Water Crisis is the first case being rebuilt through the newer evidence and provenance system. The work is moving from previously drafted material toward individually retrievable and inspectable sources.

### 6. Public research

Once a research artifact has actually passed the required evidence, verification, and human-review gates, Loom will publish it as research rather than presenting an unfinished draft as established knowledge.

## Why does this take so long?

Because the difficult part is not producing another answer.

The difficult part is building a system that can show **why an answer should be trusted, where it came from, what remains uncertain, and what happens when someone proves it wrong.**

That infrastructure has to be built before Loom can honestly claim that its research is reproducible and independently checkable.

## Want the technical version?

If you are a researcher, developer, auditor, policy professional, or someone interested in contributing to the construction of Loom, there is a more detailed roadmap covering the research objects, validation system, adversarial testing, human governance, provenance infrastructure, and planned public research process.

**[Research & Contributor Roadmap](project-loom-development-roadmap)**

## How you can follow the work

The public site will continue to distinguish between:

- **Built** — implemented and demonstrated;
- **In progress** — actively being developed or tested;
- **Planned** — defined work that has not yet been built; and
- **Not yet established** — something Loom does not currently claim to have.

That distinction is intentional. The project is documenting its own development as part of the research record.

*Last updated: September 2026.*
