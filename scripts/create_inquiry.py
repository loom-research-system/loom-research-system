"""Create a persistent, typed Loom research inquiry.

The inquiry is a research job, not an answer. Creation is deliberately separate
from evidence acquisition and claim promotion.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.route_inquiry import classify

INQUIRY_DIR = ROOT / "research" / "inquiries"
DEPTHS = {"quick_read", "loom_brief", "full_loom_audit"}


def create(question: str, depth: str = "quick_read", inquiry_id: str | None = None):
    question = question.strip()
    if len(question) < 5:
        raise ValueError("Question must be at least 5 characters.")
    if depth not in DEPTHS:
        raise ValueError(f"Unsupported depth: {depth}")
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    if inquiry_id is None:
        existing = sorted(INQUIRY_DIR.glob("INQ-*.json")) if INQUIRY_DIR.exists() else []
        n = max([int(p.stem.split("-")[1]) for p in existing] or [0]) + 1
        inquiry_id = f"INQ-{n:04d}"
    route = classify(question)
    record = {
        "id": inquiry_id,
        "type": "inquiry",
        "question": question,
        "question_type": route.question_type,
        "scope": {"jurisdiction": "", "subject": "", "identifiers": []},
        "requested_depth": depth,
        "status": "classified",
        "routing_rationale": route.rationale,
        "created": now,
        "updated": now,
    }
    INQUIRY_DIR.mkdir(parents=True, exist_ok=True)
    path = INQUIRY_DIR / f"{inquiry_id}.json"
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return path, record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--depth", default="quick_read", choices=sorted(DEPTHS))
    parser.add_argument("--id")
    args = parser.parse_args()
    path, record = create(args.question, args.depth, args.id)
    print(json.dumps({"path": str(path), "inquiry": record}, indent=2))
