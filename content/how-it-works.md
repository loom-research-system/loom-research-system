---
title: "How Loom Works"
date: 2026-10-09
tags: [methodology, how-it-works]
---

# How Loom Works

Loom is building an unusually rigorous system for answering a simple question: *Why did a policy fail, and was it actually the policy that failed?*

We do this by breaking every investigation down into five steps.

---

### 1. What was supposed to happen?
We identify the actual policy, decision, promise, law, regulation, or program. We establish the baseline intent before the implementation began.

### 2. What actually happened?
We reconstruct the timeline of events after the decision was made. We look at the real-world outcomes, not the press releases.

### 3. Who had to make it happen?
We trace the institutions, officials, agencies, contractors, systems, and other dependencies involved. A decision is only as good as the capacity of the people tasked with executing it.

### 4. Where did things diverge?
We look for the specific point where implementation departed from the intended outcome. Was it a lack of funding? A technological failure? A deliberate choice by an agency? 

### 5. How do we know?
This is where Loom's evidence system comes in. 

We do not ask an AI what happened and publish the answer. AI can help us find and organize information, but **evidence must establish the claim.** 

- **Sources are retrieved and hashed.** We don't just link to a URL; we download the document and generate a cryptographic hash. If the document changes, we know.
- **Claims are tied to evidence.** Every statement is linked to a specific page and paragraph in a retrieved source.
- **Contradictions are recorded.** If sources disagree, we don't hide it. We flag it as "unresolved" or document exactly how it was resolved.
- **Verification has to be earned.** A claim cannot be marked "Supported" or "Canonical" until it has been cross-verified by independent sources and reviewed by a human auditor.

---

## Show Your Work

When you read a Loom case study, you will see statements like:
> *"The agency had authority to implement the program, but did not have the capacity required to do so."*

Next to that statement, you can click **"Trace the Evidence."** 

This opens a layer that shows you exactly how we know that:
1. The specific **Claim** ID.
2. The **Epistemic Status** (e.g., *Supported, Cross-verified, Human Reviewed*).
3. The exact **Evidence** excerpt and its location (e.g., *Page 12, Paragraph 3*).
4. The **Source** document title, publisher, and SHA-256 cryptographic hash.
5. The **Audit Log** showing which human reviewer verified it and when.

The technical system is experienced *through* the research. We don't hide the machinery; we simply put it behind the question that made you care in the first place.
