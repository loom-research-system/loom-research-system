import unittest
import jsonschema
import yaml
from pathlib import Path

from scripts.build_loom_brief import compile_brief
from scripts.build_loom_audit import compile_audit

ROOT = Path(__file__).resolve().parents[1]


class ClaimPromotionVocabularyTests(unittest.TestCase):
    def setUp(self):
        with (ROOT / "schemas" / "claim.schema.yaml").open(encoding="utf-8") as stream:
            self.schema = yaml.safe_load(stream)

    def test_schema_uses_locked_promotion_stages(self):
        self.assertEqual(
            self.schema["properties"]["promotion_stage"]["enum"],
            ["candidate", "supported", "canonical"],
        )

    def test_accepted_is_not_a_valid_promotion_stage(self):
        validator = jsonschema.Draft7Validator(self.schema)
        errors = list(validator.iter_errors({
            "id": "CLM-001",
            "type": "claim",
            "claim_type": "standard",
            "statement": "A test statement.",
            "status": "under_review",
            "epistemic_status": "supported",
            "verification_level": "source_backed",
            "promotion_stage": "accepted",
            "primary_applicability": "not_applicable",
            "current_as_of": "2026-11-25",
            "related_evidence": [],
            "contradiction_status": "none",
            "created": "2026-11-25T00:00:00Z",
            "updated": "2026-11-25T00:00:00Z",
        }))
        self.assertTrue(any(list(error.absolute_path) == ["promotion_stage"] for error in errors))

    def test_brief_includes_supported_and_canonical_not_accepted(self):
        inquiry = {"id": "INQ-TEST-0001", "question": "Test?"}
        claims = [
            {"id": "CLM-001", "statement": "Supported claim", "promotion_stage": "supported", "verification_level": "source_backed", "epistemic_status": "supported", "contradiction_status": "none"},
            {"id": "CLM-002", "statement": "Canonical claim", "promotion_stage": "canonical", "verification_level": "cross_verified", "epistemic_status": "known", "contradiction_status": "none"},
            {"id": "CLM-003", "statement": "Legacy accepted claim", "promotion_stage": "accepted", "verification_level": "source_backed", "epistemic_status": "supported", "contradiction_status": "none"},
        ]
        brief = compile_brief(inquiry, claims)
        self.assertEqual([claim["id"] for claim in brief["key_findings"]], ["CLM-001", "CLM-002"])

    def test_audit_includes_supported_and_canonical_not_accepted(self):
        inquiry = {"id": "INQ-TEST-0001", "question": "Test?"}
        plan = {"status": "ready"}
        claims = [
            {"id": "CLM-001", "promotion_stage": "supported", "verification_level": "source_backed"},
            {"id": "CLM-002", "promotion_stage": "canonical", "verification_level": "primary_verified"},
            {"id": "CLM-003", "promotion_stage": "accepted", "verification_level": "source_backed"},
        ]
        audit = compile_audit(inquiry, plan, claims, [])
        self.assertEqual([claim["id"] for claim in audit["validated_claims"]], ["CLM-001", "CLM-002"])


if __name__ == "__main__":
    unittest.main()
