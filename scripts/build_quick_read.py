"""Compile a Quick Read from already-published claims.

This is intentionally a compiler, not an LLM answerer: if no promoted claim
supports the inquiry, it returns an explicit evidence-limited result.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from scripts.route_inquiry import classify


def _tokens(text):
    return {t for t in re.findall(r"[a-z0-9]{4,}", text.lower()) if t not in {"what", "this", "that", "does", "actually", "government"}}


def compile_quick_read(question, index):
    route = classify(question)
    q_tokens = _tokens(question)
    scored = []
    for claim in index.get("claims", []):
        score = len(q_tokens & _tokens(claim.get("statement", "")))
        if score:
            scored.append((score, claim))
    scored.sort(key=lambda item: item[0], reverse=True)
    matches = [claim for _, claim in scored[:5]]
    if not matches:
        return {
            "status": "evidence_limited",
            "question": question,
            "question_type": route.question_type,
            "headline": "Loom cannot support an answer from the published evidence yet.",
            "explanation": "The question has been classified, but no promoted claim in the public research index is sufficiently related to it. That is a research gap, not permission to guess.",
            "claims": [],
            "next_step": "Escalate to a Loom Brief or Full Loom Audit if this question matters enough to investigate.",
        }
    strongest = matches[0]
    return {
        "status": "supported" if strongest.get("epistemic_status") in {"supported", "known"} else "qualified",
        "question": question,
        "question_type": route.question_type,
        "headline": strongest["statement"],
        "explanation": "This Quick Read is compiled from promoted Loom claims. It does not generate a new factual claim.",
        "claims": matches,
        "next_step": "Open the Loom Brief for the reconstruction and evidence trail.",
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("index", type=Path)
    args = parser.parse_args()
    index = json.loads(args.index.read_text(encoding="utf-8"))
    print(json.dumps(compile_quick_read(args.question, index), indent=2))

if __name__ == "__main__":
    main()
