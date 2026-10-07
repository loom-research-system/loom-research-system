"""
Loom Research System Validator
Enforces PL-307 v1.0 schemas and cross-object validation rules.
<<<<<<< HEAD
Exit code 0 = valid, non-zero = invalid.
"""

import json
import yaml
import sys
from pathlib import Path
from typing import List, Dict, Tuple
=======
"""
import json, yaml, sys
from pathlib import Path
from typing import List, Dict
>>>>>>> 6a46dac2acf4074d0aa8255b8b5e64a161617fc6
from dataclasses import dataclass

@dataclass
class ValidationError:
    rule_code: str
<<<<<<< HEAD
    severity: str  # "error" or "warning"
=======
    severity: str
>>>>>>> 6a46dac2acf4074d0aa8255b8b5e64a161617fc6
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
<<<<<<< HEAD
        """Load all YAML objects from the repository."""
=======
>>>>>>> 6a46dac2acf4074d0aa8255b8b5e64a161617fc6
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
<<<<<<< HEAD
        """Run all validation rules."""
        self.errors = []
        
        # Schema-level validation (JSON Schema)
        for obj_id, obj in self.objects.items():
            self._validate_schema(obj)
        
        # Cross-object validation rules
        for obj_id, obj in self.objects.items():
            obj_type = obj.get("type")
            
            if obj_type == "claim":
                self._validate_claim(obj)
            elif obj_type == "diagnostic":
                self._validate_diagnostic(obj)
            elif obj_type == "evidence":
                self._validate_evidence(obj)
            elif obj_type == "source":
                self._validate_source(obj)
        
        # Cascade integrity check
        self._validate_cascade_integrity()
        
        return self.errors
    
    def _validate_schema(self, obj: dict):
        """JSON Schema validation (delegated to jsonschema library in production)."""
        # Placeholder: in production, use jsonschema.validate()
        pass
    
=======
        self.errors = []
        for obj_id, obj in self.objects.items():
            self._validate_schema(obj)
            obj_type = obj.get("type")
            if obj_type == "claim": self._validate_claim(obj)
            elif obj_type == "diagnostic": self._validate_diagnostic(obj)
            elif obj_type == "evidence": self._validate_evidence(obj)
            elif obj_type == "source": self._validate_source(obj)
        self._validate_cascade_integrity()
        return self.errors

    def _validate_schema(self, obj: dict): pass

>>>>>>> 6a46dac2acf4074d0aa8255b8b5e64a161617fc6
    def _validate_claim(self, claim: dict):
        claim_id = claim["id"]
        epistemic = claim.get("epistemic_status")
        verification = claim.get("verification_level")
        contradiction = claim.get("contradiction_status")
        promotion = claim.get("promotion_stage")
        claim_type = claim.get("claim_type")
        related_evidence = claim.get("related_evidence", [])
        
<<<<<<< HEAD
        # EPISTEMIC-004: known + unresolved contradiction
        if epistemic == "known" and contradiction == "unresolved":
            self.errors.append(ValidationError(
                rule_code="EPISTEMIC-004",
                severity="error",
                object_id=claim_id,
                reason="Claim declares 'known' while contradictory evidence remains unresolved",
                remediation="Resolve contradiction or downgrade epistemic_status to 'contested'",
                override_allowed=False
            ))
        
        # EPISTEMIC-005: supported + unresolved contradiction
        if epistemic == "supported" and contradiction == "unresolved":
            self.errors.append(ValidationError(
                rule_code="EPISTEMIC-005",
                severity="error",
                object_id=claim_id,
                reason="Claim declares 'supported' while contradictory evidence remains unresolved",
                remediation="Resolve contradiction or downgrade epistemic_status",
                override_allowed=False
            ))
        
        # VERIFICATION-001: supported requires cross_verified or stronger
        if epistemic in ["supported", "known"] and verification in ["none", "source_backed"]:
            self.errors.append(ValidationError(
                rule_code="VERIFICATION-001",
                severity="error",
                object_id=claim_id,
                reason=f"epistemic_status '{epistemic}' requires verification_level >= cross_verified",
                remediation=f"Upgrade verification_level or downgrade epistemic_status",
                override_allowed=False
            ))
        
        # VERIFICATION-002: cross_verified requires 2+ independent sources
=======
        if epistemic == "known" and contradiction == "unresolved":
            self.errors.append(ValidationError("EPISTEMIC-004", "error", claim_id, "Claim declares 'known' while contradictory evidence remains unresolved", "Resolve contradiction or downgrade epistemic_status to 'contested'", False))
        if epistemic == "supported" and contradiction == "unresolved":
            self.errors.append(ValidationError("EPISTEMIC-005", "error", claim_id, "Claim declares 'supported' while contradictory evidence remains unresolved", "Resolve contradiction or downgrade epistemic_status", False))
        if epistemic in ["supported", "known"] and verification in ["none", "source_backed"]:
            self.errors.append(ValidationError("VERIFICATION-001", "error", claim_id, f"epistemic_status '{epistemic}' requires verification_level >= cross_verified", "Upgrade verification_level or downgrade epistemic_status", False))
>>>>>>> 6a46dac2acf4074d0aa8255b8b5e64a161617fc6
        if verification == "cross_verified":
            source_ids = set()
            for evd_id in related_evidence:
                evd = self.objects.get(evd_id)
<<<<<<< HEAD
                if evd:
                    source_ids.add(evd.get("source_id"))
            if len(source_ids) < 2:
                self.errors.append(ValidationError(
                    rule_code="VERIFICATION-002",
                    severity="error",
                    object_id=claim_id,
                    reason=f"cross_verified requires 2+ independent sources, found {len(source_ids)}",
                    remediation="Add evidence from a second independent source",
                    override_allowed=False
                ))
        
        # VERIFICATION-003: AI extraction cap
        ai_extracted_material = False
        for evd_id in related_evidence:
            evd = self.objects.get(evd_id)
            if evd and evd.get("extracted_by", "").startswith("model:"):
                # Check for human confirmation event
                confirmed = any(
                    e.get("type") == "verification_event" and
                    e.get("action") == "human_source_confirmation" and
                    e.get("evidence_id") == evd_id and
                    e.get("actor", "").startswith("human:")
                    for e in self.events
                )
                if not confirmed:
                    ai_extracted_material = True
                    break
        
        if ai_extracted_material and verification in ["cross_verified", "primary_verified"]:
            self.errors.append(ValidationError(
                rule_code="VERIFICATION-003",
                severity="error",
                object_id=claim_id,
                reason="Material evidence was AI-extracted without human confirmation event",
                remediation="Add human_source_confirmation event or downgrade verification_level to source_backed",
                override_allowed=False
            ))
        
        # PROMOTION-001: canonical requires cross_verified minimum
        if promotion == "canonical" and verification in ["none", "source_backed"]:
            self.errors.append(ValidationError(
                rule_code="PROMOTION-001",
                severity="error",
                object_id=claim_id,
                reason="canonical promotion requires verification_level >= cross_verified",
                remediation="Complete cross-verification before canonical promotion",
                override_allowed=False
            ))
        
        # PROMOTION-002: canonical requires promotion_event with disclosure
        if promotion == "canonical":
            promotion_events = [
                e for e in self.events
                if e.get("type") == "promotion_event" and
                   e.get("target_object_id") == claim_id and
                   e.get("action") == "promote_to_canonical"
            ]
            if not promotion_events:
                self.errors.append(ValidationError(
                    rule_code="PROMOTION-002",
                    severity="error",
                    object_id=claim_id,
                    reason="canonical claim has no promotion_event in provenance log",
                    remediation="Add promotion_event with disclosure_text and publication_location",
                    override_allowed=False
                ))
        
        # DISPOSITIVE-001: dispositive_document requires justification and scope check
        if claim_type == "dispositive_document":
            if not claim.get("dispositive_document_justification"):
                self.errors.append(ValidationError(
                    rule_code="DISPOSITIVE-001",
                    severity="error",
                    object_id=claim_id,
                    reason="dispositive_document claim missing justification",
                    remediation="Add dispositive_document_justification explaining why claim is purely about document content",
                    override_allowed=False
                ))
            if not claim.get("dispositive_document_scope_check"):
                self.errors.append(ValidationError(
                    rule_code="DISPOSITIVE-002",
                    severity="error",
                    object_id=claim_id,
                    reason="dispositive_document claim missing scope check",
                    remediation="Confirm claim is strictly about document content, not causal/evaluative",
                    override_allowed=False
                ))
        
        # UNKNOWN-001: unknown requires search_protocol_id
        if epistemic == "unknown" and not claim.get("search_protocol_id"):
            self.errors.append(ValidationError(
                rule_code="UNKNOWN-001",
                severity="error",
                object_id=claim_id,
                reason="unknown claim missing search_protocol_id",
                remediation="Reference a formalized research protocol",
                override_allowed=False
            ))
        
        # CASCADE-001: system_flagged_for_review requires cascade_trigger_event
        if claim.get("status") == "system_flagged_for_review":
            cascade_events = [
                e for e in self.events
                if e.get("type") == "cascade_trigger_event" and
                   claim_id in e.get("affected_object_ids", [])
            ]
            if not cascade_events:
                self.errors.append(ValidationError(
                    rule_code="CASCADE-001",
                    severity="error",
                    object_id=claim_id,
                    reason="Claim has status 'system_flagged_for_review' but no cascade_trigger_event",
                    remediation="Add cascade_trigger_event or change status to 'under_review' (human-initiated)",
                    override_allowed=False
                ))
    
    def _validate_diagnostic(self, diag: dict):
        diag_id = diag["id"]
        diag_epistemic = diag.get("epistemic_status")
        
        # Lattice ordering
        lattice = {
            "proposed": 0, "unknown": 1, "unresolved": 2,
            "contested": 3, "supported": 4, "known": 5
        }
        
        material_claims = [
            sc["claim_id"] for sc in diag.get("supporting_claims", [])
            if sc.get("materiality")
        ]
        
        if not material_claims:
            self.errors.append(ValidationError(
                rule_code="DIAG-001",
                severity="error",
                object_id=diag_id,
                reason="Diagnostic has no material supporting claims",
                remediation="Mark at least one supporting claim as material",
                override_allowed=False
            ))
            return
        
        # SCOPE-001: diagnostic epistemic ceiling
        min_level = min(
            lattice.get(self.objects.get(cid, {}).get("epistemic_status"), -1)
            for cid in material_claims
        )
        diag_level = lattice.get(diag_epistemic, -1)
        
        if diag_level > min_level:
            self.errors.append(ValidationError(
                rule_code="SCOPE-001",
                severity="error",
                object_id=diag_id,
                reason=f"Diagnostic epistemic_status '{diag_epistemic}' exceeds weakest material claim",
                remediation=f"Downgrade diagnostic to at most '{list(lattice.keys())[min_level]}'",
                override_allowed=False
            ))
    
    def _validate_evidence(self, evd: dict):
        evd_id = evd["id"]
        source_id = evd.get("source_id")
        
        # PHANTOM-001: evidence must reference existing source
        if source_id not in self.objects:
            self.errors.append(ValidationError(
                rule_code="PHANTOM-001",
                severity="error",
                object_id=evd_id,
                reason=f"Evidence references non-existent source '{source_id}'",
                remediation="Create source object or correct source_id reference",
                override_allowed=False
            ))
    
    def _validate_source(self, src: dict):
        # SOURCE-001: retrieved source must have document_hash
        if src.get("retrieved") and not src.get("document_hash"):
            self.errors.append(ValidationError(
                rule_code="SOURCE-001",
                severity="error",
                object_id=src["id"],
                reason="Retrieved source missing document_hash",
                remediation="Add sha256 hash of retrieved document",
                override_allowed=False
            ))
    
    def _validate_cascade_integrity(self):
        """Ensure all cascade_trigger_events reference valid objects."""
=======
                if evd: source_ids.add(evd.get("source_id"))
            if len(source_ids) < 2:
                self.errors.append(ValidationError("VERIFICATION-002", "error", claim_id, f"cross_verified requires 2+ independent sources, found {len(source_ids)}", "Add evidence from a second independent source", False))
        if promotion == "canonical" and verification in ["none", "source_backed"]:
            self.errors.append(ValidationError("PROMOTION-001", "error", claim_id, "canonical promotion requires verification_level >= cross_verified", "Complete cross-verification before canonical promotion", False))
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
            self.errors.append(ValidationError("SCOPE-001", "error", diag_id, f"Diagnostic epistemic_status '{diag_epistemic}' exceeds weakest material claim", f"Downgrade diagnostic to at most '{list(lattice.keys())[min_level]}'", False))

    def _validate_evidence(self, evd: dict):
        evd_id = evd["id"]
        source_id = evd.get("source_id")
        if source_id not in self.objects:
            self.errors.append(ValidationError("PHANTOM-001", "error", evd_id, f"Evidence references non-existent source '{source_id}'", "Create source object or correct source_id reference", False))

    def _validate_source(self, src: dict):
        if src.get("retrieved") and not src.get("document_hash"):
            self.errors.append(ValidationError("SOURCE-001", "error", src["id"], "Retrieved source missing document_hash", "Add sha256 hash of retrieved document", False))

    def _validate_cascade_integrity(self):
>>>>>>> 6a46dac2acf4074d0aa8255b8b5e64a161617fc6
        for event in self.events:
            if event.get("type") == "cascade_trigger_event":
                trigger_src = event.get("trigger_source_id")
                if trigger_src and trigger_src not in self.objects:
<<<<<<< HEAD
                    self.errors.append(ValidationError(
                        rule_code="CASCADE-002",
                        severity="error",
                        object_id=event.get("event_id"),
                        reason=f"Cascade trigger references non-existent object '{trigger_src}'",
                        remediation="Correct trigger_source_id or create the referenced object",
                        override_allowed=False
                    ))
    
    def report(self) -> str:
        """Generate human-readable validation report."""
        if not self.errors:
            return "✓ All validation rules passed"
        
        lines = [f"✗ {len(self.errors)} validation error(s) found:\n"]
        for err in self.errors:
            lines.append(f"[{err.rule_code}] {err.object_id}")
            lines.append(f"  Reason: {err.reason}")
            lines.append(f"  Remediation: {err.remediation}")
            lines.append(f"  Override allowed: {err.override_allowed}")
            lines.append("")
        
        return "\n".join(lines)


=======
                    self.errors.append(ValidationError("CASCADE-002", "error", event.get("event_id"), f"Cascade trigger references non-existent object '{trigger_src}'", "Correct trigger_source_id", False))

    def report(self) -> str:
        if not self.errors: return "✓ All validation rules passed"
        lines = [f"✗ {len(self.errors)} validation error(s) found:\n"]
        for err in self.errors:
            lines.append(f"[{err.rule_code}] {err.object_id}\n  Reason: {err.reason}\n  Remediation: {err.remediation}\n  Override allowed: {err.override_allowed}\n")
        return "\n".join(lines)

>>>>>>> 6a46dac2acf4074d0aa8255b8b5e64a161617fc6
if __name__ == "__main__":
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    validator = LoomValidator(repo_root)
    validator.load_repository()
    errors = validator.validate_all()
    print(validator.report())
    sys.exit(1 if errors else 0)
