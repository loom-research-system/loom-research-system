"""JSON Schema contract tests for Loom's source, evidence, claim, and gap records."""
import unittest
from pathlib import Path

import jsonschema
import yaml
from jsonschema import Draft7Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def load_schema(name):
    with (SCHEMA_DIR / name).open(encoding="utf-8-sig") as stream:
        return yaml.safe_load(stream)


def is_valid(schema_name, record):
    schema = load_schema(schema_name)
    validator = Draft7Validator(schema, format_checker=FormatChecker())
    return not list(validator.iter_errors(record))


def source_record(**overrides):
    record = {
        "id": "SRC-TEST-001", "type": "source", "title": "Test document",
        "publisher": "Test Agency", "date": "2023-01-01",
        "primary_secondary": "primary", "independence": True,
        "retrieved": True, "retrieval_method": "direct_download",
        "source_format": "pdf", "document_hash": "sha256:" + "a" * 64,
        "copyright_status": "unknown",
        "source_assessment": {
            "quality_rating": "high",
            "factors": ["directness: high"],
            "rationale": "Test source record.",
        },
    }
    record.update(overrides)
    return record


def claim_record(**overrides):
    record = {
        "id": "CLM-TEST-001", "type": "claim", "claim_type": "standard",
        "statement": "Test proposition.", "status": "under_review",
        "epistemic_status": "proposed", "verification_level": "source_backed",
        "promotion_stage": "candidate", "primary_applicability": "applicable",
        "current_as_of": "2023-10-01", "related_evidence": [],
        "contradiction_status": "none",
        "created": "2023-10-01T11:00:00Z", "updated": "2023-10-01T11:00:00Z",
    }
    record.update(overrides)
    return record


def gap_record(**overrides):
    record = {
        "id": "GAP-TEST-001", "type": "evidence_gap",
        "missing_information": "A missing record", "search_performed": True,
        "search_result": "not_found", "search_scope": ["Test archive"],
        "search_methods": ["keyword_search"],
        "search_performed_at": "2023-10-01T12:00:00Z",
        "created": "2023-10-01T12:00:00Z", "updated": "2023-10-01T12:00:00Z",
    }
    record.update(overrides)
    return record


class SchemaContractTests(unittest.TestCase):
    def test_all_four_schemas_are_valid_draft7_schemas(self):
        for name in ("source.schema.yaml", "evidence.schema.yaml",
                     "claim.schema.yaml", "evidence_gap.schema.yaml"):
            with self.subTest(schema=name):
                Draft7Validator.check_schema(load_schema(name))

    def test_hashed_primary_pdf_is_valid(self):
        self.assertTrue(is_valid("source.schema.yaml", source_record()))

    def test_unhashed_secondary_web_page_is_valid(self):
        record = source_record(
            id="SRC-TEST-002", primary_secondary="secondary",
            source_format="html", retrieval_method="web_page", document_hash=None,
        )
        self.assertTrue(is_valid("source.schema.yaml", record))

    def test_retrieved_primary_pdf_without_hash_is_invalid(self):
        record = source_record(document_hash=None)
        self.assertFalse(is_valid("source.schema.yaml", record))

    def test_unknown_retrieval_method_is_invalid(self):
        record = source_record(retrieval_method="web_browser")
        self.assertFalse(is_valid("source.schema.yaml", record))

    def test_valid_evidence_record_is_accepted(self):
        record = {
            "id": "EVD-TEST-001", "type": "evidence", "source_id": "SRC-TEST-001",
            "extracted_content": "Test excerpt", "location": "Page 1",
            "retrieved_at": "2023-10-01T10:00:00Z",
            "document_hash": "sha256:" + "a" * 64,
            "extracted_by": "human:FOUNDER", "extraction_method": "manual_copy",
        }
        self.assertTrue(is_valid("evidence.schema.yaml", record))

    def test_invalid_extraction_method_is_rejected(self):
        record = {
            "id": "EVD-TEST-001", "type": "evidence", "source_id": "SRC-TEST-001",
            "extracted_content": "Test excerpt", "location": "Page 1",
            "retrieved_at": "2023-10-01T10:00:00Z",
            "document_hash": None, "extracted_by": "human:FOUNDER",
            "extraction_method": "copy_paste_from_browser",
        }
        self.assertFalse(is_valid("evidence.schema.yaml", record))

    def test_resolved_claim_requires_nonempty_resolution_and_evidence(self):
        record = claim_record(contradiction_status="resolved")
        self.assertFalse(is_valid("claim.schema.yaml", record))
        record["contradiction_resolution"] = "Resolution is supported by the cited evidence."
        record["contradiction_resolution_evidence"] = ["EVD-TEST-001"]
        self.assertTrue(is_valid("claim.schema.yaml", record))

    def test_confirmed_absent_gap_requires_basis_and_evidence(self):
        record = gap_record(search_result="confirmed_absent")
        self.assertFalse(is_valid("evidence_gap.schema.yaml", record))
        record["absence_basis"] = "The agency response explicitly states no records exist."
        record["result_evidence"] = ["EVD-TEST-001"]
        self.assertTrue(is_valid("evidence_gap.schema.yaml", record))

    def test_not_found_gap_does_not_require_absence_claim(self):
        self.assertTrue(is_valid("evidence_gap.schema.yaml", gap_record()))


if __name__ == "__main__":
    unittest.main()
