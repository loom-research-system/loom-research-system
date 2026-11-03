"""Build the read-only public evidence index used by Ask Loom.

Only accepted/canonical claims are published. Candidate and under-review material
stays in the research repository. The browser can retrieve this index, but it
cannot create or promote claims.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
OUT = ROOT / "public" / "ask-loom" / "data" / "index.json"


def load_objects():
    objects = {}
    if not ARTIFACTS.exists():
        return objects
    for path in ARTIFACTS.rglob("*.yaml"):
        try:
            import yaml
            obj = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        if isinstance(obj, dict) and obj.get("id"):
            objects[obj["id"]] = obj
    return objects


def main():
    objects = load_objects()
    claims = []
    sources = {}
    evidence = {}
    for obj in objects.values():
        if obj.get("type") == "source":
            sources[obj["id"]] = {
                "id": obj["id"],
                "title": obj.get("title", obj["id"]),
                "publisher": obj.get("publisher", ""),
                "date": obj.get("date", ""),
                "primary_secondary": obj.get("primary_secondary", ""),
            }
        elif obj.get("type") == "evidence":
            evidence[obj["id"]] = obj

    for obj in objects.values():
        if obj.get("type") != "claim" or obj.get("promotion_stage") not in {"accepted", "canonical"}:
            continue
        if obj.get("verification_level") == "none":
            continue
        refs = []
        for evd_id in obj.get("related_evidence", []):
            evd = evidence.get(evd_id)
            if not evd:
                continue
            src = sources.get(evd.get("source_id"))
            if src:
                refs.append({"evidence_id": evd_id, "source": src})
        claims.append({
            "id": obj["id"],
            "statement": obj.get("statement", ""),
            "epistemic_status": obj.get("epistemic_status"),
            "verification_level": obj.get("verification_level"),
            "promotion_stage": obj.get("promotion_stage"),
            "current_as_of": obj.get("current_as_of"),
            "contradiction_status": obj.get("contradiction_status", "none"),
            "evidence": refs,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"version": "0.1", "claims": claims}, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Built public inquiry index: {len(claims)} publishable claims")


if __name__ == "__main__":
    main()
