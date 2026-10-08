import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent

def write_file(path, content):
    full_path = BASE_DIR / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {path}")

# --- 1. SCHEMAS (Phase 2 + 3 Patches) ---
write_file("schemas/actor.schema.yaml", '''$schema: "http://json-schema.org/draft-07/schema#"
$id: "loom://schemas/actor.schema.yaml"
title: "Actor"
type: object
required: [id, type, name, created]
properties:
  id: {type: string, pattern: "^ACT-[0-9]{4,}$"}
  type: {type: string, enum: ["human", "system", "agent", "model"]}
  name: {type: string}
  affiliation: {type: string}
  role: {type: string, enum: ["founder", "internal_auditor", "external_auditor", "researcher", "system"]}
  conflict_disclosure: {type: string}
  classification: {type: string, enum: ["internal_auditor", "external_auditor", "researcher", "founder", "system"]}
  auditor_agreement_signed: {type: boolean}
  capacity_limit: {type: integer, minimum: 0}
  current_assignments: {type: integer, minimum: 0}
  independence_distance: {type: string, enum: ["none", "organizational", "financial", "professional", "personal"]}
  can_promote_to_accepted: {type: boolean}
  can_promote_to_canonical: {type: boolean}
  active: {type: boolean}
  created: {type: string, format: date-time}
additionalProperties: false
''')

write_file("schemas/source.schema.yaml", '''$schema: "http://json-schema.org/draft-07/schema#"
$id: "loom://schemas/source.schema.yaml"
title: "Source"
type: object
required: [id, type, title, publisher, date, primary_secondary, independence, retrieved, document_hash, copyright_status, source_assessment]
properties:
  id: {type: string, pattern: "^SRC-[0-9]{4,}$"}
  type: {type: string, const: "source"}
  title: {type: string}
  publisher: {type: string}
  date: {type: string, format: date}
  primary_secondary: {type: string, enum: ["primary", "secondary"]}
  independence: {type: boolean}
  url: {type: string, format: uri}
  retrieved: {type: boolean}
  document_hash: {type: string, pattern: "^sha256:[a-f0-9]{64}$"}
  copyright_status: {type: string, enum: ["public_domain", "creative_commons", "fair_use", "restricted", "unknown"]}
  source_assessment:
    type: object
    required: [quality_rating, factors, rationale]
    properties:
      quality_rating: {type: string, enum: ["high", "moderate", "low", "unknown"]}
      factors: {type: array, items: {type: string}}
      rationale: {type: string}
  retrieval_date: {type: string, format: date-time}
  retrieval_method: {type: string}
additionalProperties: false
''')

write_file("schemas/evidence.schema.yaml", '''$schema: "http://json-schema.org/draft-07/schema#"
$id: "loom://schemas/evidence.schema.yaml"
title: "Evidence"
type: object
required: [id, type, source_id, extracted_content, location, retrieved_at, document_hash, extracted_by]
properties:
  id: {type: string, pattern: "^EVD-[0-9]{4,}$"}
  type: {type: string, const: "evidence"}
  source_id: {type: string, pattern: "^SRC-[0-9]{4,}$"}
  extracted_content: {type: string}
  location: {type: string}
  retrieved_at: {type: string, format: date-time}
  document_hash: {type: string, pattern: "^sha256:[a-f0-9]{64}$"}
  extracted_by: {type: string}
  extraction_method: {type: string}
  content_hash: {type: string, pattern: "^sha256:[a-f0-9]{64}$"}
additionalProperties: false
''')

write_file("schemas/claim.schema.yaml", '''$schema: "http://json-schema.org/draft-07/schema#"
$id: "loom://schemas/claim.schema.yaml"
title: "Claim"
type: object
required: [id, type, claim_type, statement, status, epistemic_status, verification_level, promotion_stage, primary_applicability, current_as_of, related_evidence, contradiction_status, created, updated]
properties:
  id: {type: string, pattern: "^CLM-[0-9]{4,}$"}
  type: {type: string, const: "claim"}
  claim_type: {type: string, enum: ["standard", "dispositive_document"]}
  statement: {type: string}
  dispositive_document_justification: {type: string}
  dispositive_document_scope_check: {type: boolean}
  status: {type: string, enum: ["proposed", "under_review", "system_flagged_for_review", "completed", "rejected", "deprecated"]}
  epistemic_status: {type: string, enum: ["proposed", "unknown", "unresolved", "contested", "supported", "known"]}
  verification_level: {type: string, enum: ["none", "source_backed", "cross_verified", "primary_verified"]}
  promotion_stage: {type: string, enum: ["candidate", "accepted", "canonical"]}
  primary_applicability: {type: string, enum: ["applicable", "not_applicable", "destroyed_or_inaccessible"]}
  current_as_of: {type: string, format: date}
  search_protocol_id: {type: string, pattern: "^PROT-[0-9]{4,}$"}
  related_evidence: {type: array, items: {type: string, pattern: "^EVD-[0-9]{4,}$"}}
  contradictory_evidence: {type: array, items: {type: string, pattern: "^EVD-[0-9]{4,}$"}}
  contradiction_status: {type: string, enum: ["none", "documented", "unresolved", "resolved"]}
  contradiction_note: {type: string}
  contradiction_resolution: {type: string}
  scope:
    type: object
    properties:
      population: {type: string}
      geography: {type: string}
      timeframe: {type: string}
      institution: {type: string}
      event: {type: string}
      exclusions: {type: array, items: {type: string}}
  provenance:
    type: object
    required: [proposed_by, proposed_at]
    properties:
      proposed_by: {type: string}
      proposed_at: {type: string, format: date-time}
  created: {type: string, format: date-time}
  updated: {type: string, format: date-time}
additionalProperties: false
''')

write_file("schemas/observation.schema.yaml", '''$schema: "http://json-schema.org/draft-07/schema#"
$id: "loom://schemas/observation.schema.yaml"
title: "Observation"
type: object
required: [id, type, source_id, evidence_id, interpretation, status, created]
properties:
  id: {type: string, pattern: "^OBS-[0-9]{4,}$"}
  type: {type: string, const: "observation"}
  source_id: {type: string, pattern: "^SRC-[0-9]{4,}$"}
  evidence_id: {type: string, pattern: "^EVD-[0-9]{4,}$"}
  interpretation: {type: string}
  status: {type: string, enum: ["proposed", "under_review", "completed"]}
  related_claims: {type: array, items: {type: string, pattern: "^CLM-[0-9]{4,}$"}}
  created: {type: string, format: date-time}
  updated: {type: string, format: date-time}
additionalProperties: false
''')

write_file("schemas/diagnostic.schema.yaml", '''$schema: "http://json-schema.org/draft-07/schema#"
$id: "loom://schemas/diagnostic.schema.yaml"
title: "Diagnostic"
type: object
required: [id, type, ontology_concept_id, thesis, supporting_claims, epistemic_status, status, created]
properties:
  id: {type: string, pattern: "^DIAG-[0-9]{4,}$"}
  type: {type: string, const: "diagnostic"}
  ontology_concept_id: {type: string, pattern: "^PL-[0-9]{3,}$"}
  thesis: {type: string}
  supporting_claims:
    type: array
    items:
      type: object
      required: [claim_id, materiality]
      properties:
        claim_id: {type: string, pattern: "^CLM-[0-9]{4,}$"}
        materiality: {type: boolean}
  epistemic_status: {type: string, enum: ["proposed", "unknown", "unresolved", "contested", "supported", "known"]}
  status: {type: string, enum: ["proposed", "under_review", "system_flagged_for_review", "completed"]}
  created: {type: string, format: date-time}
  updated: {type: string, format: date-time}
additionalProperties: false
''')

write_file("schemas/provenance-event.schema.yaml", '''$schema: "http://json-schema.org/draft-07/schema#"
$id: "loom://schemas/provenance-event.schema.yaml"
title: "Provenance Event"
type: object
required: [event_id, type, action, actor, timestamp, target_object_id]
properties:
  event_id: {type: string, pattern: "^EVT-[0-9]{4,}$"}
  type: {type: string, enum: ["extraction_event", "verification_event", "assessment_event", "promotion_event", "demotion_event", "contradiction_search_event", "retraction_event", "correction_event", "cascade_trigger_event"]}
  action: {type: string}
  actor: {type: string}
  timestamp: {type: string, format: date-time}
  target_object_id: {type: string}
  target_object_type: {type: string, enum: ["source", "evidence", "claim", "observation", "diagnostic"]}
  inputs: {type: array, items: {type: string}}
  result: {type: string}
  method: {type: string}
  rationale: {type: string}
  disclosure_text: {type: string}
  publication_location: {type: string}
  model_identifier: {type: string}
  cascade_type: {type: string, enum: ["source_invalidation", "staleness_expiration", "material_claim_flagged"]}
  trigger_source_id: {type: string}
  affected_object_ids: {type: array, items: {type: string}}
  cascade_action: {type: string, enum: ["flag_for_review", "recompute_verification_downward", "demote_epistemic_status"]}
additionalProperties: false
''')

write_file("schemas/research-protocol.schema.yaml", '''$schema: "http://json-schema.org/draft-07/schema#"
$id: "loom://schemas/research-protocol.schema.yaml"
title: "Research Protocol"
type: object
required: [id, type, title, scope, databases_searched, query_strings, date_range, inclusion_criteria, exclusion_criteria, created_by, created_at]
properties:
  id: {type: string, pattern: "^PROT-[0-9]{4,}$"}
  type: {type: string, const: "research_protocol"}
  title: {type: string}
  scope: {type: string}
  databases_searched: {type: array, items: {type: string}}
  query_strings: {type: array, items: {type: string}}
  date_range:
    type: object
    required: [start, end]
    properties:
      start: {type: string, format: date}
      end: {type: string, format: date}
  inclusion_criteria: {type: array, items: {type: string}}
  exclusion_criteria: {type: array, items: {type: string}}
  created_by: {type: string}
  created_at: {type: string, format: date-time}
  last_executed: {type: string, format: date-time}
additionalProperties: false
''')

# --- 2. VALIDATOR ENGINE (Phase 3) ---
write_file("loom_validator/validator.py", '''"""
Loom Research System Validator
Enforces PL-307 v1.0 schemas and cross-object validation rules.
"""
import json
import yaml
import sys
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class ValidationError:
    rule_code: str
    severity: str
    object_id: str
    reason: str
    remediation: str
    override_allowed: bool = False

class LoomValidator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.objects: Dict[str, dict] = {}
        self.events: List[dict] = []
        self.errors: List[ValidationError] = []
        
    def load_repository(self):
        for schema_dir in ["artifacts", "tests/fixtures"]:
            path = self.repo_root / schema_dir
            if path.exists():
                for yaml_file in path.rglob("*.yaml"):
                    with open(yaml_file) as f:
                        obj = yaml.safe_load(f)
                        if obj:
                            obj_id = obj.get("id") or obj.get("event_id")
                            if obj_id:
                                self.objects[obj_id] = obj
                                if obj.get("type") == "provenance_event" or "event_id" in obj:
                                    self.events.append(obj)
    
    def validate_all(self) -> List[ValidationError]:
        self.errors = []
        for obj_id, obj in self.objects.items():
            obj_type = obj.get("type")
            if obj_type == "claim": self._validate_claim(obj)
            elif obj_type == "diagnostic": self._validate_diagnostic(obj)
            elif obj_type == "evidence": self._validate_evidence(obj)
            elif obj_type == "source": self._validate_source(obj)
        self._validate_cascade_integrity()
        return self.errors

    def _validate_claim(self, claim: dict):
        claim_id = claim["id"]
        epistemic = claim.get("epistemic_status")
        verification = claim.get("verification_level")
        contradiction = claim.get("contradiction_status")
        promotion = claim.get("promotion_stage")
        claim_type = claim.get("claim_type")
        related_evidence = claim.get("related_evidence", [])
        
        if epistemic == "known" and contradiction == "unresolved":
            self.errors.append(ValidationError("EPISTEMIC-004", "error", claim_id, "Claim declares 'known' while contradictory evidence remains unresolved", "Resolve contradiction or downgrade epistemic_status", False))
        if epistemic == "supported" and contradiction == "unresolved":
            self.errors.append(ValidationError("EPISTEMIC-005", "error", claim_id, "Claim declares 'supported' while contradictory evidence remains unresolved", "Resolve contradiction or downgrade epistemic_status", False))
        if epistemic in ["supported", "known"] and verification in ["none", "source_backed"]:
            self.errors.append(ValidationError("VERIFICATION-001", "error", claim_id, f"epistemic_status '{epistemic}' requires verification_level >= cross_verified", "Upgrade verification_level or downgrade epistemic_status", False))
        if verification == "cross_verified":
            source_ids = set()
            for evd_id in related_evidence:
                evd = self.objects.get(evd_id)
                if evd: source_ids.add(evd.get("source_id"))
            if len(source_ids) < 2:
                self.errors.append(ValidationError("VERIFICATION-002", "error", claim_id, f"cross_verified requires 2+ independent sources, found {len(source_ids)}", "Add evidence from a second independent source", False))
        if promotion == "canonical" and verification in ["none", "source_backed"]:
            self.errors.append(ValidationError("PROMOTION-001", "error", claim_id, "canonical promotion requires verification_level >= cross_verified", "Complete cross-verification before canonical promotion", False))
        if claim_type == "dispositive_document":
            if not claim.get("dispositive_document_justification"):
                self.errors.append(ValidationError("DISPOSITIVE-001", "error", claim_id, "dispositive_document claim missing justification", "Add dispositive_document_justification", False))
            if not claim.get("dispositive_document_scope_check"):
                self.errors.append(ValidationError("DISPOSITIVE-002", "error", claim_id, "dispositive_document claim missing scope check", "Confirm claim is strictly about document content", False))
        if epistemic == "unknown" and not claim.get("search_protocol_id"):
            self.errors.append(ValidationError("UNKNOWN-001", "error", claim_id, "unknown claim missing search_protocol_id", "Reference a formalized research protocol", False))
        if claim.get("status") == "system_flagged_for_review":
            cascade_events = [e for e in self.events if e.get("type") == "cascade_trigger_event" and claim_id in e.get("affected_object_ids", [])]
            if not cascade_events:
                self.errors.append(ValidationError("CASCADE-001", "error", claim_id, "Claim has status 'system_flagged_for_review' but no cascade_trigger_event", "Add cascade_trigger_event or change status", False))

    def _validate_diagnostic(self, diag: dict):
        diag_id = diag["id"]
        diag_epistemic = diag.get("epistemic_status")
        lattice = {"proposed": 0, "unknown": 1, "unresolved": 2, "contested": 3, "supported": 4, "known": 5}
        material_claims = [sc["claim_id"] for sc in diag.get("supporting_claims", []) if sc.get("materiality")]
        if not material_claims:
            self.errors.append(ValidationError("DIAG-001", "error", diag_id, "Diagnostic has no material supporting claims", "Mark at least one supporting claim as material", False))
            return
        min_level = min(lattice.get(self.objects.get(cid, {}).get("epistemic_status"), -1) for cid in material_claims)
        diag_level = lattice.get(diag_epistemic, -1)
        if diag_level > min_level:
            self.errors.append(ValidationError("SCOPE-001", "error", diag_id, f"Diagnostic epistemic_status '{diag_epistemic}' exceeds weakest material claim", f"Downgrade diagnostic", False))

    def _validate_evidence(self, evd: dict):
        evd_id = evd["id"]
        source_id = evd.get("source_id")
        if source_id not in self.objects:
            self.errors.append(ValidationError("PHANTOM-001", "error", evd_id, f"Evidence references non-existent source '{source_id}'", "Create source object or correct source_id reference", False))

    def _validate_source(self, src: dict):
        if src.get("retrieved") and not src.get("document_hash"):
            self.errors.append(ValidationError("SOURCE-001", "error", src["id"], "Retrieved source missing document_hash", "Add sha256 hash of retrieved document", False))

    def _validate_cascade_integrity(self):
        for event in self.events:
            if event.get("type") == "cascade_trigger_event":
                trigger_src = event.get("trigger_source_id")
                if trigger_src and trigger_src not in self.objects:
                    self.errors.append(ValidationError("CASCADE-002", "error", event.get("event_id"), f"Cascade trigger references non-existent object '{trigger_src}'", "Correct trigger_source_id", False))

    def report(self) -> str:
        if not self.errors: return "✓ All validation rules passed"
        lines = [f"✗ {len(self.errors)} validation error(s) found:\\n"]
        for err in self.errors:
            lines.append(f"[{err.rule_code}] {err.object_id}\\n  Reason: {err.reason}\\n  Remediation: {err.remediation}\\n  Override allowed: {err.override_allowed}\\n")
        return "\\n".join(lines)

if __name__ == "__main__":
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    validator = LoomValidator(repo_root)
    validator.load_repository()
    errors = validator.validate_all()
    print(validator.report())
    sys.exit(1 if errors else 0)
''')

# --- 3. ADVERSARIAL FIXTURES (Phase 4) ---
write_file("tests/fixtures/adversarial/CLM-FAKE-001.yaml", '''id: CLM-FAKE-001
type: claim
claim_type: standard
statement: "Test claim with same-source cross-verification"
status: completed
epistemic_status: supported
verification_level: cross_verified
promotion_stage: candidate
primary_applicability: applicable
current_as_of: "2026-09-12"
related_evidence:
  - EVD-FAKE-001
  - EVD-FAKE-002
contradiction_status: none
''')

write_file("tests/fixtures/adversarial/EVD-FAKE-001.yaml", '''id: EVD-FAKE-001
type: evidence
source_id: SRC-FAKE-001
extracted_content: "First excerpt"
location: "page 1"
retrieved_at: "2026-09-12T00:00:00Z"
document_hash: "sha256:aaaa..."
extracted_by: "human:reviewer_A"
''')

write_file("tests/fixtures/adversarial/EVD-FAKE-002.yaml", '''id: EVD-FAKE-002
type: evidence
source_id: SRC-FAKE-001
extracted_content: "Second excerpt"
location: "page 2"
retrieved_at: "2026-09-12T00:00:00Z"
document_hash: "sha256:aaaa..."
extracted_by: "human:reviewer_A"
''')

write_file("tests/fixtures/adversarial/SRC-FAKE-001.yaml", '''id: SRC-FAKE-001
type: source
title: "Single Source Document"
publisher: "Test Publisher"
date: "2026-01-01"
primary_secondary: secondary
independence: true
retrieved: true
document_hash: "sha256:aaaa..."
copyright_status: "public_domain"
source_assessment:
  quality_rating: "high"
  factors: ["directness: high"]
  rationale: "Test source"
''')

write_file("tests/fixtures/adversarial/CLM-FAKE-003.yaml", '''id: CLM-FAKE-003
type: claim
claim_type: standard
statement: "Claim flagged by system without cascade event"
status: system_flagged_for_review
epistemic_status: contested
verification_level: cross_verified
promotion_stage: candidate
primary_applicability: applicable
current_as_of: "2026-09-12"
related_evidence: []
contradiction_status: unresolved
''')

write_file("tests/fixtures/adversarial/CLM-FAKE-004.yaml", '''id: CLM-FAKE-004
type: claim
claim_type: dispositive_document
statement: "The agency memo caused the policy failure"
dispositive_document_justification: "Based on agency memo"
dispositive_document_scope_check: false
status: completed
epistemic_status: supported
verification_level: primary_verified
promotion_stage: candidate
primary_applicability: applicable
current_as_of: "2026-09-12"
related_evidence:
  - EVD-FAKE-003
contradiction_status: none
''')

write_file("tests/fixtures/adversarial/CLM-FAKE-005.yaml", '''id: CLM-FAKE-005
type: claim
claim_type: standard
statement: "Test claim with unconfirmed AI extraction"
status: completed
epistemic_status: supported
verification_level: cross_verified
promotion_stage: candidate
primary_applicability: applicable
current_as_of: "2026-09-12"
related_evidence:
  - EVD-FAKE-004
contradiction_status: none
''')

write_file("tests/fixtures/adversarial/EVD-FAKE-004.yaml", '''id: EVD-FAKE-004
type: evidence
source_id: SRC-FAKE-002
extracted_content: "AI-extracted content"
location: "page 1"
retrieved_at: "2026-09-12T00:00:00Z"
document_hash: "sha256:bbbb..."
extracted_by: "model:llama-3-70b"
''')

write_file("tests/fixtures/adversarial/EVT-FAKE-001.yaml", '''event_id: EVT-FAKE-001
type: promotion_event
action: promote_to_canonical
actor: "human:dr_elena_rostova"
timestamp: "2026-09-12T00:00:00Z"
target_object_id: CLM-FAKE-002
target_object_type: claim
disclosure_text: "Reviewed by independent auditor"
publication_location: "test"
''')

# --- 4. ERRATA & MANIFEST ---
write_file("errata/ERR-001_dispositive_document_edge_cases.md", '''---
id: ERR-001
status: open
severity: moderate
source: "PL-307 v0.5 §30 Open Questions"
imported_date: "2026-09-12"
related_spec: "PL-307 v1.0"
---
## Issue: Dispositive-Document Edge Cases
PL-307 v1.0 allows a single primary source to satisfy `primary_verified` for `dispositive_document` claims.
## Risk
Without strict schema guarding, this carve-out may be abused to bypass the two-independent-source requirement.
## Resolution Path (Phase 2)
The schema must require explicit justification and subject-scope narrowness check.
''')

write_file("errata/ERR-002_source_assessment_calibration.md", '''---
id: ERR-002
status: open
severity: low
source: "PL-307 v0.5 §30 Open Questions"
imported_date: "2026-09-12"
related_spec: "PL-307 v1.0"
---
## Issue: Source-Assessment Calibration
PL-307 v1.0 requires a `source_assessment` block. Without a formalized rubric, ratings may be applied inconsistently.
## Resolution Path (Phase 2 / Phase 5)
Develop a lightweight, standardized rubric for source assessment.
''')

write_file("errata/ERR-003_semantic_similarity_tuning.md", '''---
id: ERR-003
status: open
severity: moderate
source: "PL-307 v0.5 §30 Open Questions"
imported_date: "2026-09-12"
related_spec: "PL-307 v1.0"
---
## Issue: Semantic-Similarity Tuning
PL-307 v1.0 §8 mandates an initial near-duplicate flag of ≥0.90 similarity.
## Risk
The exact NLP models and thresholds require empirical tuning.
## Resolution Path (Phase 4 / Phase 12)
Test the 0.90 threshold against the adversarial fixture suite.
''')

write_file("errata/ERR-004_search_protocol_formalization.md", '''---
id: ERR-004
status: open
severity: high
source: "PL-307 v0.5 §30 Open Questions"
imported_date: "2026-09-12"
related_spec: "PL-307 v1.0"
---
## Issue: Search-Protocol Formalization
PL-307 v1.0 requires `unknown` claims to reference a `search_protocol_id`, but the structure is not formally defined.
## Resolution Path (Phase 2)
Define a mandatory `Research Protocol` schema.
''')

write_file("specifications/MANIFEST.yaml", '''# Loom Research System Specification Manifest
version: "1.0"
updated: "2026-09-12"
specifications:
  - id: "PL-307"
    title: "Claims, Epistemic Status, Verification & Promotion Specification"
    version: "1.0"
    status: "LOCKED"
    effective_date: "2026-09-10"
    file_path: "specifications/PL-307_v1.0_Claims_Epistemic_Status_Verification_Promotion.md"
    content_hash: "[PENDING_GIT_COMMIT_HASH]"
  - id: "PL-001"
    title: "Project Loom Implementation Roadmap & Governance Control Document"
    version: "1.1"
    status: "LOCKED"
    effective_date: "2026-09-12"
    file_path: "specifications/PL-001_v1.1_Implementation_Roadmap_Governance_Control.md"
    content_hash: "[PENDING_GIT_COMMIT_HASH]"
governance_state:
  current_phase: "Phase 3: Validator & Fixtures"
  interim_rule_active: true
''')

write_file("diary/milestones/2026-09-12_phase_1_initialization.md", '''---
id: DIA-2026-001
category: milestone
title: "Phase 1 Initialization: Repository Structure and Governance Baseline"
date: "2026-09-12"
author: "Loom Founder"
related_specs: ["PL-307 v1.0", "PL-001 v1.1"]
tags: ["governance", "initialization", "phase-1"]
---
## Context
Following the adversarial review of REQ-006 v2.0, PL-001 v1.1 was drafted and locked to freeze the conceptual baseline.
## Action
Phase 1 executed. Canonical directory structure established. MANIFEST.yaml registered. Errata imported.
## Impact
1. Retirement of Solo-Founder Exception.
2. Bootstrap Governance Rule Enacted.
3. Absolute Prohibition on fabricated identities enforced.
''')

# --- 5. GIT OPERATIONS ---
print("\n Running Git Operations...")
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "feat: Memorialize Phases 1-3 (Schemas, Validator, Fixtures, Errata, Manifest)"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("\n SUCCESS! All files have been memorialized and pushed to GitHub.")
except subprocess.CalledProcessError as e:
    print(f"\n️ Git operation failed: {e}")
    print("Please ensure you are in the correct directory and authenticated with GitHub CLI.")