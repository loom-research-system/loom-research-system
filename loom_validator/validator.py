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
import re

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
                    with open(yaml_file, encoding='utf-8-sig') as f:
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
            elif obj_type == "evidence_gap": self._validate_evidence_gap(obj)
            elif obj_type == "mechanism": self._validate_mechanism(obj)
            elif obj_type == "dependency": self._validate_dependency(obj)
            elif obj_type == "transition": self._validate_transition(obj)
        self._validate_cascade_integrity()
        return self.errors

    def _validate_claim(self, claim: dict):
        claim_id = claim["id"]
        epistemic = claim.get("epistemic_status")
        verification = claim.get("verification_level")
        contradiction = claim.get("contradiction_status")
        promotion = claim.get("promotion_stage")
        claim_type = claim.get("claim_type")
        claim_category = claim.get("claim_category")
        related_evidence = claim.get("related_evidence", [])

        if epistemic == "known" and contradiction == "unresolved":
            self.errors.append(ValidationError("EPISTEMIC-004", "error", claim_id, "Claim declares 'known' while contradictory evidence remains unresolved", "Resolve contradiction or downgrade epistemic_status", False))
        if epistemic == "supported" and contradiction == "unresolved":
            self.errors.append(ValidationError("EPISTEMIC-005", "error", claim_id, "Claim declares 'supported' while contradictory evidence remains unresolved", "Resolve contradiction or downgrade epistemic_status", False))
        if epistemic == "contested" and contradiction == "resolved":
            self.errors.append(ValidationError("EPISTEMIC-003", "error", claim_id, "Claim is 'contested' but contradiction is marked 'resolved' (stale state)", "Reassess contradiction_status or update epistemic_status", False))
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
        if promotion == "canonical" and epistemic in ["proposed", "unknown", "unresolved", "contested", "contradicted"]:
            self.errors.append(ValidationError("PROMOTION-003", "error", claim_id, f"canonical promotion requires epistemic_status 'supported' or 'known', found '{epistemic}'", "Resolve epistemic barriers before canonical promotion", False))
        if promotion == "accepted" and epistemic in ["proposed", "unknown", "unresolved", "contested"]:
            self.errors.append(ValidationError("PROMOTION-004", "error", claim_id, f"accepted promotion requires epistemic_status 'supported' or 'known', found '{epistemic}'", "Resolve epistemic barriers before accepted promotion", False))

        if verification == "primary_verified" and claim_type == "standard":
            source_ids = set(evd.get("source_id") for evd_id in related_evidence if (evd := self.objects.get(evd_id)))
            if len(source_ids) < 2:
                self.errors.append(ValidationError("VERIFICATION-004", "error", claim_id, "primary_verified on a 'standard' claim requires cross_verified basis (2+ sources)", "Add second independent source or change claim_type to 'dispositive_document'", False))
        if verification == "primary_verified" and claim.get("primary_applicability") in ["not_applicable", "destroyed_or_inaccessible"]:
            self.errors.append(ValidationError("VERIFICATION-005", "error", claim_id, "primary_verified requires primary_applicability to be 'applicable'", "Correct primary_applicability or downgrade verification_level", False))

        if claim.get("status") == "completed" and epistemic == "proposed":
            self.errors.append(ValidationError("WORKFLOW-001", "error", claim_id, "Claim status is 'completed' but epistemic_status is still 'proposed'", "Complete epistemic assessment or revert status to 'under_review'", False))
        if claim.get("status") == "completed" and verification == "none" and epistemic != "unknown":
            self.errors.append(ValidationError("WORKFLOW-002", "error", claim_id, "Completed claim must have at least source_backed verification", "Map evidence or downgrade status", False))
        if promotion == "canonical" and claim.get("status") == "deprecated":
            self.errors.append(ValidationError("WORKFLOW-003", "error", claim_id, "Claim is 'deprecated' but remains in 'canonical' promotion stage", "Demote promotion_stage to 'candidate' or remove deprecated status", False))

        if claim_type == "dispositive_document":
            if not claim.get("dispositive_document_justification"):
                self.errors.append(ValidationError("DISPOSITIVE-001", "error", claim_id, "dispositive_document claim missing justification", "Add dispositive_document_justification", False))
            if not claim.get("dispositive_document_scope_check"):
                self.errors.append(ValidationError("DISPOSITIVE-002", "error", claim_id, "dispositive_document claim missing scope check", "Confirm claim is strictly about document content", False))

        if epistemic == "unknown" and not claim.get("search_protocol_id"):
            self.errors.append(ValidationError("UNKNOWN-001", "error", claim_id, "unknown claim missing search_protocol_id", "Reference a formalized research protocol", False))

        if contradiction == "resolved":
            if not claim.get("contradiction_resolution"):
                self.errors.append(ValidationError("CONTRADICTION-001", "error", claim_id, "Resolved contradiction missing contradiction_resolution", "Explain how the evidence supports the resolution", False))
            resolution_evidence = claim.get("contradiction_resolution_evidence", [])
            if not resolution_evidence:
                self.errors.append(ValidationError("CONTRADICTION-002", "error", claim_id, "Resolved contradiction missing contradiction_resolution_evidence", "Reference evidence supporting the resolution", False))
            for evd_id in resolution_evidence:
                if evd_id not in self.objects or self.objects[evd_id].get("type") != "evidence":
                    self.errors.append(ValidationError("PHANTOM-003", "error", claim_id, f"Contradiction resolution references non-existent evidence '{evd_id}'", "Create evidence object or correct the reference", False))

        if claim.get("status") == "system_flagged_for_review":
            cascade_events = [e for e in self.events if e.get("type") == "cascade_trigger_event" and claim_id in e.get("affected_object_ids", [])]
            if not cascade_events:
                self.errors.append(ValidationError("CASCADE-001", "error", claim_id, "Claim has status 'system_flagged_for_review' but no cascade_trigger_event", "Add cascade_trigger_event or change status to 'under_review'", False))

        atomicity_events = [e for e in self.events if e.get("type") == "assessment_event" and e.get("action") == "atomicity_verification" and e.get("target_object_id") == claim_id]
        if not atomicity_events:
            self.errors.append(ValidationError("ATOMICITY-001", "error", claim_id, "Claim lacks a human atomicity_verification event", "Add assessment_event confirming the claim contains only one discrete assertion", False))

        if claim_category == "meta_state":
            if epistemic == "unknown" or promotion in ["accepted", "canonical"]:
                self.errors.append(ValidationError("METACLAIM-001", "error", claim_id, "Meta-claims about establishability cannot be 'unknown' or promoted", "Rewrite as a world-state claim or downgrade to observation", False))

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
        source = self.objects.get(evd.get("source_id"))
        if not source or source.get("type") != "source":
            self.errors.append(ValidationError("PHANTOM-001", "error", evd["id"], f"Evidence references non-existent source '{evd.get('source_id')}'", "Create source object or correct source_id reference", False))
            return
        source_hash = source.get("document_hash")
        evidence_hash = evd.get("document_hash")
        if source_hash and evidence_hash != source_hash:
            self.errors.append(ValidationError("PROVENANCE-001", "error", evd["id"], "Evidence document_hash does not match its source document_hash", "Use the hash of the exact source version from which the evidence was extracted", False))
        if not source_hash and evidence_hash:
            self.errors.append(ValidationError("PROVENANCE-002", "error", evd["id"], "Evidence has a document_hash while its source has no document_hash", "Hash and record the source artifact, or set evidence document_hash to null", False))

    def _validate_source(self, src: dict):
        if src.get("retrieved") and not src.get("retrieval_method"):
            self.errors.append(ValidationError("SOURCE-002", "error", src["id"], "Retrieved source missing retrieval_method", "Record how the source was obtained", False))
        if src.get("retrieved") and src.get("source_format") == "pdf" and src.get("primary_secondary") == "primary" and not src.get("document_hash"):
            self.errors.append(ValidationError("SOURCE-003", "error", src["id"], "Retrieved primary PDF missing document_hash", "Hash the exact retrieved PDF bytes", False))
        if src.get("document_hash") is not None and not re.fullmatch(r"sha256:[a-f0-9]{64}", str(src.get("document_hash"))):
            self.errors.append(ValidationError("SOURCE-004", "error", src["id"], "document_hash is not a valid SHA-256 value", "Use sha256: followed by 64 lowercase hexadecimal characters", False))

    def _validate_evidence_gap(self, gap: dict):
        gap_id = gap["id"]
        claim_id = gap.get("related_claim_id")
        protocol_id = gap.get("search_protocol_id")
        if claim_id and (claim_id not in self.objects or self.objects[claim_id].get("type") != "claim"):
            self.errors.append(ValidationError("GAP-001", "error", gap_id, f"Evidence gap references non-existent claim '{claim_id}'", "Create claim object or correct related_claim_id", False))
        if protocol_id and protocol_id not in self.objects:
            self.errors.append(ValidationError("GAP-002", "error", gap_id, f"Evidence gap references non-existent search protocol '{protocol_id}'", "Create protocol object or correct search_protocol_id", False))
        if gap.get("search_result") in ["exhausted", "confirmed_absent"] and not gap.get("search_performed"):
            self.errors.append(ValidationError("GAP-003", "error", gap_id, "Search result indicates a completed search but search_performed is false", "Record the search as performed or use pending", False))
        if gap.get("search_result") == "confirmed_absent" and not gap.get("absence_basis"):
            self.errors.append(ValidationError("GAP-004", "error", gap_id, "confirmed_absent requires an absence_basis", "Cite the evidence establishing that the material is absent", False))

    def _validate_mechanism(self, mech: dict):
        mech_id = mech["id"]
        if mech.get("effective_from") and mech.get("effective_to"):
            if mech["effective_from"] > mech["effective_to"]:
                self.errors.append(ValidationError("MECH-001", "error", mech_id, "effective_from is after effective_to", "Correct the dates", False))

    def _validate_dependency(self, dep: dict):
        dep_id = dep["id"]
        if dep.get("source_node_id") and dep["source_node_id"] not in self.objects:
            self.errors.append(ValidationError("DEP-001", "error", dep_id, f"Dependency references non-existent source node '{dep.get('source_node_id')}'", "Create source node or correct ID", False))
        if dep.get("target_node_id") and dep["target_node_id"] not in self.objects:
            self.errors.append(ValidationError("DEP-002", "error", dep_id, f"Dependency references non-existent target node '{dep.get('target_node_id')}'", "Create target node or correct ID", False))

    def _validate_transition(self, trans: dict):
        trans_id = trans["id"]
        if trans.get("target_node_id") and trans["target_node_id"] not in self.objects:
            self.errors.append(ValidationError("TRANS-001", "error", trans_id, f"Transition references non-existent target node '{trans.get('target_node_id')}'", "Create target node or correct ID", False))
        if trans.get("sequence_order") is not None and trans["sequence_order"] < 1:
            self.errors.append(ValidationError("TRANS-002", "error", trans_id, "sequence_order must be >= 1", "Update sequence order", False))

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
