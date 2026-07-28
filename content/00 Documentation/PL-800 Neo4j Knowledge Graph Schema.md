---
title: Neo4j Knowledge Graph Schema
project: Project Loom
artifact_id: PL-800
status: Draft
layer: Infrastructure
purpose: Graph database schema for modeling governance entities, cases, and relationships
---

# Neo4j Knowledge Graph Schema for Project Loom

## Overview

This schema maps Project Loom's empirical research into a graph database (Neo4j), enabling:
- **Relationship analytics** across cases, actors, and concepts
- **Pattern detection** in governance failure and success
- **Intervention simulation** (what happens if we remove/add a node?)
- **Cross-domain comparison** via graph algorithms

The graph is designed to mirror Loom's ontology while adding the relational richness that markdown files cannot easily express.

---

## Node Types

### 1. CaseStudy
A documented governance episode analyzed through the Loom protocol.

| Property | Type | Description |
|----------|------|-------------|
| `case_id` | String | Unique ID (e.g., "PL-401") |
| `title` | String | Full case title |
| `slug` | String | URL-safe identifier |
| `domain` | String | Policy domain (health, environment, immigration, etc.) |
| `governance_level` | String | federal, state, local, multi_level |
| `date_start` | Date | Start of case period |
| `date_end` | Date | End of case period (or NULL if ongoing) |
| `outcome_classification` | String | success, partial_success, implementation_failure, design_failure, governance_failure |
| `implementation_debt_level` | String | low, moderate, high, critical |
| `summary` | String | One-paragraph case summary |
| `source_url` | String | Link to full case study markdown |

**Constraints:**
```cypher
CREATE CONSTRAINT case_id_unique IF NOT EXISTS
FOR (c:CaseStudy) REQUIRE c.case_id IS UNIQUE;
```

---

### 2. Concept
An ontology concept from the Loom framework.

| Property | Type | Description |
|----------|------|-------------|
| `concept_id` | String | Unique ID (e.g., "CONCEPT-001") |
| `name` | String | Canonical name |
| `slug` | String | URL-safe identifier |
| `category` | String | fragility, capacity, debt, alignment, outcome |
| `status` | String | candidate, supported, strengthened, deprecated |
| `definition` | String | Canonical definition |
| `operationalization` | String | How the concept is measured/tested |

**Constraints:**
```cypher
CREATE CONSTRAINT concept_id_unique IF NOT EXISTS
FOR (c:Concept) REQUIRE c.concept_id IS UNIQUE;
```

**Seed Data (Core Concepts):**
```cypher
CREATE (c1:Concept {concept_id: "CONCEPT-001", name: "Implementation Debt", category: "debt", status: "supported", definition: "Accumulated mismatch between political ambition and institutional capacity.", operationalization: "Measured by gap between policy mandate and institutional capability to execute."})
CREATE (c2:Concept {concept_id: "CONCEPT-002", name: "Governance Fragility", category: "fragility", status: "supported", definition: "Vulnerability to disruption by external actors or events.", operationalization: "Assessed by number and criticality of single points of failure."})
CREATE (c3:Concept {concept_id: "CONCEPT-003", name: "Self-Correction Fragility", category: "fragility", status: "supported", definition: "Inability of institutions to convert failure information into corrective action.", operationalization: "Tested by presence/absence of mechanism to act on known failures."})
CREATE (c4:Concept {concept_id: "CONCEPT-004", name: "Veto Fragility", category: "fragility", status: "supported", definition: "Susceptibility to unilateral termination by a single actor.", operationalization: "Count of actors who could terminate the intervention and whether they did."})
CREATE (c5:Concept {concept_id: "CONCEPT-005", name: "Execution Fragility", category: "fragility", status: "supported", definition: "Susceptibility to operational breakdown due to missing dependencies.", operationalization: "Dependency chain analysis for critical path failures."})
CREATE (c6:Concept {concept_id: "CONCEPT-006", name: "Assembled Capacity", category: "capacity", status: "supported", definition: "Capacity intentionally created for a specific intervention.", operationalization: "Distinguish temporary vs. permanent; measure survival across transitions."})
CREATE (c7:Concept {concept_id: "CONCEPT-007", name: "Mechanism-Purpose Alignment", category: "alignment", status: "supported", definition: "Degree to which enforceable architecture matches deep policy objective.", operationalization: "Compare stated purpose with actual mechanism design and incentives."})
CREATE (c8:Concept {concept_id: "CONCEPT-008", name: "Chronic Partial Implementation", category: "outcome", status: "supported", definition: "Permanent state where announced policies never fully materialize.", operationalization: "Measured by persistent gap between authorization and outcome across time."})
CREATE (c9:Concept {concept_id: "CONCEPT-009", name: "Dependency Concentration", category: "fragility", status: "candidate", definition: "Over-reliance on a single node in a dependency network.", operationalization: "Graph centrality metrics on dependency chains."})
CREATE (c10:Concept {concept_id: "CONCEPT-010", name: "Governance Epistemology", category: "capacity", status: "strengthened", definition: "How institutions know what they know and whether they can act on it.", operationalization: "Compare information availability with action taken."})
```

---

### 3. Actor
An institutional entity with formal or effective authority.

| Property | Type | Description |
|----------|------|-------------|
| `actor_id` | String | Unique ID (e.g., "ACTOR-001") |
| `name` | String | Canonical name |
| `type` | String | executive, legislative, judicial, agency, state_local, private, ngo, court |
| `branch` | String | executive, legislative, judicial, none |
| `level` | String | federal, state, local, multi_level |
| `description` | String | Role in governance system |

---

### 4. Policy
A specific statute, executive order, regulation, or program.

| Property | Type | Description |
|----------|------|-------------|
| `policy_id` | String | Unique ID (e.g., "POL-001") |
| `name` | String | Full name |
| `type` | String | statute, executive_order, regulation, program, court_order, settlement |
| `citation` | String | Legal citation (e.g., "INA § 287", "42 U.S.C. § 7401") |
| `status` | String | active, repealed, amended, blocked, proposed |
| `date_enacted` | Date | Date of enactment |
| `description` | String | What the policy does |

---

### 5. Intervention
A specific action taken within a case study.

| Property | Type | Description |
|----------|------|-------------|
| `intervention_id` | String | Unique ID |
| `name` | String | Short name |
| `type` | String | legislative, executive, judicial, organizational, operational |
| `lever` | String | Which EROS lever (if applicable) |
| `description` | String | What was done |
| `date_start` | Date | When it started |
| `date_end` | Date | When it ended (or NULL) |

---

### 6. Domain
A policy domain or sector.

| Property | Type | Description |
|----------|------|-------------|
| `domain_id` | String | Unique ID |
| `name` | String | Domain name |
| `description` | String | Scope of domain |

---

### 7. Outcome
A measurable result or state.

| Property | Type | Description |
|----------|------|-------------|
| `outcome_id` | String | Unique ID |
| `description` | String | What happened |
| `type` | String | intended, unintended, counterfactual |
| `magnitude` | String | complete, partial, negligible, reversed |

---

### 8. CapacityDebt
A specific capacity gap or debt instance.

| Property | Type | Description |
|----------|------|-------------|
| `debt_id` | String | Unique ID |
| `type` | String | technical, administrative, coordination, talent, procurement |
| `description` | String | Nature of the debt |
| `severity` | String | low, moderate, high, critical |

---

## Relationship Types

### CaseStudy → Concept
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `EXHIBITS` | Case demonstrates this concept | `strength`: strong, moderate, weak; `direction`: positive, negative |
| `TESTS` | Case was designed to test this concept | `hypothesis`: String; `result`: supported, rejected, inconclusive |
| `BLOCKS` | Case demonstrates failure of this concept | `mechanism`: String |
| `VALIDATES` | Case provides supporting evidence | `evidence_level`: A, B, C, D |

### CaseStudy → Actor
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `INVOLVES` | Actor participated in case | `role`: primary, supporting, blocking; `authority_type`: authorization, budget, intervention, sustaining |
| `AUTHORIZED` | Actor gave legal authority | `instrument`: String |
| `VETOED` | Actor blocked or terminated | `veto_type`: political, legal, administrative; `date`: Date |
| `IMPLEMENTED` | Actor carried out intervention | `compliance`: full, partial, nominal |

### CaseStudy → Policy
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `GOVERNED_BY` | Case operates under this policy | `binding`: true, false |
| `CREATED` | Case led to creation of policy | `date`: Date |
| `REPEALED` | Case led to repeal of policy | `date`: Date |

### CaseStudy → Intervention
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `CONTAINS` | Case includes this intervention | `stage`: String; `sequence`: Integer |

### CaseStudy → Domain
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `IN_DOMAIN` | Case belongs to domain | `primary`: true, false |

### CaseStudy → Outcome
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `PRODUCES` | Case produced this outcome | `expected`: true, false |

### CaseStudy → CapacityDebt
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `ACCUMULATES` | Case accumulated this debt | `pre_existing`: true, false |
| `REDUCES` | Case reduced this debt | `mechanism`: String |

### Actor → Actor
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `OVERSEES` | Hierarchical oversight | `formal`: true, false |
| `FUNDS` | Financial flow | `amount`: Float; `instrument`: String |
| `DEPENDS_ON` | Operational dependency | `criticality`: high, medium, low |
| `COLLABORATES_WITH` | Cooperative relationship | `formalized`: true, false; `instrument`: String |
| `CONSTRAINS` | Limits authority or action | `mechanism`: String |

### Actor → Policy
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `AUTHORS` | Created or drafted | `role`: primary, co-author |
| `ENFORCES` | Responsible for enforcement | `capacity_adequate`: true, false |
| `COMPLIES_WITH` | Subject to policy | `compliance_level`: full, partial, nominal |
| `CHALLENGES` | Legal or political challenge | `status`: pending, resolved, dismissed |

### Policy → Policy
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `AMENDS` | Modifies prior policy | `scope`: narrow, broad |
| `REPEALS` | Nullifies prior policy | `date`: Date |
| `DEPENDS_ON` | Requires other policy to function | `critical`: true, false |
| `CONFLICTS_WITH` | Legal or operational contradiction | `resolution`: String |

### Intervention → Actor
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `EXECUTED_BY` | Actor carried out | `compliance`: full, partial |
| `REQUIRES` | Needs actor participation | `mandatory`: true, false |

### Intervention → Policy
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `AUTHORIZED_BY` | Legal basis | `binding`: true, false |
| `CREATES` | Generates new policy | `type`: String |

### Concept → Concept
| Relationship | Meaning | Properties |
|--------------|---------|------------|
| `SUBSUMES` | Broader concept includes narrower | `direction`: unidirectional, bidirectional |
| `CONTRASTS_WITH` | Negative case relationship | `basis`: String |
| `CORRELATES_WITH` | Statistical or observed association | `strength`: strong, moderate, weak |

---

## Indexes for Performance

```cypher
// Case lookups
CREATE INDEX case_domain_idx IF NOT EXISTS
FOR (c:CaseStudy) ON (c.domain);

CREATE INDEX case_outcome_idx IF NOT EXISTS
FOR (c:CaseStudy) ON (c.outcome_classification);

// Actor lookups
CREATE INDEX actor_type_idx IF NOT EXISTS
FOR (a:Actor) ON (a.type);

CREATE INDEX actor_level_idx IF NOT EXISTS
FOR (a:Actor) ON (a.level);

// Policy lookups
CREATE INDEX policy_status_idx IF NOT EXISTS
FOR (p:Policy) ON (p.status);

CREATE INDEX policy_type_idx IF NOT EXISTS
FOR (p:Policy) ON (p.type);

// Concept lookups
CREATE INDEX concept_category_idx IF NOT EXISTS
FOR (c:Concept) ON (c.category);

CREATE INDEX concept_status_idx IF NOT EXISTS
FOR (c:Concept) ON (c.status);

// Full-text search
CREATE FULLTEXT INDEX case_search_idx IF NOT EXISTS
FOR (c:CaseStudy) ON EACH [c.title, c.summary];

CREATE FULLTEXT INDEX concept_search_idx IF NOT EXISTS
FOR (c:Concept) ON EACH [c.name, c.definition];
```

---

## Example Cypher Queries

### 1. Find all cases that exhibit high Implementation Debt
```cypher
MATCH (c:CaseStudy)-[r:EXHIBITS]->(concept:Concept {name: "Implementation Debt"})
WHERE r.strength = "strong"
RETURN c.case_id, c.title, c.domain, c.outcome_classification
ORDER BY c.date_start;
```

### 2. Map the actor network for a specific case
```cypher
MATCH (c:CaseStudy {case_id: "PL-410"})-[r:INVOLVES]->(a:Actor)
OPTIONAL MATCH (a)-[r2:DEPENDS_ON|FUNDS|OVERSEES|COLLABORATES_WITH]->(a2:Actor)
RETURN a.name, a.type, r.role, r.authority_type,
       collect(DISTINCT {related: a2.name, rel_type: type(r2)}) as connections
ORDER BY r.role;
```

### 3. Find cases where Self-Correction failed (contrast with USDS)
```cypher
MATCH (c:CaseStudy)-[r:BLOCKS]->(concept:Concept {name: "Self-Correction Fragility"})
MATCH (c)-[:IN_DOMAIN]->(d:Domain)
RETURN c.case_id, c.title, d.name, c.outcome_classification, r.mechanism
ORDER BY c.date_start;
```

### 4. Dependency chain analysis: what breaks if an actor is removed?
```cypher
// Simulate removing ICE
MATCH path = (ice:Actor {name: "Immigration and Customs Enforcement"})-[*1..4]-(dependent)
WHERE dependent <> ice
RETURN [node in nodes(path) | node.name] as chain,
       [rel in relationships(path) | type(rel)] as rel_types
LIMIT 50;
```

### 5. Cross-case concept validation matrix
```cypher
MATCH (c:CaseStudy)-[r:EXHIBITS|TESTS|VALIDATES]->(concept:Concept)
WHERE concept.status IN ["supported", "strengthened"]
RETURN concept.name,
       count(DISTINCT CASE WHEN r.result = "supported" THEN c.case_id END) as supporting_cases,
       count(DISTINCT CASE WHEN r.result = "rejected" THEN c.case_id END) as rejecting_cases,
       count(DISTINCT c) as total_cases
ORDER BY supporting_cases DESC;
```

### 6. Find all policies that depend on a policy targeted for repeal
```cypher
// Simulate repealing INA § 287
MATCH (target:Policy {citation: "INA § 287"})<-[:DEPENDS_ON]-(dependent:Policy)
OPTIONAL MATCH (dependent)-[:GOVERNS_BY]->(c:CaseStudy)
RETURN dependent.name, dependent.citation, dependent.status,
       collect(DISTINCT c.title) as affected_cases;
```

### 7. Graph algorithm: PageRank on actors by case involvement
```cypher
CALL gds.graph.project(
  "actor-case-graph",
  ["Actor", "CaseStudy"],
  {
    INVOLVES: {orientation: "UNDIRECTED"}
  }
)
YIELD graphName, nodeCount, relationshipCount;

CALL gds.pageRank.stream("actor-case-graph")
YIELD nodeId, score
MATCH (n) WHERE id(n) = nodeId AND n:Actor
RETURN n.name, n.type, score
ORDER BY score DESC
LIMIT 20;
```

### 8. Find shortest path between two cases through shared concepts
```cypher
MATCH (c1:CaseStudy {case_id: "PL-407"}), (c2:CaseStudy {case_id: "PL-410"})
MATCH path = shortestPath(
  (c1)-[:EXHIBITS|TESTS|BLOCKS|VALIDATES*]-(c2)
)
RETURN [node in nodes(path) | 
  CASE 
    WHEN node:CaseStudy THEN node.case_id + ": " + node.title
    WHEN node:Concept THEN "CONCEPT: " + node.name
    ELSE coalesce(node.name, "")
  END
] as path_nodes;
```

### 9. Intervention lever coverage analysis (for ICE abolition)
```cypher
MATCH (i:Intervention)
WHERE i.lever IS NOT NULL
OPTIONAL MATCH (i)-[:EXECUTED_BY]->(a:Actor)
OPTIONAL MATCH (i)-[:AUTHORIZED_BY]->(p:Policy)
RETURN i.lever,
       count(DISTINCT i) as intervention_count,
       collect(DISTINCT a.name) as actors,
       collect(DISTINCT p.citation) as legal_basis
ORDER BY intervention_count DESC;
```

### 10. Temporal fragility: cases by duration and outcome
```cypher
MATCH (c:CaseStudy)
WHERE c.date_start IS NOT NULL AND c.date_end IS NOT NULL
WITH c, duration.between(c.date_start, c.date_end).years as years
RETURN years,
       count(c) as case_count,
       collect(c.outcome_classification) as outcomes
ORDER BY years;
```

---

## Data Ingestion Pipeline

### From Obsidian Vault to Neo4j

```python
# Pseudocode for ingestion script
import frontmatter
import glob
from neo4j import GraphDatabase

def ingest_case_studies(vault_path, neo4j_uri, neo4j_auth):
    driver = GraphDatabase.driver(neo4j_uri, auth=neo4j_auth)

    for filepath in glob.glob(f"{vault_path}/content/03 Permanent Notes/PL-4*.md"):
        with open(filepath) as f:
            post = frontmatter.load(f)

        # Extract frontmatter
        case_id = post.get("artifact_id", "")
        title = post.get("title", "")
        domain = post.get("domain", "")

        # Create CaseStudy node
        with driver.session() as session:
            session.run("""
                MERGE (c:CaseStudy {case_id: $case_id})
                SET c.title = $title,
                    c.domain = $domain,
                    c.summary = $summary
            """, case_id=case_id, title=title, domain=domain, 
                 summary=post.content[:500])

            # Extract concepts from content
            concepts = extract_concepts(post.content)  # Custom parser
            for concept in concepts:
                session.run("""
                    MATCH (c:CaseStudy {case_id: $case_id})
                    MERGE (concept:Concept {name: $concept_name})
                    MERGE (c)-[r:EXHIBITS]->(concept)
                    SET r.strength = $strength
                """, case_id=case_id, concept_name=concept["name"],
                     strength=concept["strength"])

    driver.close()
```

---

## Schema Evolution Rules

1. **Never delete a Concept node** — deprecate it and create a `SUPERSEDED_BY` relationship
2. **CaseStudy nodes are immutable** after publication — corrections create new versions
3. **Actor nodes are canonical** — use standard names (e.g., "Department of Homeland Security" not "DHS" in primary label; add aliases as properties)
4. **Policy nodes track status changes** via relationship timestamps, not property overwrites
5. **All relationships should have a `source` property** pointing to the case study or document that justifies them

---

## Next Steps

1. **Deploy Neo4j** — Neo4j Aura (cloud) or local Docker instance
2. **Seed concepts** — Run the concept seed Cypher above
3. **Ingest first 3 cases** — PL-401, PL-403, PL-407 (diverse outcomes)
4. **Build queries** — Start with simple lookups, progress to graph algorithms
5. **Visualize** — Bloom or custom D3.js for public-facing dependency maps
6. **Sync pipeline** — Automate Obsidian → Neo4j ingestion on git push

---

*Schema version: 0.1 • Last updated: 2026-07-27 • Artifact: PL-800*
