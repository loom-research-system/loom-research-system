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
