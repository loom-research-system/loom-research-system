"""
Loom Research System Validator
Enforces PL-307 v1.0 schemas and cross-object validation rules.
Exit code 0 = valid, non-zero = invalid.
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
                    with open(yaml_file, encoding='utf-8') as f:
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
                self.errors.append(ValidationError("CASCADE-001", "error", claim_id, "Claim has status 'system_flagged_for_review' but no cascade_trigger_event", "Add cascade_trigger_event or change status to 'under_review'", False))

    def _validate_diagnostic(self, diag: dict):
        diag_id = diag["id"]
        diag_epistemic = diag.get("epistemic_status")
        lattice = {"proposed": 0, "unknown": 1, "unresolved": 2, "contested": 3, "supported": 4, "known": 5}
        material_claims = [sc["claim_id"] for sc in diag.get("supporting_claims", []) if sc.get("materiality")]
        if not material_claims:
            self.errors.append(ValidationError("DIAG-001", "error", diag_id, "Diagnostic has no material supporting claims", "Mark at least one supporting claim as material", False))
            return
        min_level = min(lattice.get(self.objects.get(cid, {}).get("epistemic_status"), -1) for cid in material_claims)
        if lattice.get(diag_epistemic, -1) > min_level:
            self.errors.append(ValidationError("SCOPE-001", "error", diag_id, f"Diagnostic epistemic_status '{diag_epistemic}' exceeds weakest material claim", f"Downgrade diagnostic to at most '{list(lattice.keys())[min_level]}'", False))

    def _validate_evidence(self, evd: dict):
        if evd.get("source_id") not in self.objects:
            self.errors.append(ValidationError("PHANTOM-001", "error", evd["id"], f"Evidence references non-existent source '{evd.get('source_id')}'", "Create source object or correct source_id reference", False))

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
        lines = [f"✗ {len(self.errors)} validation error(s) found:\n"]
        for err in self.errors:
            lines.extend([f"[{err.rule_code}] {err.object_id}", f"  Reason: {err.reason}", f"  Remediation: {err.remediation}", f"  Override allowed: {err.override_allowed}", ""])
        return "\n".join(lines)

if __name__ == "__main__":
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    validator = LoomValidator(repo_root)
    validator.load_repository()
    errors = validator.validate_all()
    print(validator.report())
    sys.exit(1 if errors else 0)
