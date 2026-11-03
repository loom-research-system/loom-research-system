"""Compile a Loom Brief from a research record and validated claims.

A Brief is a transparent synthesis layer. It never creates a new factual claim.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def compile_brief(inquiry, claims, gaps=None):
    gaps = gaps or []
    usable = [c for c in claims if c.get("promotion_stage") in {"accepted", "canonical"} and c.get("verification_level") != "none"]
    supported = [c for c in usable if c.get("epistemic_status") in {"supported", "known"}]
    contested = [c for c in usable if c.get("contradiction_status") in {"documented", "unresolved"}]
    if supported:
        headline = supported[0].get("statement", "")
        status = "supported"
    elif usable:
        headline = "The published record supports a qualified answer, but not a definitive conclusion."
        status = "qualified"
    else:
        headline = "Loom does not yet have enough validated evidence to publish a substantive answer."
        status = "evidence_limited"
    return {
        "version": "0.1",
        "type": "loom_brief",
        "inquiry_id": inquiry.get("id"),
        "question": inquiry.get("question"),
        "status": status,
        "headline": headline,
        "answer_basis": "Compiled only from accepted/canonical claims in the validated research record.",
        "key_findings": usable,
        "contested_or_unresolved": contested,
        "evidence_gaps": gaps,
        "limits": [
            "This Brief does not treat missing evidence as evidence of absence.",
            "Claims remain bounded by their current_as_of dates and verification levels.",
        ],
        "escalation": "A Full Loom Audit is appropriate when the unresolved evidence, institutional chain, or competing explanations materially affect the question.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inquiry", type=Path)
    parser.add_argument("claims", type=Path)
    parser.add_argument("--gaps", type=Path)
    args = parser.parse_args()
    inquiry = json.loads(args.inquiry.read_text(encoding="utf-8"))
    claims = json.loads(args.claims.read_text(encoding="utf-8"))
    gaps = json.loads(args.gaps.read_text(encoding="utf-8")) if args.gaps else []
    print(json.dumps(compile_brief(inquiry, claims, gaps), indent=2))

if __name__ == "__main__":
    main()
