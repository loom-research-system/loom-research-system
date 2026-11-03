import json
import tempfile
import unittest
from pathlib import Path

from scripts.route_inquiry import classify, make_inquiry
from scripts.plan_inquiry import build
from scripts.build_loom_brief import compile_brief
from scripts.build_loom_audit import compile_audit

class InquiryPipelineTests(unittest.TestCase):
    def test_routes_implementation_question(self):
        self.assertEqual(classify("Did the governor actually implement this policy?").question_type, "implementation_status")

    def test_routes_legislative_question_without_substring_false_positive(self):
        self.assertEqual(classify("What is the compass for this program?").question_type, "full_research")

    def test_created_inquiry_is_complete_enough_for_schema(self):
        inquiry = make_inquiry("Where did the money go?", "quick_read", "INQ-9001")
        self.assertEqual(inquiry["id"], "INQ-9001")
        self.assertIn("created", inquiry)
        self.assertIn("updated", inquiry)

    def test_plan_preserves_question_type_and_has_stopping_conditions(self):
        inquiry = make_inquiry("Did the government implement this policy?", "loom_brief", "INQ-9002")
        plan = build(inquiry, "PLAN-9001")
        self.assertEqual(plan["question_type"], "implementation_status")
        self.assertTrue(plan["research_steps"])
        self.assertTrue(plan["stopping_conditions"])

    def test_brief_does_not_publish_unvalidated_claims(self):
        inquiry = make_inquiry("Did the government implement this policy?", "loom_brief", "INQ-9003")
        claims = [
            {"id":"CLM-1","statement":"Unsupported candidate claim","promotion_stage":"candidate","verification_level":"source_backed","epistemic_status":"proposed"},
            {"id":"CLM-2","statement":"Validated finding","promotion_stage":"accepted","verification_level":"cross_verified","epistemic_status":"supported","contradiction_status":"none"},
        ]
        brief = compile_brief(inquiry, claims)
        self.assertEqual(brief["headline"], "Validated finding")
        self.assertEqual(len(brief["key_findings"]), 1)

    def test_audit_keeps_gaps_visible(self):
        inquiry = make_inquiry("What happened?", "full_loom_audit", "INQ-9004")
        plan = build(inquiry, "PLAN-9002")
        gaps = [{"id":"GAP-1","search_result":"not_found","missing_information":"A missing record"}]
        audit = compile_audit(inquiry, plan, [], gaps)
        self.assertEqual(audit["audit_status"], "incomplete_or_unresolved")
        self.assertEqual(len(audit["evidence_gaps"]), 1)

if __name__ == "__main__":
    unittest.main()
