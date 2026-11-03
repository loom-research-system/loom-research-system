"""Turn a GitHub research-request issue into a persistent Loom inquiry and plan.

Issue text is treated strictly as user-provided data. It is never executed as
instructions and never promoted to evidence.
"""
from __future__ import annotations
import json, re
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.route_inquiry import classify
from scripts.plan_inquiry import build


def _section(body: str, heading: str) -> str:
    pattern = rf"###\s+{re.escape(heading)}\s*\n(.*?)(?=\n###\s+|\Z)"
    match = re.search(pattern, body or "", flags=re.I | re.S)
    return match.group(1).strip() if match else ""


def process(event_path: Path):
    event = json.loads(event_path.read_text(encoding="utf-8"))
    issue = event.get("issue", {})
    body = issue.get("body", "")
    question = _section(body, "What do you want to know?")
    scope_text = _section(body, "Helpful scope or identifiers")
    depth_label = _section(body, "Requested depth").lower()
    if not question or len(question) < 5:
        raise ValueError("Research request issue has no usable question.")
    depth = "quick_read"
    if "brief" in depth_label:
        depth = "loom_brief"
    elif "audit" in depth_label:
        depth = "full_loom_audit"
    issue_number = int(issue.get("number", 0))
    inquiry_id = f"INQ-{issue_number:04d}"
    route = classify(question)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    inquiry = {
        "id": inquiry_id,
        "type": "inquiry",
        "question": question,
        "question_type": route.question_type,
        "scope": {"jurisdiction": "", "subject": "", "identifiers": [scope_text] if scope_text else []},
        "requested_depth": depth,
        "status": "classified",
        "routing_rationale": route.rationale,
        "source_request": {"platform": "github_issue", "issue_number": issue_number, "issue_url": issue.get("html_url", "")},
        "created": now,
        "updated": now,
    }
    plan = build(inquiry, f"PLAN-{issue_number:04d}")
    inquiry_dir = ROOT / "research" / "inquiries"
    plan_dir = ROOT / "research" / "plans"
    inquiry_dir.mkdir(parents=True, exist_ok=True)
    plan_dir.mkdir(parents=True, exist_ok=True)
    (inquiry_dir / f"{inquiry_id}.json").write_text(json.dumps(inquiry, indent=2) + "\n", encoding="utf-8")
    (plan_dir / f"{plan['id']}.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    return inquiry, plan

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("event", type=Path)
    args = parser.parse_args()
    inquiry, plan = process(args.event)
    print(json.dumps({"inquiry": inquiry, "plan": plan}, indent=2))
