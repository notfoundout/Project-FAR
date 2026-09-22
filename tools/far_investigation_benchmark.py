#!/usr/bin/env python3
"""Fail-closed validator/analyzer entry point for FAR Investigation Benchmark v0.1."""

from __future__ import annotations
import argparse, hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ALLOWED_STATUS = {"prepared","frozen","unblinded","completed","completed_imported_sealed","blocked"}
REQUIRED = {"schema_version","campaign_id","status","target","evaluators","environment","protocol","stages","source_manifest","artifacts","times","final_adjudication","replay","limitations"}
TARGET_REQUIRED = {"repository","commit","tree","theory_or_question","hashes"}
ZERO64 = "0"*64

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def validate(manifest_path):
    m=load(manifest_path)
    errors=[]
    if set(m)!=REQUIRED:
        errors.append(f"top-level fields differ: missing={sorted(REQUIRED-set(m))}, extra={sorted(set(m)-REQUIRED)}")
    if m.get("schema_version")!="1.0": errors.append("schema_version must be 1.0")
    if m.get("status") not in ALLOWED_STATUS: errors.append("invalid status")
    t=m.get("target",{})
    if set(t)!=TARGET_REQUIRED: errors.append("target fields do not match campaign schema")
    for k in ("commit","tree"):
        v=t.get(k,"")
        if len(v)!=40 or any(c not in "0123456789abcdef" for c in v): errors.append(f"target.{k} must be 40 lowercase hex")
    p=m.get("protocol",{})
    if set(p)!={"id","version","path","sha256"}: errors.append("protocol fields do not match campaign schema")
    arts=m.get("artifacts",[])
    if not arts: errors.append("artifacts must be non-empty")
    for i,a in enumerate(arts):
        if set(a)!={"path","sha256","role","verify_current_path"}: errors.append(f"artifact {i} fields invalid"); continue
        d=a.get("sha256","")
        if len(d)!=64 or any(c not in "0123456789abcdef" for c in d): errors.append(f"artifact {i} sha256 invalid")
        if a.get("verify_current_path"):
            fp=ROOT/a["path"]
            if not fp.exists(): errors.append(f"artifact {i} path missing: {a['path']}")
            elif m.get("status")!="prepared" and d!=sha256(fp): errors.append(f"artifact {i} hash mismatch")
    if m.get("status")!="prepared":
        if p.get("sha256") in {"",ZERO64} or "TO_BE_" in p.get("sha256",""): errors.append("non-prepared manifest requires frozen protocol hash")
        for i,a in enumerate(arts):
            if a["sha256"]==ZERO64: errors.append(f"non-prepared artifact {i} retains placeholder hash")
    if errors:
        for e in errors: print("ERROR:",e,file=sys.stderr)
        return 1
    print(f"VALID {m['campaign_id']} status={m['status']}")
    return 0

def analyze(manifest_path):
    m=load(manifest_path)
    if validate(manifest_path): return 1
    if m["status"] not in {"unblinded","completed","completed_imported_sealed"}:
        print("BLOCKED: analysis requires an unblinded/completed frozen campaign.",file=sys.stderr)
        return 2
    metrics=manifest_path.parent/"metrics.csv"
    if not metrics.exists():
        print("BLOCKED: metrics.csv is absent.",file=sys.stderr); return 2
    print("Analysis execution is intentionally unavailable until the frozen metric implementation is added and reviewed.")
    return 2

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    for name in ("validate","analyze"):
        p=sub.add_parser(name); p.add_argument("--manifest",required=True,type=pathlib.Path)
    a=ap.parse_args()
    path=a.manifest if a.manifest.is_absolute() else ROOT/a.manifest
    return validate(path) if a.cmd=="validate" else analyze(path)

if __name__=="__main__": raise SystemExit(main())
