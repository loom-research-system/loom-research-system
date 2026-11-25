import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import jsonschema
import yaml
from scripts import ingest_research_request as intake
from scripts import process_research_request


class ResearchRequestExtractionTests(unittest.TestCase):
    def test_prefilled_public_ask_loom_body(self):
        body = "## What do you want to know?\n\nDid Hochul's AI data center policy create the jobs promised?\n\n## Requested depth\n\nQuick Read"
        self.assertEqual(intake.extract_question(body), "Did Hochul's AI data center policy create the jobs promised?")

    def test_github_issue_form_three_hash_heading(self):
        body = "### What do you want to know?\n\nDid the agency implement the policy?\n\n### Helpful scope or identifiers\n\nNew York"
        self.assertEqual(intake.extract_question(body), "Did the agency implement the policy?")

    def test_classic_question_heading(self):
        body = "## Question\n\nWhere did the grant funding go?\n\n## Context\n\nCounty program"
        self.assertEqual(intake.extract_question(body), "Where did the grant funding go?")

    def test_requested_depth_is_preserved(self):
        self.assertEqual(intake.requested_depth("### Requested depth\n\nFull Loom Audit"), "full_loom_audit")
        self.assertEqual(intake.requested_depth("### Requested depth\n\nLoom Brief"), "loom_brief")
        self.assertEqual(intake.requested_depth("### Requested depth\n\nQuick Read"), "quick_read")


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
                self.assertEqual(inquiry["requested_depth"], "quick_read")
                self.assertEqual(inquiry["source_request"]["issue_number"], 42)
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

    def test_workflow_adapter_uses_same_ingester_and_id_scheme(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            event = root / "event.json"
            event.write_text(json.dumps({"issue": {
                "number": 44,
                "title": "Question",
                "body": "### What do you want to know?\n\nDid the agency implement this?\n\n### Requested depth\n\nLoom Brief",
                "html_url": "https://github.com/example/repo/issues/44",
            }}), encoding="utf-8")
            with patch.object(intake, "INQUIRY_DIR", root / "inquiries"), patch.object(intake, "PLAN_DIR", root / "plans"):
                inquiry_path, plan_path, inquiry, created = process_research_request.process(event)
                self.assertTrue(created)
                self.assertEqual(inquiry["id"], "INQ-GH-0044")
                self.assertEqual(inquiry["requested_depth"], "loom_brief")
                self.assertEqual(inquiry["source_request"]["issue_url"], "https://github.com/example/repo/issues/44")
                self.assertTrue(inquiry_path.exists())
                self.assertTrue(plan_path.exists())


if __name__ == "__main__":
    unittest.main()
