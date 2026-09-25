"""Probe which canonical-JSON serialization reproduces the fixture freeze hashes.

The far-ir/2.0 spec (section 5) says "SHA-256 of canonical JSON for the contract
object only" but does not define "canonical JSON". This probe tests candidate
serializations against the declared fixture hashes (fixture data only).
"""
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
FIXTURES = sorted((ROOT / "conformance" / "far-ir-2.0").glob("*.json"))

VARIANTS = {
    "sorted_compact_ascii": dict(sort_keys=True, separators=(",", ":"), ensure_ascii=True),
    "sorted_compact_utf8": dict(sort_keys=True, separators=(",", ":"), ensure_ascii=False),
    "sorted_default_sep": dict(sort_keys=True),
    "unsorted_compact": dict(separators=(",", ":")),
}

for path in FIXTURES:
    if path.name == "manifest.json":
        continue
    doc = json.loads(path.read_text(encoding="utf-8"))
    want = doc["freeze"]["contract_sha256"]
    hits = [
        name
        for name, kw in VARIANTS.items()
        if hashlib.sha256(json.dumps(doc["contract"], **kw).encode("utf-8")).hexdigest() == want
    ]
    print(f"{path.name}: matching variants = {hits}")
