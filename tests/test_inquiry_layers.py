import unittest
from scripts.route_inquiry import classify, make_inquiry


class InquiryLayerTests(unittest.TestCase):
    def test_implementation_route(self):
        route = classify("Did the governor actually implement this policy?")
        self.assertEqual(route.question_type, "implementation_status")

    def test_legislative_route(self):
        route = classify("What are the odds of this bill passing?")
        self.assertEqual(route.question_type, "legislative_likelihood")

    def test_unknown_questions_are_preserved_for_research(self):
        inquiry = make_inquiry("Tell me something unusual about this agency")
        self.assertEqual(inquiry["type"], "inquiry")
        self.assertEqual(inquiry["status"], "classified")
        self.assertEqual(inquiry["question_type"], "full_research")


if __name__ == "__main__":
    unittest.main()
