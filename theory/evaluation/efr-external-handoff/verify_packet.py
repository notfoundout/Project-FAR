#!/usr/bin/env python3
"""Standalone, stdlib-only verifier for the Project FAR EFR external handoff."""
from __future__ import annotations
import hashlib, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
EXPECTED_IDS = [f"FAR-CORE-{i:03d}" for i in range(1, 15)]
ALLOWED = {"SURVIVES-ATTACK", "FALSIFIED", "INDETERMINATE"}
FORBIDDEN_TEXT = (
    "PR #453 negative witness", "PR #453 positive witness",
    "expected_verdict", "W1 exact-scope truth verdict",
    "sOr_not_derivable", "sAnd_derivable",
)

def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fail(msg: str) -> None:
    raise ValueError(msg)

def verify_manifest() -> dict:
    p = HERE / "manifest.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    if data.get("status") != "HANDOFF_READY_NOT_EXECUTED":
        fail("manifest status must remain HANDOFF_READY_NOT_EXECUTED")
    for rel, expected in data.get("files", {}).items():
        q = HERE / rel
        if not q.is_file():
            fail(f"missing handoff file: {rel}")
        if sha256(q) != expected:
            fail(f"sha256 mismatch: {rel}")
    return data

def verify_r1() -> dict:
    p = HERE / "r1-statement-only.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    baseline = data.get("scientific_baseline", {})
    if baseline.get("commit") != "195fc079d0a8993e4db3e063e09cf45d0bcd78c2":
        fail("wrong frozen scientific baseline")
    claims = data.get("claims", [])
    ids = [x.get("id") for x in claims]
    if ids != EXPECTED_IDS or len(set(ids)) != 14:
        fail("claim binding must be exactly FAR-CORE-001..014 once each")
    vocab = data.get("formal_vocabulary", {})
    if vocab.get("exact_decoder_signature") != "d:ρ[X]→V^T":
        fail("decoder domain/codomain guard failed")
    by_id = {x["id"]: x for x in claims}
    c4 = by_id["FAR-CORE-004"]
    if "least-informative sufficient representation for every observation contract" not in c4["claim"]:
        fail("FAR-CORE-004 minimality wording lost")
    g4 = data["semantic_guards"]["FAR-CORE-004"]
    if "identity representation is sufficient for every observation contract" not in g4["nonclaim"]:
        fail("FAR-CORE-004 identity-sufficiency nonclaim lost")
    c10 = by_id["FAR-CORE-010"]
    if "L,J,I" not in c10["claim"] or "Γ" not in c10["claim"]:
        fail("FAR-CORE-010 canonical binding lost")
    g10 = data["semantic_guards"]["FAR-CORE-010"]
    dep = g10.get("dependency", "")
    if "Γ alone cannot change T_{L,J,I}" not in dep or "residue" not in dep:
        fail("FAR-CORE-010 dependency guard failed")
    g14 = data["semantic_guards"]["FAR-CORE-014"]
    required = {"bounded_scope", "decoder_chain", "witness_summary", "mll",
                "required_independent_reconstruction", "source"}
    if not required.issubset(g14):
        fail("FAR-CORE-014 bounded definition surface incomplete")
    decoders = g14["decoder_chain"].get("uniform_decoders", [])
    if [(d["name"], d["values"]) for d in decoders] != [
        ("termDecoder",[False,False,False]), ("andDecoder",[False,False,True]),
        ("orDecoder",[False,True,True]), ("nonemptyDecoder",[True,True,True])]:
        fail("FAR-CORE-014 decoder class changed")
    if g14["witness_summary"] != {
        "S_or":{"derivable":False,"terminal":False,"successorTruths":"mixed"},
        "S_and":{"derivable":True,"terminal":False,"successorTruths":"mixed"}}:
        fail("FAR-CORE-014 witness definition surface changed")
    ledger = data.get("evaluator_contract", {}).get("verdict_ledger", [])
    if [r.get("id") for r in ledger] != EXPECTED_IDS:
        fail("verdict ledger ids invalid")
    if any(r.get("verdict") is not None or r.get("reason") is not None for r in ledger):
        fail("verdict ledger must be blank before evaluation")
    text = p.read_text(encoding="utf-8")
    for marker in FORBIDDEN_TEXT:
        if marker in text:
            fail(f"forbidden proof/expected-output leakage marker: {marker}")
    if data.get("status") != "EXTERNAL_HANDOFF_READY_NOT_EXECUTED":
        fail("R1 status may not imply execution")
    return data

def verify_other_surfaces() -> None:
    r2 = json.loads((HERE/"r2-custodian-contract.json").read_text(encoding="utf-8"))
    if r2.get("status") != "HANDOFF_READY_NOT_EXECUTED":
        fail("R2 status may not imply execution")
    banned = json.dumps(r2, ensure_ascii=False).lower()
    for marker in ("held_out_cases\": [", "expected_outputs"):
        if marker in banned:
            fail("R2 contains withheld cases or expected outputs")
    a1 = json.loads((HERE/"a1-intake.schema.json").read_text(encoding="utf-8"))
    props = a1.get("properties", {})
    if "independence_attestation" not in props or "human_judgment" not in props:
        fail("A1 intake lacks independence/judgment fields")
    for name in ("claude-blind-review-protocol.md","claude-post-unblinding-critic-protocol.md"):
        text = (HERE/name).read_text(encoding="utf-8")
        for marker in ("NOT EFR EXECUTION", "NOT I2", "NOT I3"):
            if marker not in text:
                fail(f"{name} lacks {marker} boundary")

def main() -> int:
    verify_manifest()
    verify_r1()
    verify_other_surfaces()
    print("EFR external handoff verification: PASS")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"EFR external handoff verification: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
