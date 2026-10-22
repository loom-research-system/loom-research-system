# Evidence and Provenance Model
**Version:** 0.1  
**Status:** Working specification — implementation validation required  
**Applies to:** Sources, evidence, observations, claims, diagnostics, and publication artifacts

## Purpose

This model makes it possible to answer a basic question about any public Loom finding: **what exactly supports this statement, where did that material come from, what checks were performed, and what remains uncertain?**

The model is a specification for the research record. A field in a schema, a hash-shaped string, or a passing structural validator is not by itself proof that a source was retrieved, a quotation is accurate, or a claim is true.

> **AI may propose. Evidence must establish. Humans may promote.**

## 1. The evidence chain

`Source → Evidence → Observation → Claim → Assessment → Governance decision → Publication`

These are different objects and different acts:

- **Source (`SRC`)** — an identifiable document, dataset, record, interview, web archive, or other material that can be examined.
- **Evidence (`EVD`)** — a located excerpt, data point, or other relevant material from a retrieved source. Preserve what the source says separately from Loom's interpretation.
- **Observation** — a preliminary interpretation or pattern noticed while examining evidence. An observation is not a verified claim and does not automatically enter the permanent research record.
- **Claim (`CLM`)** — a bounded, assessable statement. It should say one main thing and specify relevant time, place, population, institution, or other scope.
- **Assessment** — a reasoned evaluation of whether the evidence supports, challenges, or fails to resolve the claim.
- **Governance decision** — a recorded human decision about promotion, rejection, correction, demotion, or retirement.
- **Publication artifact** — the versioned presentation of claims, evidence references, limitations, and review state made available to readers.

A later stage must not erase the distinctions or uncertainty in an earlier stage.

## 2. Retrieval comes before evidentiary use

A discovered link is not a retrieved source. Retrieval requires usable documentary content: for example, a downloaded file, accessible API response, archive snapshot, or captured text whose origin and limitations are recorded.

For each source, record as applicable:

- stable source ID and title;
- publisher/creator and publication date;
- canonical URL or repository location;
- retrieval date and retrieval method;
- source type (primary or secondary);
- whether the source is actually retrieved and inspectable;
- relevant version, archive timestamp, or edition;
- SHA-256 hash of the exact captured object, where that object is available;
- copyright/access status;
- quality assessment and rationale;
- limitations, missing pages, OCR, transcription, or access problems.

If the document was not retrieved, say so. Do not invent an excerpt, page number, hash, or retrieval event to complete a record.

## 3. Evidence records

An evidence record should identify the source and the exact location of the relevant material: page, section, paragraph, table, timestamp, dataset field, or other reproducible locator. It should preserve the excerpt faithfully, including enough surrounding context to avoid changing its meaning.

Record who or what extracted the material and how. Machine-extracted text must be labelled as machine-extracted until a reviewer checks it against the source. An AI-generated quotation is a lead to verify, not evidence in its own right.

The current evidence schema requires an evidence ID, source ID, extracted content, location, retrieval timestamp, document hash, and extractor. These fields define a record shape; they do not guarantee the values are truthful or that the source file is available.

## 4. Verification is not a single yes/no flag

Loom separates four claim dimensions, as defined in PL-307:

- **Workflow status:** where the review process stands.
- **Epistemic status:** what the evidence currently permits Loom to conclude.
- **Verification level:** how the claim was checked.
- **Promotion stage:** its standing in the governed research record.

Use the narrowest description justified by the completed checks:

- `none`: no substantive verification.
- `source_backed`: at least one retrieved source appears to support the claim.
- `cross_verified`: multiple relevant sources were examined and their independence was assessed.
- `primary_verified`: applicable primary documentation was examined.

If a primary source exists but has not been examined, do not claim `primary_verified`. If no applicable primary source exists, record `primary_applicability: not_applicable` with a rationale. “Not found” is not the same as “does not exist.”

AI-assisted extraction or drafting does not establish a claim. Until a human checks the underlying source and confirms that the material supports the stated scope, the claim must not be described as independently source-verified.

## 5. Independence and duplicate detection

Two citations do not necessarily mean two independent sources. Review common authorship, institutional interests, syndication, shared underlying documents, citation chains, and whether one source merely repeats another.

Near-duplicate detection at or above the configured `0.90` similarity threshold should flag material for review; it must not silently delete, merge, or decide the truth of records. Similarity is a review signal, not a judgment of evidentiary independence. The similarity method and version should be recorded when used.

## 6. Contradictions, uncertainty, and absence

Record evidence that challenges a claim alongside supporting evidence. A contradiction must have a status and an explanation; it cannot be resolved merely by choosing the preferred source. Record who assessed the conflict, what criteria were applied, and what evidence would change the conclusion.

Permitted outcomes include supported, contested, unresolved, unknown, or contradicted where the governing specification and schema allow them. An unsuccessful search may support a carefully scoped statement about what was not found in the searched locations and period; it does not establish universal absence.

Diagnostics—such as an explanation that a failure reflects weak self-correction—are interpretations built from claims. A diagnostic cannot be more certain than the weakest material claim on which it depends.

## 7. Provenance and change history

For each material extraction, verification, assessment, promotion, demotion, correction, or retraction, the target design calls for an event recording:

- event ID, action, actor, and timestamp;
- target object and relevant inputs;
- method and rationale;
- result and any required disclosure;
- model/tool identity when automation materially contributed;
- publication location, where applicable.

The intended record is append-only: corrections add a new event and preserve the prior state rather than rewriting history without trace. A correction may supersede a current value, but it should not erase the fact that the earlier value was published or relied upon.

Cryptographic hashes can help detect whether a captured object has changed, provided the exact object and hash are retained and the comparison is performed. A hash alone does not prove who authored a document, whether its contents are true, or whether the original retrieval was authentic.

## 8. Promotion and human accountability

Validation can establish that a record meets specified structural rules. It cannot establish the truth of every statement. Passing validation creates, at most, eligibility for the applicable review or promotion step.

No AI agent may promote its own output. A human promotion decision must be explicit and recorded. Where independent review is required, the record must identify the reviewers and their actual review actions; repeating the same reviewer's name twice is not independent review.

Promotion, correction, demotion, and retraction must be distinguishable events. Public-facing pages should expose the current status and the limits that matter to interpreting the claim.

## 9. Publication requirements

A public research artifact should provide, at minimum:

1. the question and scope;
2. the claims being made;
3. evidence references and precise locations;
4. source retrieval and provenance state;
5. verification and promotion state;
6. material contradictory evidence;
7. method and review history, where available;
8. known limitations, missing records, and unresolved questions;
9. version or date of the published artifact.

Do not label an artifact “verified,” “audited,” “cryptographically proven,” or “independently reviewed” unless the relevant actions and records have actually been checked.

## 10. Current implementation boundary

This document describes the intended evidence/provenance model and requirements to validate. The repository contains YAML schemas and validation code, but the existence of those files does not by itself demonstrate that every requirement above is implemented, tested, and satisfied by every artifact. In particular, public research must not treat placeholder hashes, unretrieved sources, or unverified audit entries as completed provenance.

Implementation status should be upgraded only after the relevant behavior has been tested against real artifacts, including adversarial cases, and the test evidence is available for inspection.

## Related documents

- [PL-307 — Claims, Epistemic Status, Verification & Promotion](../pl-307/)
- [How Loom Research Works](../methodology/)
- [Research Protocol](../research-protocol/)
- [Ontology](../ontology/)
