# How Loom Research Works (v1.0)
**Effective Date:** October 9, 2026  
**Governing Specifications:** PL-307 v1.0, PL-001 v1.1  
**Status:** Active and Mechanically Enforced  

---

## 1. The Core Philosophy
Project Loom is an empirical governance research program. We do not rely on the inherent trustworthiness of AI, nor do we rely on the inherent authority of human reviewers. Instead, we rely on a **mechanically enforced, auditable trail of evidence**.

Our core directive is simple: *We do not call a research finding "working" until our automated validators and human auditors can demonstrate that it behaves exactly as the evidence dictates.*

## 2. The Four Dimensions of Truth
In traditional research, a claim is often just "true" or "false." In Loom, every claim is evaluated across four distinct dimensions to prevent bias and overconfidence:

1. **Workflow Status:** Where is the object in the pipeline? (e.g., `proposed`, `under_review`, `completed`).
2. **Epistemic Status:** What does the evidence actually allow us to say? (e.g., `unknown`, `contested`, `supported`, `known`).
3. **Verification Level:** How deeply has it been checked? (e.g., `source_backed`, `cross_verified`, `primary_verified`).
4. **Promotion Stage:** Has it been formally admitted to the permanent record? (e.g., `candidate`, `accepted`, `canonical`).

*Crucially, a claim cannot be "promoted" just because it is "verified." Promotion is a separate governance decision.*

## 3. The Research Lifecycle
Here is exactly what happens when Loom investigates a topic (like the Flint Water Crisis):

### Step 1: Source Retrieval
We do not accept URLs. A source is only "retrieved" when we have a local copy of the document and have generated a cryptographic hash (SHA-256) of it. If the document changes, the hash changes, and the evidence is invalidated.

### Step 2: Evidence Extraction
We extract specific passages from those documents. 
* If an AI extracts the text, it is capped at a low verification level until a human physically opens the document and confirms the text matches. 
* AI may propose, but evidence must establish.

### Step 3: Claim Formulation
We write atomic claims (one discrete fact per claim). We explicitly define the scope (geography, timeframe) so a claim cannot silently expand to cover things it wasn't proven to cover.

### Step 4: The Mechanical Gate (The Validator)
Before a human ever reviews the claim, our automated Python validator checks it against 23+ strict epistemic rules. 
* *Does it claim to be "known" while having an unresolved contradiction?* **Blocked.**
* *Does it claim "cross_verified" but both sources are from the same publisher?* **Blocked.**
* *Is it a "canonical" claim without a formal promotion event?* **Blocked.**

### Step 5: Human Audit & Governance
Once the validator passes the claim, it enters the human audit queue. 
* To prevent solo-founder bias, our current governance rule requires at least **two designated internal auditors** to independently review and sign off on a claim before it can be promoted to `accepted`. 
* Auditors must disclose their independence distance and sign an agreement. Their reviews are logged as permanent, append-only provenance events.

### Step 6: Publication
Only after the validator passes and the human audit is complete do we generate a Publication Bundle. This bundle includes the claim, the exact evidence excerpts, the source hashes, the full audit trail, and a list of all known system limitations (errata) at the time of publication.

## 4. What Loom Does NOT Do
Transparency requires stating our limits as clearly as our capabilities.

* **Schema validity is not research credibility.** Just because a claim passes our automated checks does not mean it is infallible. It means it meets our structural and epistemic minimums.
* **AI agreement is not evidence.** If an AI model generates a plausible-sounding fact, it is treated as a `proposed` claim with zero verification until a human anchors it to a retrieved source.
* **Canonical is not infallible.** A `canonical` claim is simply one that has passed our highest current governance threshold. If new evidence emerges, the system is designed to trigger a "retraction cascade" and downgrade the claim.

## 5. How to Verify Us
You do not have to take our word for it. Project Loom is built on reproducibility.

1. **View the Code:** Our entire specification, schema, and validator code is open in our GitHub repository.
2. **Inspect the Artifacts:** Every Flint Water Crisis claim, source hash, and auditor signature is stored in machine-readable YAML files.
3. **Run the Validator:** You can clone our repository, install Python, and run our validator yourself. If we have violated our own epistemic rules, the machine will tell you.

---
*This document describes the current operational reality of Project Loom as of v1.0. It is not a roadmap of future intentions.*
