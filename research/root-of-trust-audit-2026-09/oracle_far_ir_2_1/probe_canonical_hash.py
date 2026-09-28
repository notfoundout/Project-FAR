"""Empirically identify which canonical-JSON convention reproduces the fixture
freeze hashes. Data-only probe: reads fixture JSON, not implementation code."""
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
FIXTURES = [
    ROOT / "conformance/far-ir-2.1/valid-frontier.json",
    ROOT / "conformance/far-ir-2.1/valid-zero-boundary.json",
]
VARIANTS = {
    "sort_keys,compact,ensure_ascii": dict(sort_keys=True, separators=(",", ":"), ensure_ascii=True),
    "sort_keys,compact,utf8": dict(sort_keys=True, separators=(",", ":"), ensure_ascii=False),
    "sort_keys,default_separators": dict(sort_keys=True),
    "insertion_order,compact": dict(separators=(",", ":")),
    "sort_keys,indent2": dict(sort_keys=True, indent=2),
}
for path in FIXTURES:
    doc = json.loads(path.read_text())
    want = doc["freeze"]["contract_sha256"]
    for name, kw in VARIANTS.items():
        got = hashlib.sha256(json.dumps(doc["contract"], **kw).encode("utf-8")).hexdigest()
        print(f"{path.name:28s} {name:34s} {'MATCH' if got == want else '-'}")
