"""Validate persisted inquiry and plan records before workflow commits."""
from __future__ import annotations
import json
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
TARGETS = (
    ("research/inquiries", "schemas/inquiry.schema.yaml"),
    ("research/plans", "schemas/research_plan.schema.yaml"),
)


def main() -> int:
    errors = []
    checked = 0
    for relative_dir, schema_path in TARGETS:
        directory = ROOT / relative_dir
        schema = yaml.safe_load((ROOT / schema_path).read_text(encoding="utf-8"))
        validator = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())
        if not directory.exists():
            continue
        for record_path in sorted(directory.glob("*.json")):
            checked += 1
            try:
                record = json.loads(record_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{record_path.relative_to(ROOT)}: cannot parse JSON: {exc}")
                continue
            for error in sorted(validator.iter_errors(record), key=lambda e: list(e.absolute_path)):
                location = ".".join(str(part) for part in error.absolute_path) or "<root>"
                errors.append(f"{record_path.relative_to(ROOT)} [{location}]: {error.message}")
    if errors:
        print("Research-record validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validated {checked} inquiry/plan JSON records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
