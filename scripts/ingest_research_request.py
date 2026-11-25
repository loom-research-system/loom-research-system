"""Idempotently ingest a GitHub research-request issue as a Loom inquiry and plan."""
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


def extract_section(body: str, headings: tuple[str, ...]) -> str:
    names = "|".join(re.escape(h) for h in headings)
    pattern = rf"(?ims)^#{{2,3}}\s*(?:{names})\s*\n+(.*?)(?=^#{{2,3}}\s|\Z)"
    match = re.search(pattern, body or "")
    if not match:
        return ""
    value = match.group(1).strip()
    return "" if value in {"_No response_", "_No response"} else value


def extract_question(body: str) -> str:
    question = extract_section(body, ("Question", "What do you want to know?"))
    return question or (body or "").strip()


def requested_depth(body: str) -> str:
    value = extract_section(body, ("Requested depth",)).lower()
    if "audit" in value:
        return "full_loom_audit"
    if "brief" in value:
        return "loom_brief"
    return "quick_read"


def ingest(number: int, title: str, body: str, url: str):
    if number < 1:
        raise ValueError("GitHub issue number must be positive.")
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
    scope_text = extract_section(body, ("Helpful scope or identifiers", "Scope or identifiers"))
    inquiry = {
        "id": inquiry_id,
        "type": "inquiry",
        "question": question,
        "question_type": route.question_type,
        "scope": {"jurisdiction": "", "subject": "", "identifiers": [scope_text] if scope_text else []},
        "requested_depth": requested_depth(body),
        "status": "received",
        "routing_rationale": route.rationale,
        "source_request": {
            "platform": "github_issue",
            "issue_number": number,
            "title": title,
            "issue_url": url,
        },
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
            output.write("inquiry_id=" + inquiry["id"] + "\n")
    print(json.dumps({"created": created, "inquiry": inquiry, "inquiry_path": str(ip), "plan_path": str(pp)}, indent=2))


if __name__ == "__main__":
    main()
