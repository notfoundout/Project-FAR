#!/usr/bin/env python3
"""Mutation self-test of the oracle's mini JSON Schema evaluator (not of any implementation).
For a valid fixture: deleting any required property, or adding an undeclared property to any
closed object, must yield SCHEMA_CONSTRAINT_VIOLATION."""
import copy
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import oracle  # noqa: E402

BASES = ["valid-factorization.json", "valid-collision.json", "valid-quotient.json"]


def objects(node, path=()):
    if isinstance(node, dict):
        yield path, node
        for k, v in node.items():
            yield from objects(v, path + (k,))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from objects(v, path + (i,))


def at(doc, path):
    for p in path:
        doc = doc[p]
    return doc


def main():
    bad = checked = 0
    for name in BASES:
        base = json.loads((oracle.ROOT / "conformance/far-ir-2.0" / name).read_text("utf-8"))
        assert oracle.diagnose_document(base) == [], name
        for path, obj in list(objects(base)):
            open_obj = path and path[-1] in ("value", "extensions", "legacy_document")
            if open_obj:
                continue
            for key in list(obj):
                optional = key in ("notes", "extensions", "legacy_document", "approximation")
                if optional:
                    continue
                m = copy.deepcopy(base)
                del at(m, path)[key]
                checked += 1
                if "SCHEMA_CONSTRAINT_VIOLATION" not in oracle.diagnose_document(m):
                    bad += 1
                    print("delete not rejected:", name, path, key)
            m = copy.deepcopy(base)
            at(m, path)["zz_undeclared"] = 1
            checked += 1
            if "SCHEMA_CONSTRAINT_VIOLATION" not in oracle.diagnose_document(m):
                bad += 1
                print("extra key not rejected:", name, path)
    print(f"schema mutations checked={checked} not_rejected={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
