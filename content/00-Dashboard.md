---
title: Dashboard
description: Navigation hub and project status for Project Loom
---

<style>
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}
.dashboard-card {
  border: 1px solid var(--gray);
  border-radius: 8px;
  padding: 1.25rem;
  background: var(--light);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.dashboard-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.dashboard-card h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
  border-bottom: 2px solid var(--secondary);
  padding-bottom: 0.4rem;
}
.dashboard-card ul {
  margin: 0.5rem 0 0 0;
  padding-left: 1.2rem;
}
.dashboard-card li {
  margin-bottom: 0.35rem;
}
.status-badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.status-live { background: #d4edda; color: #155724; }
.status-draft { background: #fff3cd; color: #856404; }
.status-wip { background: #cce5ff; color: #004085; }
.status-review { background: #f8d7da; color: #721c24; }
.metric-row {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  margin: 1rem 0;
}
.metric {
  text-align: center;
  min-width: 100px;
}
.metric-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--secondary);
  line-height: 1;
}
.metric-label {
  font-size: 0.8rem;
  color: var(--darkgray);
  margin-top: 0.25rem;
}
</style>

# Project Loom Dashboard

<div class="metric-row">
  <div class="metric">
    <div class="metric-number">9</div>
    <div class="metric-label">Case Studies</div>
  </div>
  <div class="metric">
    <div class="metric-number">12</div>
    <div class="metric-label">Ontology Concepts</div>
  </div>
  <div class="metric">
    <div class="metric-number">3</div>
    <div class="metric-label">Administrations</div>
  </div>
  <div class="metric">
    <div class="metric-number">6</div>
    <div class="metric-label">Framework Stages</div>
  </div>
</div>

---

## Navigate by Category

<div class="dashboard-grid">

<div class="dashboard-card">
<h3>📋 Case Studies</h3>
<p>Ten-stage diagnostic analyses of governance outcomes.</p>
<ul>
<li><a href="03-permanent-notes/pl-401-case-study-001">PL-401: Student Loan Forgiveness</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-403-case-study-002">PL-403: Healthcare.gov</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-404-case-study-003">PL-404: Cash for Clunkers</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-405-case-study-004">PL-405: Acid Rain Program</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-406-case-study-005">PL-406: Operation Warp Speed</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-407-case-study-006">PL-407: Flint Water Crisis</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-408-case-study-007">PL-408: Tobacco Master Settlement</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-409-case-study-008">PL-409: California High-Speed Rail</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-410-case-study-009">PL-410: USDS</a> <span class="status-badge status-live">Live</span></li>
</ul>
</div>

<div class="dashboard-card">
<h3>🧬 Ontology</h3>
<p>Canonical definitions and relationships.</p>
<ul>
<li><a href="03-permanent-notes/pl-101-project-loom-ontology">Core Ontology</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-105-ontology-evolution-log">Evolution Log</a> <span class="status-badge status-wip">WIP</span></li>
<li><a href="03-permanent-notes/pl-102-implementation-debt">Implementation Debt</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-103-governance-fragility">Governance Fragility</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-104-self-correction-fragility">Self-Correction Fragility</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-106-mechanism-purpose-alignment">Mechanism-Purpose Alignment</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-107-chronic-partial-implementation">Chronic Partial Implementation</a> <span class="status-badge status-live">Live</span></li>
</ul>
</div>

<div class="dashboard-card">
<h3>🔧 Frameworks</h3>
<p>Methodologies and analytical tools.</p>
<ul>
<li><a href="03-permanent-notes/pl-201-loom-analysis-protocol">Loom Analysis Protocol</a> <span class="status-badge status-live">Live</span></li>
<li><a href="03-permanent-notes/pl-202-eros-governance-analysis-framework">EROS Framework</a> <span class="status-badge status-wip">WIP</span></li>
<li><a href="03-permanent-notes/pl-203-dependency-chain-mapping">Dependency Chain Mapping</a> <span class="status-badge status-draft">Draft</span></li>
<li><a href="03-permanent-notes/pl-204-capacity-assessment-rubric">Capacity Assessment Rubric</a> <span class="status-badge status-draft">Draft</span></li>
</ul>
</div>

<div class="dashboard-card">
<h3>🚀 Projects & Outputs</h3>
<p>Active research and public-facing work.</p>
<ul>
<li><a href="04-projects/pl-600-ice-abolition-architecture">ICE Abolition Architecture</a> <span class="status-badge status-wip">WIP</span></li>
<li><a href="05-outputs/pl-000-intro-autopsy-of-a-vanishing">Autopsy of a Vanishing</a> <span class="status-badge status-draft">Draft</span></li>
<li><a href="05-outputs/pl-700-eros-white-paper">EROS White Paper 0.1</a> <span class="status-badge status-draft">Draft</span></li>
<li><a href="04-projects/pl-800-neo4j-knowledge-graph">Neo4j Knowledge Graph</a> <span class="status-badge status-review">Planned</span></li>
</ul>
</div>

<div class="dashboard-card">
<h3>📚 Literature & Sources</h3>
<p>Research material and theoretical foundations.</p>
<ul>
<li><a href="02-literature-notes">Literature Notes Index</a></li>
<li><a href="02-literature-notes/lit-001-francis-fukuyama-state-building">Fukuyama — State Building</a></li>
<li><a href="02-literature-notes/lit-002-james-scott-seeing-like-a-state">Scott — Seeing Like a State</a></li>
<li><a href="02-literature-notes/lit-003-daniel-carpenter-forging-bureaucratic-autonomy">Carpenter — Bureaucratic Autonomy</a></li>
<li><a href="02-literature-notes/lit-004-mariana-mazzucato-mission-economy">Mazzucato — Mission Economy</a></li>
</ul>
</div>

<div class="dashboard-card">
<h3>⚙️ Meta & Documentation</h3>
<p>Project operations and standards.</p>
<ul>
<li><a href="00-documentation/documentation-getting-started">Getting Started</a></li>
<li><a href="00-documentation/documentation-style-guide">Style Guide</a></li>
<li><a href="00-documentation/documentation-naming-conventions">Naming Conventions</a></li>
<li><a href="00-documentation/documentation-git-workflow">Git Workflow</a></li>
<li><a href="00-documentation/pl-000-session-memorial">Session Memorial</a></li>
</ul>
</div>

</div>

---

## Cross-Cutting Views

| View | Description | Link |
|------|-------------|------|
| **By Domain** | Cases grouped by policy domain (health, environment, immigration, etc.) | [Domain Index](03-permanent-notes/domain-index) |
| **By Outcome** | Cases classified by outcome type (success, partial, failure, design failure) | [Outcome Matrix](03-permanent-notes/outcome-matrix) |
| **By Concept Tested** | Which cases test which ontology concepts | [Concept-Case Matrix](03-permanent-notes/pl-501-cross-case-comparison-matrix) |
| **By Administration** | Cases mapped to presidential administration | [Administration Timeline](03-permanent-notes/administration-timeline) |
| **Chronological** | All cases in temporal order | [Case Timeline](03-permanent-notes/case-timeline) |

---

## Project Status

| Module | Status | Last Updated |
|--------|--------|--------------|
| Core Ontology v1.0 | ✅ Complete | 2026-07-25 |
| Case Library (9 cases) | ✅ Complete | 2026-07-25 |
| EROS Framework v0.1 | 🔄 Draft | 2026-07-25 |
| ICE Abolition Architecture | 🔄 Draft | 2026-07-25 |
| Autopsy of a Vanishing | 📝 Draft | 2026-07-25 |
| Neo4j Knowledge Graph | 📋 Planned | — |
| Public Site (Quartz) | 🔄 Live / Improving | 2026-07-27 |

---

## Quick Actions

- **[Add a new case study](00-documentation/documentation-getting-started#adding-a-case-study)** — Follow the 10-stage protocol
- **[Propose an ontology change](03-permanent-notes/pl-105-ontology-evolution-log)** — Log the proposal with evidence
- **[Review open questions](03-permanent-notes/open-questions)** — Unresolved analytical gaps
- **[View site on GitHub](https://github.com/loom-research-system/loom-research-system)** — Source repository

---

*Last rebuilt: {{ date:YYYY-MM-DD }} • [Report an issue](https://github.com/loom-research-system/loom-research-system/issues)*
