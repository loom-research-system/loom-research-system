"""Compile a Full Loom Audit record from the validated research components."""
from __future__ import annotations
import argparse, json
from pathlib import Path


def compile_audit(inquiry, plan, claims, gaps, transitions=None, mechanisms=None):
    transitions = transitions or []
    mechanisms = mechanisms or []
    usable = [c for c in claims if c.get("promotion_stage") in {"accepted", "canonical"} and c.get("verification_level") != "none"]
    return {
        "version": "0.1",
        "type": "full_loom_audit",
        "inquiry_id": inquiry.get("id"),
        "question": inquiry.get("question"),
        "research_plan": plan,
        "validated_claims": usable,
        "evidence_gaps": gaps,
        "institutional_transitions": transitions,
        "candidate_mechanisms": mechanisms,
        "epistemic_boundary": {
            "rule": "AI may propose. Evidence must establish. Humans may promote.",
            "note": "Only validated claims are included as findings; unresolved gaps remain visible.",
        },
        "audit_status": "complete" if plan.get("status") == "complete" and not any(g.get("search_result") in {"pending", "not_found"} for g in gaps) else "incomplete_or_unresolved",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inquiry", type=Path)
    parser.add_argument("plan", type=Path)
    parser.add_argument("claims", type=Path)
    parser.add_argument("gaps", type=Path)
    args = parser.parse_args()
    inquiry = json.loads(args.inquiry.read_text(encoding="utf-8"))
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    claims = json.loads(args.claims.read_text(encoding="utf-8"))
    gaps = json.loads(args.gaps.read_text(encoding="utf-8"))
    print(json.dumps(compile_audit(inquiry, plan, claims, gaps), indent=2))

if __name__ == "__main__":
    main()
