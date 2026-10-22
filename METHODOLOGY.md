# How Loom Research Works
**Version:** 1.1  
**Status:** Active public methodology; implementation claims are qualified  
**Updated:** October 2026

## The basic question

Project Loom investigates what happens between a public decision and the outcome people experience. A policy can be announced or formally adopted without all the authority, resources, people, information, systems, and follow-through needed to carry it out.

Loom studies that gap through cases and evidence. It does not assume in advance that a policy succeeded or failed, and it does not treat a plausible explanation as established merely because it sounds convincing.

> **AI may propose. Evidence must establish. Humans may promote.**

This is both an epistemic rule and a test for the research system itself. The system must not claim to enforce a safeguard until its behavior has been implemented and tested.

## 1. Start with a bounded question

A case begins with a question that can be investigated. Researchers define the policy or decision, the intended outcome, the observed outcome being examined, the relevant institutions, geography and timeframe, and the limits of the inquiry.

The question should leave room for more than one answer. The researcher should identify what evidence could support the initial explanation, what could challenge it, and what would leave the question unresolved.

## 2. Find and retrieve sources

Potential sources include laws and regulations, agency records, budgets, audits, technical reports, court documents, meeting minutes, datasets, official statements, peer-reviewed research, and credible reporting. Which sources matter depends on the case.

A search result or URL is a lead, not evidence by itself. A source is usable as evidence only when its relevant content has been retrieved and can be inspected. Access failures, missing pages, unavailable records, and changes in the source should be recorded rather than silently filled in.

Where an exact captured file or response is available, a cryptographic hash can help identify that particular object and detect later changes. A hash does not prove that the source is truthful, authentic, or correctly interpreted.

## 3. Separate source, evidence, observation, and claim

These are different things:

- **Source:** the document, dataset, record, or other material being examined.
- **Evidence:** a specific passage, data point, or other located material from that source.
- **Observation:** an initial interpretation or pattern noticed during research.
- **Claim:** a bounded statement that can be assessed against evidence.
- **Diagnostic:** an explanation of how or why a mechanism may have contributed to an outcome.

A claim should say one main thing and define the scope that the evidence supports. A broad causal explanation requires more than a source showing that one event occurred.

AI can help locate material, suggest claims, or organize analysis. Its output is a proposal until the relevant underlying evidence has been retrieved and checked. AI agreement is not corroboration.

## 4. Assess evidence and uncertainty

Loom distinguishes four dimensions rather than compressing them into a single status:

| Dimension | Question |
|---|---|
| Workflow status | Where is this object in the review process? |
| Epistemic status | What does the available evidence currently allow us to say? |
| Verification level | What checks have actually been performed? |
| Promotion stage | What is the object's standing in the governed research record? |

A source-backed claim is not automatically cross-verified. Multiple sources are not automatically independent: they may repeat the same report, share an institutional interest, or rely on one underlying source. Primary-source status and independence are also different questions.

Researchers should seek evidence that challenges the emerging explanation, preserve contradictions, and explain how conflicts are assessed. If the record is inadequate, conflicting, or incomplete, “unknown” or “unresolved” may be the correct result. Failure to find a record in one search does not prove that the record does not exist.

## 5. Map the implementation mechanism

After establishing the relevant facts, Loom examines the path between the decision and the outcome. Depending on the case, that can include:

- who had legal or operational authority;
- which actors had to act, and in what order;
- the funding, staffing, technical systems, and administrative capacity required;
- procurement and interagency dependencies;
- what information decision-makers received;
- how monitoring, appeals, warnings, and correction were supposed to work;
- where the observed pathway diverged from the intended one.

The existence of a dependency or a capacity gap does not by itself prove that it caused the outcome. Loom must distinguish observed facts from interpretation, test alternatives, and keep conclusions within the limits of the evidence.

## 6. Validate records and review decisions

Schemas and validators can check whether research objects follow specified structural rules. Those checks are useful, but schema validity is not the same as factual accuracy or research credibility.

Human review should consider source fidelity, claim scope, independence, contradictory evidence, provenance, causal reasoning, and limitations. Where independent review is required, reviewers must actually perform distinct reviews; duplicate entries do not establish independence.

Passing a validator may make an object eligible for review. It does not automatically make a claim true or promote it to the permanent record. Promotion, correction, demotion, and retraction are governance decisions that should be recorded with their rationale.

## 7. Publish the finding and the limits

A public case should help readers understand:

1. what question was investigated;
2. what the evidence supports;
3. what contradicts or complicates the explanation;
4. how the proposed mechanism connects decisions to outcomes;
5. what remains unknown or unverified;
6. what the research system itself has and has not implemented.

The public page should not ask readers to trust a label such as “passed,” “audited,” or “verified” without giving them a meaningful way to inspect what that label represents.

## 8. Keep a correction path

Research can change when a source is corrected, a missing document becomes available, an interpretation is challenged, or a test reveals a system defect. Loom's target design is to preserve a traceable history of verification and correction rather than silently rewriting the record.

The specification and schemas describe parts of this design. Their presence in the repository does not establish that every intended safeguard is already implemented, tested, and satisfied by every case. Each such claim requires implementation evidence.

## Current implementation boundary

Loom has public specifications, schemas, validation code, and a growing research record. The work of validating provenance and review behavior against real artifacts remains important. In particular, placeholder hashes, unretrieved sources, unverified quotations, or incomplete audit records must not be presented as completed cryptographic provenance or independent verification.

The Flint case is therefore being treated as a source-and-provenance audit task before it is represented as a fully reproducible public case artifact. The same rule applies to all future cases.

## How to inspect the work

- Read the [Claims, Epistemic Status, Verification & Promotion Specification](../pl-307/).
- Read the [Evidence and Provenance Model](../evidence-provenance/).
- Read the [Research Protocol](../research-protocol/).
- Read the [Ontology](../ontology/).
- Browse the [public Research Record](../../record/).

The repository is the underlying development record; the Loom website publishes the research documents in a readable form. The governing test remains simple: **do not ask readers to accept more than the evidence and the implementation can support.**
