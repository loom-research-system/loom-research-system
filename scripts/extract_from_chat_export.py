"""Extract locked artifacts from Project Loom chat export."""
from __future__ import annotations

import json
import re
from pathlib import Path

EXPORT = Path(r"C:\Users\rweye\Downloads\chat-export-1791333658698.json")
ROOT = Path(r"C:\Users\rweye\loom-research-system")

SCHEMA_FILES = [
    "actor.schema.yaml",
    "source.schema.yaml",
    "evidence.schema.yaml",
    "research-protocol.schema.yaml",
    "claim.schema.yaml",
    "observation.schema.yaml",
    "diagnostic.schema.yaml",
    "provenance-event.schema.yaml",
]

ADVERSARIAL_FIXTURES = [
    "CLM-FAKE-001.yaml",
    "EVD-FAKE-001.yaml",
    "SRC-FAKE-001.yaml",
    "CLM-FAKE-002.yaml",
    "EVD-FAKE-002.yaml",
]


def get_text(msg: dict) -> str:
    parts: list[str] = []
    if msg.get("content"):
        parts.append(str(msg["content"]))
    for item in msg.get("content_list") or []:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict):
            if item.get("text"):
                parts.append(item["text"])
            elif item.get("content"):
                parts.append(str(item["content"]))
    return "\n".join(parts)


def iter_messages(obj):
    if isinstance(obj, dict):
        if "role" in obj and ("content" in obj or "content_list" in obj):
            yield obj
        for v in obj.values():
            yield from iter_messages(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_messages(item)


def load_messages() -> list[dict]:
    data = json.loads(EXPORT.read_text(encoding="utf-8"))
    return list(iter_messages(data))


def find_doc(
    messages: list[dict],
    *,
    startswith: str | None = None,
    must_contain: list[str] | None = None,
    version_pattern: str | None = None,
    status_locked: bool = False,
) -> str:
    best = ""
    for msg in messages:
        if msg.get("role") != "assistant":
            continue
        t = get_text(msg)
        if startswith and not t.strip().startswith(startswith):
            continue
        if must_contain and not all(s in t for s in must_contain):
            continue
        if version_pattern and not re.search(version_pattern, t):
            continue
        if status_locked and "LOCKED" not in t:
            continue
        if len(t) > len(best):
            best = t
    if not best:
        raise SystemExit(f"No document found: startswith={startswith!r}")
    return best


def trim_doc_to_end(text: str, end_markers: list[str]) -> str:
    """Drop trailing chat commentary after the spec ends."""
    earliest = len(text)
    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1 and idx < earliest:
            earliest = idx
    if earliest < len(text):
        return text[:earliest].rstrip() + "\n"
    return text.rstrip() + "\n"


def extract_pl307(text: str) -> str:
    """PL-307 v1.0 LOCKED message bundles REQ-006 v2.0 in the same assistant reply."""
    split = re.split(r"\n# REQ-006\b", text, maxsplit=1)
    return split[0].rstrip() + "\n"


def extract_pl001(text: str) -> str:
    return text.rstrip() + "\n"


def extract_req006(text: str) -> str:
    return trim_doc_to_end(
        text,
        [
            "\n---\n\n## External review",
            "\n## Review",
            "\nOverall:",
        ],
    )


def extract_schema_block(text: str, filename: str) -> str:
    escaped = re.escape(filename)
    patterns = [
        rf"\*\*File:\*\* `schemas/{escaped}`\s*\n\s*```yaml\s*\n(.*?)```",
        rf"\*\*File:\*\* `{escaped}`\s*\n\s*```yaml\s*\n(.*?)```",
        rf"`schemas/{escaped}`\s*\n\s*```yaml\s*\n(.*?)```",
        rf"##[^\n]*\n\n\*\*File:\*\* `schemas/{escaped}`\s*\n\s*```yaml\s*\n(.*?)```",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip() + "\n"
    raise SystemExit(f"Schema block not found: {filename}")


def extract_validator(text: str) -> str:
    patterns = [
        r"\*\*File:\*\* `loom_validator/validator\.py`\s*\n\s*```python\s*\n(.*?)```",
        r"\*\*File:\*\* `validator\.py`\s*\n\s*```python\s*\n(.*?)```",
        r"##[^\n]*Validator[^\n]*\n.*?```python\s*\n(.*?)```",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip() + "\n"
    # fallback: largest python block after "validator"
    idx = text.lower().find("validator engine")
    if idx == -1:
        idx = text.lower().find("validator.py")
    sub = text[idx:] if idx != -1 else text
    blocks = re.findall(r"```python\s*\n(.*?)```", sub, re.DOTALL)
    if not blocks:
        raise SystemExit("validator.py block not found")
    return max(blocks, key=len).strip() + "\n"


def extract_fixture(text: str, basename: str) -> str:
    """Extract YAML fixture by filename or object id stem."""
    stem = basename.replace(".yaml", "")
    patterns = [
        rf"\*\*File:\*\* `tests/fixtures/adversarial/{re.escape(basename)}`\s*\n\s*```yaml\s*\n(.*?)```",
        rf"\*\*File:\*\* `{re.escape(basename)}`\s*\n\s*```yaml\s*\n(.*?)```",
        rf"###[^\n]*{re.escape(stem)}[^\n]*\n.*?```yaml\s*\n(.*?)```",
        rf"{re.escape(stem)}[^\n]*\n\s*```yaml\s*\n(.*?)```",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip() + "\n"
    raise SystemExit(f"Fixture not found: {basename}")


def discover_adversarial_fixtures(text: str) -> list[str]:
    """First five adversarial fixtures listed in the Phase 3 execution message."""
    names = re.findall(
        r"\*\*File:\*\* `tests/fixtures/adversarial/([^`]+\.yaml)`",
        text,
    )
    if len(names) >= 5:
        return names[:5]
    return ADVERSARIAL_FIXTURES


def main() -> None:
    messages = load_messages()

    pl307_raw = find_doc(
        messages,
        startswith="# PL-307",
        must_contain=["PL-307", "Claims, Epistemic Status"],
        version_pattern=r"\*\*Version:\*\*\s*1\.0",
        status_locked=True,
    )
    pl001_raw = find_doc(
        messages,
        startswith="# PL-001",
        must_contain=["Implementation Roadmap", "Governance Control"],
        version_pattern=r"\*\*Version:\*\*\s*1\.1",
        status_locked=True,
    )
    req006_raw = find_doc(
        messages,
        startswith="# REQ-006 v2.1",
        must_contain=["Fully Audited Artifact"],
    )
    phase2_raw = find_doc(
        messages,
        startswith="# Phase 2 Execution",
    )
    phase3_raw = find_doc(
        messages,
        startswith="# Phase 3 Execution",
    )

    out_specs = ROOT / "specifications"
    out_artifacts = ROOT / "artifacts"
    out_schemas = ROOT / "schemas"
    out_validator = ROOT / "loom_validator"
    out_fixtures = ROOT / "tests" / "fixtures" / "adversarial"

    for d in (out_specs, out_artifacts, out_schemas, out_validator, out_fixtures):
        d.mkdir(parents=True, exist_ok=True)

    (out_specs / "PL-307_v1.0_Claims_Epistemic_Status_Verification_Promotion.md").write_text(
        extract_pl307(pl307_raw),
        encoding="utf-8",
    )
    (out_specs / "PL-001_v1.1_Implementation_Roadmap_Governance_Control.md").write_text(
        extract_pl001(pl001_raw),
        encoding="utf-8",
    )
    (out_artifacts / "REQ-006_v2.1_Flint_Water_Crisis_Fully_Audited.md").write_text(
        extract_req006(req006_raw),
        encoding="utf-8",
    )

    for schema in SCHEMA_FILES:
        (out_schemas / schema).write_text(
            extract_schema_block(phase2_raw, schema),
            encoding="utf-8",
        )

    (out_validator / "validator.py").write_text(
        extract_validator(phase3_raw),
        encoding="utf-8",
    )

    fixture_names = discover_adversarial_fixtures(phase3_raw)
    if not fixture_names:
        fixture_names = ADVERSARIAL_FIXTURES
    print("Fixtures to extract:", fixture_names)
    for name in fixture_names:
        (out_fixtures / name).write_text(
            extract_fixture(phase3_raw, name),
            encoding="utf-8",
        )

    print("Extraction complete.")
    print("PL-307 bytes:", (out_specs / "PL-307_v1.0_Claims_Epistemic_Status_Verification_Promotion.md").stat().st_size)
    print("PL-001 bytes:", (out_specs / "PL-001_v1.1_Implementation_Roadmap_Governance_Control.md").stat().st_size)
    print("REQ-006 bytes:", (out_artifacts / "REQ-006_v2.1_Flint_Water_Crisis_Fully_Audited.md").stat().st_size)
    print("Schemas:", len(list(out_schemas.glob("*.yaml"))))
    print("Fixtures:", len(list(out_fixtures.glob("*.yaml"))))


if __name__ == "__main__":
    main()
