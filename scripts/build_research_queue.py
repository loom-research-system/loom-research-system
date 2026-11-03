"""Build a machine-readable research queue from persistent inquiries and plans."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INQUIRY_DIR = ROOT / "research" / "inquiries"
PLAN_DIR = ROOT / "research" / "plans"
OUT = ROOT / "research" / "queue.json"


def load_dir(path):
    records = {}
    if path.exists():
        for p in path.glob("*.json"):
            try:
                obj = json.loads(p.read_text(encoding="utf-8"))
                if obj.get("id"):
                    records[obj["id"]] = obj
            except (OSError, json.JSONDecodeError):
                pass
    return records


def main():
    inquiries = load_dir(INQUIRY_DIR)
    plans = load_dir(PLAN_DIR)
    queue = []
    for inquiry in inquiries.values():
        plan = next((p for p in plans.values() if p.get("inquiry_id") == inquiry["id"]), None)
        if inquiry.get("status") in {"completed", "blocked"}:
            next_action = "review status"
        elif not plan:
            next_action = "create research plan"
        elif any(s.get("status") == "blocked" for s in plan.get("research_steps", [])):
            next_action = "resolve blocked research step"
        elif any(s.get("status") == "pending" for s in plan.get("research_steps", [])):
            next_action = "begin or continue evidence acquisition"
        else:
            next_action = "compile validated result"
        queue.append({
            "inquiry_id": inquiry["id"],
            "question": inquiry["question"],
            "question_type": inquiry["question_type"],
            "depth": inquiry["requested_depth"],
            "status": inquiry["status"],
            "plan_id": plan.get("id") if plan else None,
            "next_action": next_action,
            "updated": inquiry.get("updated"),
        })
    queue.sort(key=lambda x: (x["status"], x["inquiry_id"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"version": "0.1", "inquiries": queue}, indent=2) + "\n", encoding="utf-8")
    print(f"Built research queue: {len(queue)} inquiries")

if __name__ == "__main__":
    main()
