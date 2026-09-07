#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_BASELINE = ("195fc079d0a8993e4db3e063e09cf45d0bcd78c2", "a01517ed65f45e62b3d47ffba9dc955fff2bae9b")
EXPECTED_DECODER = "d:ρ[X]→V^T"
EXPECTED_CLAIMS = [
("FAR-CORE-001","proved","any Set-based exact contract","exact sufficiency iff behavior factors through the representation"),
("FAR-CORE-002","proved","any Set-based exact contract; cardinal minimum when finite","the observational quotient is the unique least-informative exact representation up to isomorphism"),
("FAR-CORE-003","proved","declared action/test closure","context closure makes observational equivalence action-compatible"),
("FAR-CORE-004","proved","nontrivial domain with observation contract allowed to vary","no single representation is simultaneously a least-informative sufficient representation for every observation contract; universal sufficiency alone is not denied"),
("FAR-CORE-005","proved","nested admitted transformation classes","invariants are antitone in the admitted re-representation class"),
("FAR-CORE-006","proved","injective transport with decoder","unconstrained encoding establishes host capacity, not native common structure"),
("FAR-CORE-007","proved","faithful reification/tagging regime","primitive vocabulary count is not representation invariant"),
("FAR-CORE-008","proved","finite operator family with tagged tuples","finite operator count is not representation invariant"),
("FAR-CORE-009","proved","proper finite subset of an open domain","finite panels do not establish open-domain universality"),
("FAR-CORE-010","proved","fixed language, interpretation profiles/models, and target class; frame additionally indexes the frame-subtracted residue","exact common theory is relative to L,J,I; the substantive residue is additionally relative to Γ"),
("FAR-CORE-011","proved","any exact contract","omitting a consequence-affecting parameter refutes sufficiency"),
("FAR-CORE-012","proved","contracts distinguishing determinate absence from Unknown","sufficient representations must preserve that distinction"),
("FAR-CORE-013","proved","canonical FARA definition of Ω","Ω is a semantically eliminable derived materialized view"),
("FAR-CORE-014","supported_derived","PR #453 stated representation and decoder classes","Search-State Sufficiency is a bounded factorization instance, not a universal architecture"),
]
EXPECTED_TESTS = {"EFR-R1","EFR-R2","EFR-H1","EFR-A1","EFR-HD1","EFR-U1","EFR-C1","EFR-N1"}

def fail(msg):
    print(f"INVALID PACKET: {msg}")
    raise SystemExit(1)

def sha256(path):
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def main():
    manifest_path=ROOT/"MANIFEST.json"
    packet_path=ROOT/"packet.json"
    if not manifest_path.is_file() or not packet_path.is_file(): fail("missing MANIFEST.json or packet.json")
    try:
        manifest=json.loads(manifest_path.read_text(encoding="utf-8")); packet=json.loads(packet_path.read_text(encoding="utf-8"))
    except Exception as e: fail(f"invalid JSON: {e}")
    files=manifest.get("files")
    if not isinstance(files, dict) or not files: fail("manifest files map missing")
    for rel, expected in files.items():
        p=ROOT/rel
        if not p.is_file(): fail(f"manifest member missing: {rel}")
        if sha256(p)!=expected: fail(f"hash mismatch: {rel}")
    base=packet.get("scientific_baseline",{})
    if (base.get("commit"),base.get("tree")) != EXPECTED_BASELINE: fail("scientific baseline mismatch")
    status=packet.get("execution_status",{})
    if status != {"efr_executed":False,"i3_established":False,"novelty_established":False,"priority_established":False,"tests_executed":0}: fail("execution/nonclaim boundary changed")
    if packet.get("common_definitions",{}).get("exact_decoder_domain") != EXPECTED_DECODER: fail("decoder domain is not exactly d:ρ[X]→V^T")
    got=[(c.get("id"),c.get("status"),c.get("scope"),c.get("claim")) for c in packet.get("claims",[])]
    if got != EXPECTED_CLAIMS: fail("FAR-CORE 14/14 id/status/scope/claim binding mismatch")
    dep=packet.get("far_core_010_dependency",{})
    if dep.get("exact_common_theory")!="T_{L,J,I}" or dep.get("depends_on") != ["L","J","I"] or dep.get("frame")!="Γ" or dep.get("frame_subtracted_residue")!="T_{L,J,I}\\Cn_L(Γ)": fail("FAR-CORE-010 dependency structure malformed")
    rule=dep.get("rule","")
    if "Changing Γ alone" not in rule or "does not change exact T_{L,J,I}" not in rule or "frame-subtracted residue" not in rule: fail("FAR-CORE-010 Γ rule missing or contradictory")
    sss=packet.get("far_core_014_bounded_definitions",{})
    authority=sss.get("authority",{})
    if authority.get("path") != "research/independent-dialogue-theory/PROOFS.md" or authority.get("baseline_git_blob_sha") != "8bb4cde696fbd778a0b6eed42a102d34d71f93e1": fail("FAR-CORE-014 authoritative source lock mismatch")
    if "not authority" not in authority.get("note",""): fail("PR #453 non-authority guard missing")
    rep=sss.get("representation_class",{}); dec=sss.get("decoder_class",{}); wit=sss.get("witnesses",{})
    if rep.get("name")!="R_bin^Seq" or "individual MLL sequent" not in rep.get("state_type","") or "S→_π P iff" not in rep.get("transition",""): fail("FAR-CORE-014 representation class incomplete")
    if dec.get("name")!="D_succ" or set(dec.get("members",{})) != {"TERM","AND","OR","NONEMPTY"} or list(dec.get("members",{}).values()) != [[0,0,0],[0,0,1],[0,1,1],[1,1,1]]: fail("FAR-CORE-014 decoder class incomplete")
    if set(wit)!={"S_or","S_or_fact","S_and","S_and_fact"}: fail("FAR-CORE-014 witness surface incomplete")
    if sss.get("bounded_result")!="No pair in R_bin^Seq×D_succ computes MLL provability.": fail("FAR-CORE-014 bounded result missing")
    if "richer state types" not in sss.get("scope_guard","") or "hyperedges" not in sss.get("scope_guard","") or "frontier multisets" not in sss.get("scope_guard",""): fail("FAR-CORE-014 scope guard incomplete")
    tests=packet.get("registered_efr_tests",[])
    if {x.get("id") for x in tests} != EXPECTED_TESTS or any(x.get("state")!="PREREGISTERED_NOT_EXECUTED" for x in tests): fail("registered EFR state changed")
    if "before viewing or releasing any withheld material" not in packet.get("sealed_output_rule",""): fail("pre-unblinding seal rule missing")
    digest=sha256(packet_path)
    print(f"VALID PACKET {packet.get('packet_id')} sha256={digest}")

if __name__ == "__main__": main()
