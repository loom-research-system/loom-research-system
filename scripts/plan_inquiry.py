"""Compile a deterministic research plan from a Loom inquiry.

This creates the worklist for human/agent research. It does not claim that any
source exists or that any conclusion is established.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_DIR = ROOT / "research" / "plans"

TEMPLATES = {
    "implementation_status": [
        ("decision", "Identify the formal decision or policy commitment.", "authorizing document"),
        ("authority", "Identify who had legal/administrative authority to implement it.", "authority assignment or governing instrument"),
        ("requirements", "Reconstruct the conditions and dependencies required for implementation.", "implementation instructions, contracts, budgets, dependencies"),
        ("execution", "Test what actions were actually taken and when.", "execution records, operational evidence"),
        ("current_state", "Establish the current documented implementation state.", "current official record"),
    ],
    "legislative_likelihood": [
        ("status", "Establish the bill's formal procedural status.", "legislative record"),
        ("path", "Reconstruct remaining procedural steps and dependencies.", "rules, calendar, committee/action record"),
        ("signals", "Collect documented actions that materially affect the path.", "official actions and reliable contemporaneous reporting"),
        ("uncertainty", "Record factors that could change the assessment.", "documented contingencies"),
    ],
    "promise_commitment": [
        ("promise", "Identify the exact public commitment and date.", "primary statement or official commitment"),
        ("authority", "Determine what authority and resources were required.", "law, budget, executive or agency authority"),
        ("execution", "Test documented actions against the commitment.", "implementation record"),
        ("status", "Determine whether the commitment is fulfilled, partial, unresolved, or not supported.", "current evidence"),
    ],
    "spending_funding": [
        ("authorization", "Identify the funding authorization and intended purpose.", "appropriation, award, or budget record"),
        ("obligation", "Trace documented obligations or commitments.", "contract, award, obligation record"),
        ("disbursement", "Trace documented payments or expenditures where available.", "payment/expenditure record"),
        ("gap", "Identify missing financial evidence and its availability.", "accounting or oversight records"),
    ],
    "responsibility_authority": [
        ("mandate", "Identify the formal authority structure.", "statute, regulation, order, charter, delegation"),
        ("decision", "Identify who made the relevant decision.", "decision record"),
        ("execution", "Identify who was responsible for operational action.", "assignment, contract, agency record"),
        ("oversight", "Identify who could detect, correct, or escalate failure.", "oversight mandate and record"),
    ],
    "outcome": [
        ("intervention", "Establish what intervention or policy action occurred.", "implementation record"),
        ("baseline", "Establish the relevant baseline or comparison state.", "baseline evidence"),
        ("outcome", "Collect evidence of observed results.", "outcome measures or primary records"),
        ("alternatives", "Test competing explanations where the evidence permits.", "countervailing evidence"),
    ],
    "historical_reconstruction": [
        ("timeline", "Establish the sequence of documented decisions and actions.", "dated primary records"),
        ("authority", "Map institutional authority at each material transition.", "governing instruments and assignments"),
        ("dependencies", "Identify dependencies that affected transitions.", "contracts, budgets, procedures, technical or institutional dependencies"),
        ("gaps", "Register unresolved evidence and competing explanations.", "evidence gaps"),
    ],
    "full_research": [
        ("scope", "Define the proposition, actors, jurisdiction, and time boundary.", "scope-defining records"),
        ("timeline", "Construct the documented institutional sequence.", "dated primary records"),
        ("mechanisms", "Test candidate explanations against the evidence.", "mechanism-specific evidence"),
        ("gaps", "Search and formally register unresolved evidence.", "evidence gaps and search protocols"),
        ("synthesis", "Compile only conclusions supported by the validated record.", "validated claims"),
    ],
}


def build(inquiry: dict, plan_id: str):
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    qtype = inquiry["question_type"]
    steps = []
    for i, (sid, purpose, target) in enumerate(TEMPLATES.get(qtype, TEMPLATES["full_research"]), 1):
        steps.append({"id": f"{i:02d}-{sid}", "purpose": purpose, "evidence_target": target, "suggested_sources": [], "status": "pending"})
    return {
        "id": plan_id,
        "type": "research_plan",
        "inquiry_id": inquiry["id"],
        "question_type": qtype,
        "depth": inquiry["requested_depth"],
        "objective": f"Establish what can be supported about: {inquiry['question']}",
        "research_steps": steps,
        "stopping_conditions": [
            "Do not convert absence of evidence into evidence of absence.",
            "Register unresolved material questions as evidence gaps.",
            "Stop a public conclusion at the strongest epistemic state supported by validated evidence.",
        ],
        "unresolved_questions": [],
        "status": "ready",
        "created": now,
        "updated": now,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inquiry", type=Path)
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    inquiry = json.loads(args.inquiry.read_text(encoding="utf-8"))
    plan = build(inquiry, args.id)
    PLAN_DIR.mkdir(parents=True, exist_ok=True)
    out = PLAN_DIR / f"{args.id}.json"
    out.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(plan, indent=2))

if __name__ == "__main__":
    main()
