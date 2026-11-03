"""Turn a submitted GitHub research-request issue into a persistent Loom Inquiry and plan."""
from __future__ import annotations
import argparse, json, os, re, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.route_inquiry import classify
from scripts.plan_inquiry import build as build_plan

INQUIRY_DIR = ROOT / "research" / "inquiries"
PLAN_DIR = ROOT / "research" / "plans"

def extract_question(body: str) -> str:
    # Accept both the dedicated issue-form heading and classic prefilled issue body.
    patterns = [
        r"(?ims)^#{2,3}\s*(?:Question|What do you want to know\?)\s*\n+(.*?)(?=^#{2,3}\s|\Z)",
        r"(?ims)^Question:\s*\n+(.*?)(?=^##\s|\Z)",
    ]
    for pattern in patterns:
        match = re.search(pattern, body)
        if match:
            value = match.group(1).strip()
            if value and value not in {"_No response_", "_No response"}:
                return value
    return body.strip()

def ingest(number: int, title: str, body: str, url: str):
    question = extract_question(body)
    if len(question) < 5:
        raise ValueError("Issue does not contain a usable research question.")
    inquiry_id = f"INQ-GH-{number:04d}"
    plan_id = f"PLAN-{number:04d}"
    INQUIRY_DIR.mkdir(parents=True, exist_ok=True)
    PLAN_DIR.mkdir(parents=True, exist_ok=True)
    inquiry_path = INQUIRY_DIR / f"{inquiry_id}.json"
    plan_path = PLAN_DIR / f"{plan_id}.json"
    if inquiry_path.exists():
        existing = json.loads(inquiry_path.read_text(encoding="utf-8"))
        if not plan_path.exists():
            plan = build_plan(existing, plan_id)
            plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        return inquiry_path, plan_path, existing, False
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    route = classify(question)
    inquiry = {
        "id": inquiry_id,
        "type": "inquiry",
        "question": question,
        "question_type": route.question_type,
        "scope": {"jurisdiction": "", "subject": "", "identifiers": []},
        "requested_depth": "quick_read",
        "status": "received",
        "routing_rationale": route.rationale,
        "created": now,
        "updated": now,
    }
    plan = build_plan(inquiry, plan_id)
    inquiry_path.write_text(json.dumps(inquiry, indent=2) + "\n", encoding="utf-8")
    plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    return inquiry_path, plan_path, inquiry, True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", type=int, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    ip, pp, inquiry, created = ingest(args.number, args.title, args.body, args.url)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
            output.write("inquiry_id=" + inquiry["id"] + "\\n")
    print(json.dumps({"created": created, "inquiry": inquiry, "inquiry_path": str(ip), "plan_path": str(pp)}, indent=2))

if __name__ == "__main__":
    main()
