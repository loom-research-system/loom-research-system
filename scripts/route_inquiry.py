"""Classify a public question into a Loom Inquiry routing record.

This module deliberately does not answer questions. It creates the typed research
request that a later evidence/research layer can resolve.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict

@dataclass(frozen=True)
class Route:
    question_type: str
    rationale: str

PATTERNS = [
    ("implementation_status", [r"\bimplement(?:ed|ation|ing)?\b", r"\bin effect\b", r"\bactually doing\b", r"\bcarried out\b", r"\benforced\b"]),
    ("legislative_likelihood", [r"\bpass\b", r"\bpassed\b", r"\bbecome law\b", r"\blegislation\b", r"\bbill\b"]),
    ("promise_commitment", [r"\bpromise\b", r"\bpromised\b", r"\bcommitment\b", r"\bpledged\b", r"\bsaid they would\b"]),
    ("spending_funding", [r"\bmoney\b", r"\bfund(?:ing)?\b", r"\bspent\b", r"\bspending\b", r"\bbudget\b", r"\ballocated\b"]),
    ("responsibility_authority", [r"\bwho was responsible\b", r"\bwho had authority\b", r"\bresponsible for\b", r"\bwho could\b", r"\bwho decided\b"]),
    ("outcome", [r"\bworked\b", r"\boutcome\b", r"\bresult\b", r"\bdid it help\b", r"\bwhat happened\b"]),
    ("historical_reconstruction", [r"\bwhat happened\b", r"\bhow did\b", r"\bwhy did\b", r"\btimeline\b", r"\bhistory\b"]),
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
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "id": inquiry_id,
        "type": "inquiry",
        "question": question.strip(),
        "question_type": route.question_type,
        "scope": {"jurisdiction": "", "subject": "", "identifiers": []},
        "requested_depth": requested_depth,
        "status": "classified",
        "routing_rationale": route.rationale,
        "created": now,
        "updated": now,
    }

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--depth", default="quick_read", choices=["quick_read", "loom_brief", "full_loom_audit"])
    args = parser.parse_args()
    print(json.dumps(make_inquiry(args.question, args.depth), indent=2))
