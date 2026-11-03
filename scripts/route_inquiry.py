"""Classify a public question into a Loom Inquiry routing record.

This module deliberately does not answer questions. It creates the typed research
request that a later evidence/research layer can resolve.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class Route:
    question_type: str
    rationale: str

PATTERNS = [
    ("implementation_status", [r"implemented", r"implementation", r"in effect", r"actually doing", r"carried out", r"enforced"]),
    ("legislative_likelihood", [r"pass", r"passed", r"become law", r"legislation", r"bill"]),
    ("promise_commitment", [r"promise", r"promised", r"commitment", r"pledged", r"said they would"]),
    ("spending_funding", [r"money", r"fund", r"funding", r"spent", r"spending", r"budget", r"allocated"]),
    ("responsibility_authority", [r"who was responsible", r"who had authority", r"responsible for", r"who could", r"who decided"]),
    ("outcome", [r"worked", r"outcome", r"result", r"did it help", r"what happened"]),
    ("historical_reconstruction", [r"what happened", r"how did", r"why did", r"timeline", r"history"]),
]

def classify(question: str) -> Route:
    text = question.lower().strip()
    for question_type, patterns in PATTERNS:
        for pattern in patterns:
            if re.search(pattern, text):
                return Route(question_type, f"Matched public inquiry pattern: {pattern}")
    return Route("full_research", "No narrow route matched; preserve the question for research triage.")

def make_inquiry(question: str, requested_depth: str = "quick_read", inquiry_id: str = "INQ-0001") -> Dict:
    route = classify(question)
    return {"id": inquiry_id, "type": "inquiry", "question": question.strip(), "question_type": route.question_type, "scope": {"jurisdiction": "", "subject": "", "identifiers": []}, "requested_depth": requested_depth, "status": "classified", "routing_rationale": route.rationale}

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--depth", default="quick_read", choices=["quick_read", "loom_brief", "full_loom_audit"])
    args = parser.parse_args()
    print(json.dumps(make_inquiry(args.question, args.depth), indent=2))
