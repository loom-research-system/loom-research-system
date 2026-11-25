"""GitHub Actions adapter for the single canonical research-request ingester.

The event file is transport input only. It is never treated as evidence or
as instructions to the research system.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from scripts.ingest_research_request import ingest


def process(event_path: Path):
    event = json.loads(event_path.read_text(encoding="utf-8"))
    issue = event.get("issue") or {}
    if not issue.get("number"):
        raise ValueError("GitHub event does not contain an issue number.")
    return ingest(
        int(issue["number"]),
        issue.get("title", ""),
        issue.get("body", "") or "",
        issue.get("html_url", ""),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("event", type=Path)
    args = parser.parse_args()
    inquiry_path, plan_path, inquiry, created = process(args.event)
    print(json.dumps({
        "created": created,
        "inquiry": inquiry,
        "inquiry_path": str(inquiry_path),
        "plan_path": str(plan_path),
    }, indent=2))
