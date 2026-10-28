"""Repeatable adversarial tests for Loom's cross-object validator.

These tests exercise validator rules directly with isolated in-memory objects.
They do not assert that a structurally valid claim is factually true.
Run: python -m unittest discover -s tests -p 'test_*.py' -v
"""
import unittest
from pathlib import Path

from loom_validator.validator import LoomValidator


HASH_A = "sha256:" + "a" * 64
HASH_B = "sha256:" + "b" * 64


def validator_with(*objects):
    validator = LoomValidator(Path("."))
    validator.objects = {obj["id"]: obj for obj in objects}
    # Prevent unrelated atomicity/cascade checks from being triggered unless
    # a test explicitly supplies the relevant event.
    validator.events = []
    return validator


def source(source_id="SRC-TEST-001", *, independence=True, source_format="pdf",
           primary_secondary="primary", document_hash=HASH_A, retrieved=True,
           retrieval_method="direct_download"):
    return {
        "id": source_id, "type": "source", "title": "Test source",
        "publisher": "Test agency", "date": "2023-01-01",
        "primary_secondary": primary_secondary, "independence": independence,
        "retrieved": retrieved, "retrieval_method": retrieval_method,
        "source_format": source_format, "document_hash": document_hash,
    }


def evidence(evidence_id="EVD-TEST-001", source_id="SRC-TEST-001",
             document_hash=HASH_A):
    return {
        "id": evidence_id, "type": "evidence", "source_id": source_id,
        "extracted_content": "Test excerpt", "location": "Page 1",
        "retrieved_at": "2023-10-01T10:00:00Z",
        "document_hash": document_hash, "extracted_by": "human:test",
        "extraction_method": "manual_copy",
    }


def claim(**overrides):
    obj = {
        "id": "CLM-TEST-001", "type": "claim", "claim_type": "standard",
        "statement": "A test proposition.", "status": "under_review",
        "epistemic_status": "proposed", "verification_level": "source_backed",
        "promotion_stage": "candidate", "primary_applicability": "applicable",
        "related_evidence": [], "contradictory_evidence": [],
        "contradiction_status": "none",
        "created": "2023-10-01T11:00:00Z",
        "updated": "2023-10-01T11:00:00Z",
    }
    obj.update(overrides)
    return obj


def gap(**overrides):
    obj = {
        "id": "GAP-TEST-001", "type": "evidence_gap",
        "missing_information": "A missing record",
        "search_performed": True, "search_result": "not_found",
        "search_scope": ["Test archive"], "search_methods": ["keyword_search"],
        "search_performed_at": "2023-10-01T12:00:00Z",
        "created": "2023-10-01T12:00:00Z",
        "updated": "2023-10-01T12:00:00Z",
    }
    obj.update(overrides)
    return obj


def rule_codes(validator):
    return {err.rule_code for err in validator.errors}


class SourceValidationTests(unittest.TestCase):
    def test_hashed_retrieved_primary_pdf_passes(self):
        v = validator_with(source())
        v._validate_source(v.objects["SRC-TEST-001"])
        self.assertEqual(rule_codes(v), set())

    def test_unhashed_secondary_web_page_is_allowed(self):
        obj = source(source_format="html", primary_secondary="secondary",
                     document_hash=None, retrieval_method="web_page")
        v = validator_with(obj)
        v._validate_source(obj)
        self.assertEqual(rule_codes(v), set())

    def test_retrieved_primary_pdf_without_hash_fails(self):
        obj = source(document_hash=None)
        v = validator_with(obj)
        v._validate_source(obj)
        self.assertIn("SOURCE-003", rule_codes(v))

    def test_malformed_hash_fails(self):
        obj = source(document_hash="sha256:abc")
        v = validator_with(obj)
        v._validate_source(obj)
        self.assertIn("SOURCE-004", rule_codes(v))

    def test_retrieved_source_without_retrieval_method_fails(self):
        obj = source(retrieval_method=None)
        v = validator_with(obj)
        v._validate_source(obj)
        self.assertIn("SOURCE-002", rule_codes(v))


class EvidenceProvenanceTests(unittest.TestCase):
    def test_matching_source_and_evidence_hash_passes(self):
        src, evd = source(), evidence()
        v = validator_with(src, evd)
        v._validate_evidence(evd)
        self.assertEqual(rule_codes(v), set())

    def test_mismatched_evidence_hash_fails(self):
        src, evd = source(), evidence(document_hash=HASH_B)
        v = validator_with(src, evd)
        v._validate_evidence(evd)
        self.assertIn("PROVENANCE-001", rule_codes(v))

    def test_evidence_cannot_add_hash_when_source_is_unhashed(self):
        src = source(source_format="html", primary_secondary="secondary",
                     document_hash=None)
        evd = evidence(document_hash=HASH_A)
        v = validator_with(src, evd)
        v._validate_evidence(evd)
        self.assertIn("PROVENANCE-002", rule_codes(v))

    def test_missing_source_fails(self):
        evd = evidence(source_id="SRC-MISSING-999")
        v = validator_with(evd)
        v._validate_evidence(evd)
        self.assertIn("PHANTOM-001", rule_codes(v))


class ClaimVerificationTests(unittest.TestCase):
    def setUp(self):
        self.atomicity_event = {
            "type": "assessment_event", "action": "atomicity_verification",
            "target_object_id": "CLM-TEST-001",
        }

    def test_cross_verified_requires_two_independent_sources(self):
        s1 = source("SRC-TEST-001", independence=True)
        s2 = source("SRC-TEST-002", independence=True, document_hash=HASH_B)
        e1 = evidence("EVD-TEST-001", "SRC-TEST-001", HASH_A)
        e2 = evidence("EVD-TEST-002", "SRC-TEST-002", HASH_B)
        c = claim(verification_level="cross_verified",
                  related_evidence=["EVD-TEST-001", "EVD-TEST-002"])
        v = validator_with(s1, s2, e1, e2, c)
        v.events = [self.atomicity_event]
        v._validate_claim(c)
        self.assertNotIn("VERIFICATION-002", rule_codes(v))

    def test_two_sources_not_marked_independent_do_not_cross_verify(self):
        s1 = source("SRC-TEST-001", independence=False)
        s2 = source("SRC-TEST-002", independence=False, document_hash=HASH_B)
        e1 = evidence("EVD-TEST-001", "SRC-TEST-001", HASH_A)
        e2 = evidence("EVD-TEST-002", "SRC-TEST-002", HASH_B)
        c = claim(verification_level="cross_verified",
                  related_evidence=["EVD-TEST-001", "EVD-TEST-002"])
        v = validator_with(s1, s2, e1, e2, c)
        v.events = [self.atomicity_event]
        v._validate_claim(c)
        self.assertIn("VERIFICATION-002", rule_codes(v))

    def test_resolved_contradiction_without_resolution_evidence_fails(self):
        c = claim(contradiction_status="resolved",
                  contradiction_resolution="A narrative explanation only.")
        v = validator_with(c)
        v.events = [self.atomicity_event]
        v._validate_claim(c)
        self.assertIn("CONTRADICTION-002", rule_codes(v))

    def test_resolved_contradiction_with_dangling_resolution_evidence_fails(self):
        c = claim(contradiction_status="resolved",
                  contradiction_resolution="See the cited record.",
                  contradiction_resolution_evidence=["EVD-MISSING-999"])
        v = validator_with(c)
        v.events = [self.atomicity_event]
        v._validate_claim(c)
        self.assertIn("PHANTOM-003", rule_codes(v))

    def test_resolved_contradiction_with_existing_evidence_passes_structural_check(self):
        src, evd = source(), evidence()
        c = claim(contradiction_status="resolved",
                  contradiction_resolution="Resolution is documented in the cited evidence.",
                  contradiction_resolution_evidence=["EVD-TEST-001"])
        v = validator_with(src, evd, c)
        v.events = [self.atomicity_event]
        v._validate_claim(c)
        self.assertNotIn("CONTRADICTION-001", rule_codes(v))
        self.assertNotIn("CONTRADICTION-002", rule_codes(v))
        # This is only a structural pass; it does not establish truth.


class EvidenceGapTests(unittest.TestCase):
    def test_not_found_is_valid_without_claim_of_absence(self):
        g = gap()
        v = validator_with(g)
        v._validate_evidence_gap(g)
        self.assertEqual(rule_codes(v), set())

    def test_gap_with_nonexistent_claim_fails(self):
        g = gap(related_claim_id="CLM-MISSING-999")
        v = validator_with(g)
        v._validate_evidence_gap(g)
        self.assertIn("GAP-001", rule_codes(v))

    def test_confirmed_absent_requires_absence_basis(self):
        g = gap(search_result="confirmed_absent", absence_basis=None)
        v = validator_with(g)
        v._validate_evidence_gap(g)
        self.assertIn("GAP-004", rule_codes(v))

    def test_confirmed_absent_requires_linked_evidence(self):
        g = gap(search_result="confirmed_absent",
                absence_basis="Agency response says no responsive records exist.")
        v = validator_with(g)
        v._validate_evidence_gap(g)
        self.assertIn("GAP-006", rule_codes(v))

    def test_gap_dangling_result_evidence_fails(self):
        g = gap(result_evidence=["EVD-MISSING-999"])
        v = validator_with(g)
        v._validate_evidence_gap(g)
        self.assertIn("GAP-005", rule_codes(v))

    def test_confirmed_absent_with_evidence_reference_passes_structural_check(self):
        src = source()
        evd = evidence()
        g = gap(search_result="confirmed_absent",
                absence_basis="The cited agency response explicitly states no records exist.",
                result_evidence=["EVD-TEST-001"])
        v = validator_with(src, evd, g)
        v._validate_evidence_gap(g)
        self.assertEqual(rule_codes(v), set())


if __name__ == "__main__":
    unittest.main()
