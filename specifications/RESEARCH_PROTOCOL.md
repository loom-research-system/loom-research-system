# Project Loom Research Protocol
**Version:** 0.1  
**Status:** Draft for implementation and case-level validation  
**Purpose:** Establish a repeatable way to investigate what happens between a governance decision and the outcome people experience.

This protocol is a public working method. It should not be described as fully implemented or independently validated until the required steps, records, and tests are demonstrated on real research artifacts.

## 1. Define the question before collecting evidence

Write a research question that can be investigated and specify:

- the policy, program, or institutional decision under study;
- the intended outcome and the observed outcome, without assuming they differ;
- the jurisdiction, organizations, population, and timeframe;
- the unit of analysis and what is outside scope;
- the candidate mechanisms to investigate;
- what evidence would support, weaken, or falsify the initial explanation.

Avoid framing the question so that only one conclusion can count as success. Where practical, record the initial question and scope before drawing conclusions.

## 2. Create a search and retrieval protocol

Record a protocol ID, title, scope, creator, creation date, databases or repositories searched, exact query strings, date range, inclusion criteria, and exclusion criteria. Also record the date each search was run, the results or records screened, access failures, and changes to the search plan.

Searches should be appropriate to the case. Potential source classes include primary legal instruments, agency records, budgets, audits, technical reports, court records, meeting minutes, datasets, public statements, peer-reviewed research, and credible investigative reporting. The list is a menu, not a claim that every source class has been searched.

A search result or URL is a discovery lead. It becomes a usable source only after its relevant content has been retrieved and can be inspected. If access fails, record the failure rather than substituting an imagined quotation or an unverified summary.

## 3. Build a source register

For each relevant source, record a stable ID, title, author or publisher, date, source type, URL or location, retrieval state, retrieval method and date, source quality assessment, independence considerations, access/copyright status, and object hash where a captured object is available.

Distinguish:
- primary source from independent source;
- official statement from independently established fact;
- a source's assertion from the truth of that assertion;
- source discovery from source retrieval;
- original reporting from repetition or syndication.

No number of derivative sources automatically creates independent corroboration.

## 4. Extract evidence without changing its meaning

Create evidence records with source IDs and exact locations. Preserve relevant context and distinguish direct quotation, paraphrase, data extraction, OCR, and model-generated suggestions.

A human reviewer must compare AI-assisted extraction against the underlying retrieved source before it is treated as human-confirmed. Keep extraction errors and corrections visible. Record missing pages, OCR uncertainty, unavailable attachments, and other limitations that could affect interpretation.

## 5. Form bounded claims

Each claim should express one main proposition and specify the relevant time, place, actor, population, or conditions. Link the claim to supporting evidence and, where relevant, contradictory evidence.

Ask:
- Is this a factual claim, an interpretation, or a causal explanation?
- Does the cited evidence support the exact wording and scope?
- Does the claim overgeneralize beyond the source?
- What plausible evidence would contradict it?
- Is the statement actually unknown because the available record is incomplete?

Keep observations distinct from claims. A diagnostic explanation should link to the claims on which it depends and must not imply more certainty than those claims support.

## 6. Assess evidence and contradictions

Assess source quality, relevance, limitations, and independence. Search deliberately for disconfirming evidence and institutional or stakeholder perspectives that challenge the emerging explanation. Record contradictory evidence structurally; do not discard it because it complicates the narrative.

Use epistemic language proportionate to the record: proposed, unknown, unresolved, contested, supported, or known, as applicable under PL-307. “Known” is a restricted category, not a stylistic synonym for confidence. Record why a contradiction is considered resolved, if it is, and what would reopen the question.

Near-duplicate detection may flag possible repeated material for review. A similarity score alone does not establish source independence or factual correctness.

## 7. Map the implementation mechanism

After establishing the relevant facts, map the path from policy to outcome:

- formal decision and stated purpose;
- legal and institutional authority;
- responsible actors and handoffs;
- funding, staffing, technical and administrative capacity;
- procurement, information and system dependencies;
- sequencing and timing constraints;
- monitoring, feedback, appeal and correction channels;
- observed divergence, failure points, and alternative explanations.

Do not treat the existence of a dependency as proof that it caused the outcome. State the mechanism hypothesis and identify what evidence would distinguish it from alternatives.

## 8. Validate and review

Structural validation checks whether records satisfy specified schema and cross-object rules. It does not independently establish truth. Record validator version, test result, and any exceptions.

Human review should examine source fidelity, claim scope, contradiction handling, causal reasoning, provenance completeness, and limits. Where the governing rule requires independent reviewers, independence must be real and documented; duplicate entries by one reviewer do not satisfy that requirement.

The current repository contains schemas and validator code, but this protocol's full set of requirements must be tested against real artifacts before Loom can claim that every step is mechanically enforced.

## 9. Decide whether to publish or promote

Validation and review create eligibility for a decision; they do not automatically promote a claim. Record the decision-maker, action, timestamp, rationale, applicable evidence, and resulting status.

A public case artifact should separate:
- what the record supports;
- what remains disputed or unknown;
- the diagnostic interpretation;
- the alternative explanations considered;
- the limitations and gaps;
- the implementation and verification state of Loom's own tools.

Do not describe a case as fully audited, cryptographically verified, or independently reviewed unless those actions are evidenced in the record.

## 10. Preserve corrections and reproducibility

When a source, claim, or diagnosis changes, preserve the prior published state and add a traceable correction, demotion, retraction, or supersession event. Document why the change occurred and which downstream claims or conclusions may be affected.

A reproducibility package should identify the artifact version, source list, evidence locations, hashes of available captured objects, protocol and validator versions, decisions, known limitations, and steps needed to repeat the checks. Public availability must respect legal, privacy, and safety constraints.

## 11. Report null results and limits

Record failed searches, inaccessible records, evidence that did not support the initial hypothesis, and cases where the mechanism could not be resolved. Do not convert absence of located evidence into proof of absence unless the search design and evidence support that narrower conclusion.

The protocol is successful when another researcher can understand what was asked, what was searched, what was found, how claims were evaluated, where uncertainty remains, and how the conclusions could be challenged.

## Related documents

- [Evidence and Provenance Model](../evidence-provenance/)
- [Ontology](../ontology/)
- [PL-307 — Claims, Epistemic Status, Verification & Promotion](../pl-307/)
- [How Loom Research Works](../methodology/)
