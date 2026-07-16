#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
SCENARIO=ROOT/"theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001/scenario/scenario-v1.0.json"
COMPILERS=[
    ROOT/"tools/cre002_compilers/compiler_recursive.py",
    ROOT/"tools/cre002_compilers/compiler_iterative.py",
    ROOT/"tools/cre002_compilers/compiler_pairs.py",
]
VERIFIER=ROOT/"tools/cre002_compilers/verifier.py"

def run_process(command: list[str], cwd: Path) -> None:
    env={"PYTHONHASHSEED":"0","PATH":os.environ.get("PATH","")}
    cp=subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True)
    if cp.returncode:
        raise RuntimeError(f"command failed ({cp.returncode}): {' '.join(command)}\n{cp.stdout}{cp.stderr}")

def isolated_run(root: Path, name: str) -> dict[str,Any]:
    run=root/name; run.mkdir()
    outputs=[]
    for index,compiler in enumerate(COMPILERS,1):
        work=run/f"compiler-{index}"; work.mkdir()
        source=work/"scenario.json"; output=work/"output.json"
        shutil.copyfile(SCENARIO,source)
        run_process([sys.executable,str(compiler),str(source),str(output)],work)
        outputs.append(output)
    verify=run/"verifier"; verify.mkdir()
    frozen=[]
    for index,output in enumerate(outputs,1):
        target=verify/f"candidate-{index}.json"; shutil.copyfile(output,target); frozen.append(target)
    report_path=verify/"report.json"
    command=[sys.executable,str(VERIFIER),"--scenario",str(SCENARIO),"--output",str(report_path)]
    for candidate in frozen: command.extend(["--candidate",str(candidate)])
    run_process(command,verify)
    return json.loads(report_path.read_text(encoding="utf-8"))

def check() -> int:
    for path in [*COMPILERS,VERIFIER]:
        if not path.is_file(): raise FileNotFoundError(path)
    if len({path.read_bytes() for path in COMPILERS}) != len(COMPILERS):
        raise ValueError("compiler source files must be distinct")
    with tempfile.TemporaryDirectory(prefix="cre002-separated-") as directory:
        root=Path(directory); first=isolated_run(root,"run-1"); second=isolated_run(root,"run-2")
    deterministic=first==second
    report=dict(first)
    report["deterministic_rerun"]=deterministic
    report["separate_source_files"]=True
    report["compiler_files"]=[str(path.relative_to(ROOT)) for path in COMPILERS]
    report["verifier_file"]=str(VERIFIER.relative_to(ROOT))
    report["status"]="pass" if deterministic and first.get("status")=="pass" else "fail"
    print(json.dumps(report,indent=2,sort_keys=True))
    return 0 if report["status"]=="pass" else 1

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--check",action="store_true"); p.parse_args(); return check()
if __name__=="__main__": raise SystemExit(main())
