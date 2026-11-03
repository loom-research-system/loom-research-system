import unittest
from scripts.ingest_research_request import extract_question

class ResearchRequestExtractionTests(unittest.TestCase):
    def test_prefilled_public_ask_loom_body(self):
        body = "## What do you want to know?\n\nDid Hochul's AI data center policy create the jobs promised?\n\n## Requested depth\n\nQuick Read"
        self.assertEqual(extract_question(body), "Did Hochul's AI data center policy create the jobs promised?")

    def test_github_issue_form_three_hash_heading(self):
        body = "### What do you want to know?\n\nDid the agency implement the policy?\n\n### Helpful scope or identifiers\n\nNew York"
        self.assertEqual(extract_question(body), "Did the agency implement the policy?")

    def test_classic_question_heading(self):
        body = "## Question\n\nWhere did the grant funding go?\n\n## Context\n\nCounty program"
        self.assertEqual(extract_question(body), "Where did the grant funding go?")

if __name__ == "__main__":
    unittest.main()

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import jsonschema
import yaml
from scripts import ingest_research_request as intake

class ResearchRequestIntegrationTests(unittest.TestCase):
    def test_ingest_creates_schema_valid_linked_inquiry_and_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(intake, "INQUIRY_DIR", root / "inquiries"), patch.object(intake, "PLAN_DIR", root / "plans"):
                inquiry_path, plan_path, inquiry, created = intake.ingest(
                    42,
                    "[Ask Loom] Did the policy create the jobs promised?",
                    "## What do you want to know?\n\nDid Hochul's AI data center policy create the jobs promised?\n\n## Requested depth\n\nQuick Read",
                    "https://github.com/example/repo/issues/42",
                )
                self.assertTrue(created)
                self.assertTrue(inquiry_path.exists())
                self.assertTrue(plan_path.exists())
                plan = json.loads(plan_path.read_text(encoding="utf-8"))
                with (intake.ROOT / "schemas" / "inquiry.schema.yaml").open(encoding="utf-8") as stream:
                    inquiry_schema = yaml.safe_load(stream)
                with (intake.ROOT / "schemas" / "research_plan.schema.yaml").open(encoding="utf-8") as stream:
                    plan_schema = yaml.safe_load(stream)
                jsonschema.validate(inquiry, inquiry_schema)
                jsonschema.validate(plan, plan_schema)
                self.assertEqual(plan["inquiry_id"], inquiry["id"])
                self.assertEqual(inquiry["question"], "Did Hochul's AI data center policy create the jobs promised?")
                self.assertEqual(plan["status"], "ready")

    def test_duplicate_issue_intake_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(intake, "INQUIRY_DIR", root / "inquiries"), patch.object(intake, "PLAN_DIR", root / "plans"):
                first = intake.ingest(43, "Test", "## What do you want to know?\n\nDid the agency implement this?", "https://example.test/43")
                second = intake.ingest(43, "Test", "## What do you want to know?\n\nDid the agency implement this?", "https://example.test/43")
                self.assertTrue(first[3])
                self.assertFalse(second[3])
                self.assertEqual(first[2]["id"], second[2]["id"])
