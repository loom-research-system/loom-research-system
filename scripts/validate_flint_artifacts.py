#!/usr/bin/env python3
"""Validate the Flint machine-readable records and emit a truthful trust manifest.

The manifest hashes repository artifacts as they exist in the checked-out commit.
It does not claim that source-document hashes are genuine unless those source
objects have been retrieved and their hashes independently recomputed.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "flint"
SCHEMA_DIR = ROOT / "schemas"
PUBLIC_DIR = ROOT / "public" / "cases"
MANIFEST_PATH = PUBLIC_DIR / "flint-artifacts.json"

# Prevent PyYAML from coercing ISO dates to datetime.date; JSON Schema expects
# a string and then validates the declared format.
class StringDateSafeLoader(yaml.SafeLoader):
    pass

StringDateSafeLoader.yaml_implicit_resolvers = {
    key: [(tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

TYPE_TO_SCHEMA = {
    "claim": "claim.schema.yaml",
    "diagnostic": "diagnostic.schema.yaml",
    "evidence": "evidence.schema.yaml",
    "source": "source.schema.yaml",
    "verification_event": "provenance-event.schema.yaml",
    "assessment_event": "provenance-event.schema.yaml",
    "promotion_event": "provenance-event.schema.yaml",
    "demotion_event": "provenance-event.schema.yaml",
    "contradiction_search_event": "provenance-event.schema.yaml",
    "correction_event": "provenance-event.schema.yaml",
    "retraction_event": "provenance-event.schema.yaml",
    "extraction_event": "provenance-event.schema.yaml",
    "cascade_trigger_event": "provenance-event.schema.yaml",
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    errors: list[str] = []
    objects: dict[str, dict] = {}
    records: list[dict] = []
    schema_cache: dict[str, dict] = {}

    for path in sorted(ARTIFACT_DIR.glob("*.yaml")):
        raw = path.read_bytes()
        try:
            obj = yaml.load(raw.decode("utf-8-sig"), Loader=StringDateSafeLoader)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: YAML parse failed: {exc}")
            continue
        if not isinstance(obj, dict):
            errors.append(f"{path.relative_to(ROOT)}: expected a YAML object")
            continue
        object_id = obj.get("id") or obj.get("event_id")
        if not isinstance(object_id, str) or not object_id:
            errors.append(f"{path.relative_to(ROOT)}: missing id/event_id")
            continue
        if object_id in objects:
            errors.append(f"{path.relative_to(ROOT)}: duplicate object ID {object_id}")
        objects[object_id] = obj

        object_type = obj.get("type")
        schema_name = TYPE_TO_SCHEMA.get(object_type)
        schema_ok = False
        if not schema_name:
            errors.append(f"{path.relative_to(ROOT)}: no schema mapping for type {object_type!r}")
        else:
            try:
                if schema_name not in schema_cache:
                    schema_path = SCHEMA_DIR / schema_name
                    schema_cache[schema_name] = yaml.safe_load(schema_path.read_text(encoding="utf-8-sig"))
                jsonschema.Draft7Validator.check_schema(schema_cache[schema_name])
                validator = jsonschema.Draft7Validator(
                    schema_cache[schema_name],
                    format_checker=jsonschema.FormatChecker(),
                )
                problems = sorted(validator.iter_errors(obj), key=lambda e: list(map(str, e.path)))
                if problems:
                    for problem in problems:
                        where = ".".join(str(part) for part in problem.path) or "(object)"
                        errors.append(f"{object_id} [{schema_name}] {where}: {problem.message}")
                else:
                    schema_ok = True
            except Exception as exc:
                errors.append(f"{object_id}: schema validation could not run: {exc}")

        doc_hash = obj.get("document_hash")
        if object_type in ("source", "evidence"):
            if doc_hash is not None and (
                not isinstance(doc_hash, str)
                or not re.fullmatch(r"sha256:[a-f0-9]{64}", doc_hash)
            ):
                errors.append(f"{object_id}: document_hash is malformed")
            elif isinstance(doc_hash, str) and doc_hash.startswith("sha256:" + "0" * 32):
                errors.append(f"{object_id}: document_hash looks like a placeholder; retrieve and hash the actual source object")
            elif (
                object_type == "source"
                and obj.get("retrieved") is True
                and obj.get("primary_secondary") == "primary"
                and obj.get("source_format") == "pdf"
                and not doc_hash
            ):
                errors.append(f"{object_id}: retrieved primary PDF requires a document_hash")

        records.append({
            "id": object_id,
            "type": object_type or "unknown",
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256(path),
            "schema_valid": schema_ok,
            "source_document_hash_state": (
                "placeholder_or_suspect" if isinstance(doc_hash, str) and doc_hash.startswith("sha256:" + "0" * 32)
                else "recorded_not_independently_recomputed" if doc_hash else "not_applicable"
            ),
        })

    # Verify cross-object links for the Flint set.
    for object_id, obj in objects.items():
        if obj.get("type") == "evidence":
            source_id = obj.get("source_id")
            if source_id not in objects or objects[source_id].get("type") != "source":
                errors.append(f"{object_id}: source_id {source_id!r} does not resolve to a source object")
            else:
                source_hash = objects[source_id].get("document_hash")
                evidence_hash = obj.get("document_hash")
                if source_hash and evidence_hash != source_hash:
                    errors.append(f"{object_id}: document_hash must match source {source_id}")
                elif not source_hash and evidence_hash is not None:
                    errors.append(f"{object_id}: document_hash must be null when source {source_id} has no captured-byte hash")
        elif obj.get("type") == "claim":
            for evidence_id in obj.get("related_evidence", []) + obj.get("contradictory_evidence", []):
                if evidence_id not in objects or objects[evidence_id].get("type") != "evidence":
                    errors.append(f"{object_id}: evidence reference {evidence_id!r} does not resolve to an evidence object")
        elif obj.get("type") in ("assessment_event", "verification_event", "promotion_event"):
            target_id = obj.get("target_object_id")
            if target_id and target_id not in objects:
                errors.append(f"{object_id or obj.get('event_id')}: target_object_id {target_id!r} does not resolve within the Flint artifact set")

    # Hash additional human-readable research artifacts, too.
    extra_paths = [
        ROOT / "artifacts" / "flint" / "PUBLICATION_BUNDLE.md",
        ROOT / "artifacts" / "flint" / "PUBLICATION_BUNDLE_QUARTZ.md",
        ROOT / "content" / "flint-water-crisis.md",
    ]
    extra_records = []
    for path in extra_paths:
        if path.exists():
            extra_records.append({
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "kind": "repository_artifact",
            })

    status = "PASS" if not errors else "FAIL"
    report = {
        "schema_version": "1.0",
        "case": "Flint Water Crisis",
        "case_id": "REQ-006",
        "commit": __import__("os").environ.get("GITHUB_SHA", "local-uncommitted"),
        "generated_at_utc": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "validation_status": status,
        "validator": "scripts/validate_flint_artifacts.py",
        "checks": [
            "YAML parsing",
            "JSON Schema validation for mapped Flint object types",
            "unique object IDs",
            "evidence-to-source references",
            "claim-to-evidence references",
            "provenance-event target references",
            "placeholder/suspect source-document hash detection",
        ],
        "object_count": len(records),
        "repository_artifact_count": len(extra_records),
        "errors": errors,
        "objects": records,
        "repository_artifacts": extra_records,
        "interpretation": (
            "PASS means these repository records passed the checks listed above. It does not establish factual truth, "
            "source authenticity, independent review, or correctness of the research conclusions."
        ),
    }
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Flint artifact validation: {status}")
    print(f"Machine-readable objects hashed: {len(records)}")
    print(f"Repository research artifacts hashed: {len(extra_records)}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Manifest: {MANIFEST_PATH.relative_to(ROOT)}")
    return 0 if not errors else 1

if __name__ == "__main__":
    sys.exit(main())
