---
project: Project Loom
artifact_id: PL-101
title: Project Loom Ontology
version: v0.3
status: Working
layer: Knowledge
owner: Project Loom
created: 2026-07-11
updated: 2026-07-11
depends_on:
  - "[[PL-001 Project Loom Charter]]"
supersedes: []
superseded_by: []
related:
  - "[[PL-102 Ontology Change Log]]"
  - "[[PL-201 Loom Analysis Protocol]]"
purpose: Define the canonical vocabulary of Project Loom. Every concept, relationship, and analytical distinction used in the framework is defined here.
scope: The Ontology is the conceptual foundation. All other artifacts—protocols, case studies, specifications—reference these definitions.
---

# Project Loom Ontology

## Version 0.3

---

## Entry 1: Governance

**Concept:** Governance

**Definition:** Governance is the system of institutions, authorities, processes, and relationships through which collective decisions are made, implemented, and enforced. It encompasses the formal structures of government—legislatures, executive agencies, courts—as well as the informal norms, procedural rules, funding flows, and accountability mechanisms that shape how power is exercised and policy is produced.

**Purpose:** Governance is the most general concept in the Project Loom ontology. It names the domain of study. Every other concept—policy, implementation, capacity, debt, dependency—describes a component, property, or dynamic within a governance system.

**Why It Matters:** Without a clear definition of governance, the scope of the project is unbounded. Specifying it as the entire system—institutions, authorities, processes, and relationships—establishes that Project Loom studies the architecture of collective decision-making, not just the actions of particular officials or agencies.

**Relationships:**
- Governance *produces* Policy
- Governance *enables or constrains* Implementation
- Governance *possesses* Governance Capacity
- Governance *accumulates* Implementation Debt
- Governance *contains* Dependency Chains

**Examples:**
- The United States federal governance system, including Congress, the executive branch, federal agencies, the judiciary, state governments, and the procedural rules, funding mechanisms, and accountability relationships connecting them.
- A municipal governance system, including a city council, mayor's office, departments, budgets, public hearings, and procurement processes.
- A university governance system, including a board of trustees, administration, faculty senate, accreditation bodies, and funding sources.

**Non-Examples:**
- A single policy decision (that is a Policy, not Governance).
- A specific agency (that is a component of Governance).
- Political ideology or partisan affiliation.

**Open Questions:**
- Where does governance end and civil society begin?
- How should informal governance mechanisms—lobbying, regulatory capture, political patronage—be modeled?
- Is there a minimum set of institutions required for a system to qualify as "governance"?

**Status:** Stable
**Version:** v0.1

---

## Entry 2: Policy

**Concept:** Policy

**Definition:** A policy is a decision by an authorized actor within a governance system that declares an intention to achieve a specified outcome. Policies take many forms: statutes, executive orders, regulations, agency guidance, court rulings, budget resolutions, and administrative directives. A policy is a statement of intent; it is not the work required to realize that intent.

**Purpose:** Distinguishing policy from implementation is one of the foundational conceptual moves of Project Loom. Implementation debt arises precisely because policies (declarations of intent) are routinely produced without corresponding investment in the capacity to execute them.

**Why It Matters:** Public discourse routinely treats the announcement of a policy as the completion of the work. By defining policy strictly as a decision, Project Loom creates conceptual space to study what happens after the declaration: the implementation pathway, the dependencies, the capacity requirements, and the risks.

**Relationships:**
- Policy *is produced by* Governance
- Policy *requires* Implementation
- Policy *depends on* Institutions, Authorities, and Funding (via Dependency Chains)
- Policy *incurs* Implementation Debt (when declared without sufficient capacity)
- Policy *is constrained by* Governance Capacity

**Examples:**
- The Affordable Care Act (statute).
- Executive Order 14008 on Tackling the Climate Crisis.
- A city council resolution adopting a new zoning code.
- An agency's final rule on emissions standards.

**Non-Examples:**
- The actual construction of a healthcare exchange website (that is Implementation).
- A politician's campaign promise that has not been formalized through any institutional mechanism.
- A court's interpretation of a statute (may affect policy but is a judicial decision, not a policy declaration).

**Open Questions:**
- What is the minimum level of institutional formalization required for something to count as a Policy?
- How should policies that contradict each other be modeled?
- Do policies have a definable "lifespan"?

**Status:** Stable
**Version:** v0.1

---

## Entry 3: Implementation

**Concept:** Implementation

**Definition:** Implementation is the transformation of a policy decision into operational reality. It encompasses all of the administrative, legal, fiscal, technological, and human actions required to execute a policy: rulemaking, procurement, hiring, system development, funding allocation, enforcement, monitoring, and adaptation. Implementation is the operational pathway between a declared intention and a realized outcome.

**Purpose:** If Policy is what governance decides, Implementation is what governance does. Project Loom exists because this distinction is under-theorized and under-documented.

**Why It Matters:** The gap between policy and implementation is where governance succeeds or fails in the lives of citizens. Making implementation visible as a distinct analytical domain is a prerequisite for diagnosing and reducing these failures.

**Relationships:**
- Implementation *realizes* Policy
- Implementation *consumes* Governance Capacity
- Implementation *is constrained by* Dependency Chains
- Implementation *is enabled or obstructed by* Institutions, Funding, Legal Authority, and Personnel
- Implementation *can accumulate* additional Implementation Debt

**Examples:**
- The rulemaking process, public comment period, and system development required to operationalize a new environmental regulation.
- The procurement, hiring, training, and deployment required to staff a new public health program.
- The multi-year process of restructuring a police department under a consent decree.

**Non-Examples:**
- A bill signing ceremony (that is a Policy event, not Implementation).
- A press release announcing a new initiative (communication about Policy).
- A court ruling striking down a regulation (judicial action affecting Policy).

**Open Questions:**
- When does Implementation end?
- How should partial implementation be modeled?
- What is the relationship between Implementation and policy success?

**Status:** Stable
**Version:** v0.1

---

## Entry 4: Governance Capacity

**Concept:** Governance Capacity

**Definition:** Governance capacity is the ability of an institution or governance system to formulate, implement, administer, monitor, and sustain policy effectively and accountably. It is a composite resource comprising multiple domains. Governance capacity is not binary (present or absent) but scalar—it can be adequate, insufficient, degraded, or developing—and it varies across institutions, policy domains, and time.

**Capacity Domains:**

| Domain | Question |
|--------|----------|
| Policy capacity | Can the institution design effective interventions? |
| Legal capacity | Can the institution's authority survive challenge? |
| Administrative capacity | Can the institution manage complex operations? |
| Technical capacity | Can the institution's systems support the required functions? |
| Contractor management capacity | Can the institution effectively oversee external vendors? |
| Financial capacity | Are resources available and allocable? |
| Political capacity | Can the institution sustain support for the intervention? |
| Adaptive capacity | Can the institution diagnose failure and restructure its approach? |

**Why It Matters:** Many governance failures are misdiagnosed as policy design failures or political failures when they are, at root, capacity failures. Capacity analysis makes these constraints visible and actionable. An institution may be strong in some domains and critically weak in others.

**Relationships:**
- Governance *possesses* Governance Capacity
- Governance Capacity *constrains* Implementation
- Governance Capacity *is consumed by* Policy execution
- Governance Capacity *can be built, degraded, or destroyed* by institutional transitions
- Governance Capacity *is related to* Implementation Debt (debt is incurred when policies exceed capacity)

**Examples:**
- A federal agency with a $2 billion appropriation, clear statutory authority, 5,000 trained staff, modern IT systems, and established procurement processes has high governance capacity in its domain.
- A state agency tasked with administering a new unemployment insurance program during a crisis, with outdated mainframe systems, 40% staffing vacancies, and no surge capacity, has critically low governance capacity.

**Non-Examples:**
- Political will (may influence whether capacity is built, but is not capacity itself).
- Funding alone (an input to capacity; an agency can be well-funded and still lack expertise or systems).
- A policy's popularity or public support (political capital, not institutional capacity).

**Open Questions:**
- How should governance capacity be measured?
- Can capacity be aggregated across institutions to produce a system-level assessment?
- What is the relationship between governance capacity and institutional resilience?

**Status:** Stable (core definition); Working (domains subject to further testing)
**Version:** v0.3

**References:** [[PL-402 Case Study 001|Case Study #001]], [[PL-403 Case Study 002|Case Study #002]]

---

## Entry 5: Implementation Debt

**Concept:** Implementation Debt

**Definition:** Implementation debt is the accumulated mismatch between institutional architecture and the demands placed upon it, whether those demands arise from specific policy commitments or from the structural complexity of the governance system itself. Like technical debt in software engineering, implementation debt compounds over time: each new policy introduced without corresponding investment in administrative capacity increases the complexity, fragility, and cost of all future implementation efforts. Implementation debt exists before the stress event that reveals it.

**Common Forms (non-exhaustive):**

| Debt Type | Description | Case Example |
|-----------|-------------|--------------|
| Legal debt | Unresolved questions about the scope of authority | Student Loan Forgiveness |
| Procurement debt | Dependency structures that lack internal verification or replacement capability | Healthcare.gov |
| Timeline debt | Schedule compression without corresponding margin or scope adjustment | Healthcare.gov |
| Testing debt | Deferred or incomplete verification of system readiness | Healthcare.gov |
| Oversight debt | Reliance on information sources that cannot be independently verified | Healthcare.gov |
| Data debt | Fragmented, inaccessible, or unverified information required for execution | Student Loan Forgiveness |
| Institutional debt | Accumulated administrative complexity from prior policy layers | Both cases |

**Why It Matters:** Implementation debt explains a recurring pattern in governance: ambitious reforms are announced, implementation falters, public trust declines, and the next round of reforms begins from an even weaker institutional foundation. The concept reframes governance failure not as a series of discrete mistakes but as a compounding structural