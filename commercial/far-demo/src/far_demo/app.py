from __future__ import annotations

import hashlib
import json
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, Response

from far_decision_integrity.adjudicate import adjudicate
from far_decision_integrity.model import DecisionPackage, PackageValidationError
from far_decision_integrity.report import report_payload

MAX_BYTES = 1_000_000
app = FastAPI(title="Project FAR Demo", version="0.3.0")


def _package(payload: dict[str, Any]) -> DecisionPackage:
    return DecisionPackage.from_dict(payload)


def _sha(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _nodes(package: DecisionPackage) -> dict[str, dict[str, Any]]:
    return {
        node.node_id: {
            "id": node.node_id,
            "kind": node.kind,
            "statement": node.statement,
            "attributes": node.attributes,
        }
        for node in package.nodes
    }


def _dependencies(package: DecisionPackage) -> list[dict[str, str]]:
    return [
        {"source_id": item.source_id, "target_id": item.target_id, "relation": item.relation}
        for item in package.dependencies
    ]


def _present(baseline: DecisionPackage, candidate: DecisionPackage) -> dict[str, Any]:
    baseline_adjudication = adjudicate(baseline)
    candidate_adjudication = adjudicate(candidate)
    baseline_report = report_payload(baseline_adjudication)
    candidate_report = report_payload(candidate_adjudication)
    baseline_nodes = _nodes(baseline)
    candidate_nodes = _nodes(candidate)

    baseline_incoming = {
        item.source_id for item in baseline.dependencies if item.target_id == baseline.decision_root
    }
    candidate_incoming = {
        item.source_id for item in candidate.dependencies if item.target_id == candidate.decision_root
    }
    removed = sorted(baseline_incoming - candidate_incoming)
    added = sorted(candidate_incoming - baseline_incoming)

    changes: list[dict[str, Any]] = []
    for node_id in removed:
        required = node_id in baseline.authorization_requirements
        changes.append(
            {
                "type": "authorization_dependency_removed" if required else "decision_dependency_removed",
                "severity": "critical" if required else "high",
                "title": "Required approval was removed" if required else "Decision support was removed",
                "description": baseline_nodes.get(node_id, {"statement": node_id})["statement"],
                "node_id": node_id,
            }
        )
    for node_id in added:
        changes.append(
            {
                "type": "decision_dependency_added",
                "severity": "review",
                "title": "New decision support appeared",
                "description": candidate_nodes.get(node_id, {"statement": node_id})["statement"],
                "node_id": node_id,
            }
        )

    baseline_rule_ids = {finding["rule_id"] for finding in baseline_report["findings"]}
    for finding in candidate_report["findings"]:
        if finding["rule_id"] not in baseline_rule_ids:
            changes.append(
                {
                    "type": finding["rule_id"],
                    "severity": "critical" if finding["severity"] == "error" else "review",
                    "title": "FAR found missing authorization" if finding["rule_id"] == "authorization-dependency-missing" else finding["rule_id"].replace("-", " ").title(),
                    "description": finding["message"],
                    "node_id": finding.get("node_id"),
                }
            )

    status = candidate_adjudication.status.value
    headline = {
        "unsupported": "The new agent issued the refund without recorded supervisor approval.",
        "unverifiable": "There is not enough evidence to verify the new agent's decision.",
        "underdetermined": "The evidence supports more than one possible conclusion.",
        "justified": "The recorded evidence supports the new agent's decision.",
    }[status]

    artifact = {
        "schema": "far-demo-report/0.3",
        "engine": "far-decision-integrity/1.0.0",
        "baseline": baseline_report,
        "candidate": candidate_report,
        "comparison": {
            "removed_decision_dependencies": removed,
            "added_decision_dependencies": added,
            "status_transition": [baseline_adjudication.status.value, candidate_adjudication.status.value],
        },
        "claim_boundary": "FAR evaluates only the supplied packages and recorded dependencies. It does not infer hidden reasoning, external truth, safety, or regulatory compliance.",
    }
    artifact["sha256"] = _sha(artifact)

    return {
        "status": status,
        "headline": headline,
        "plain_summary": "Version A followed the approval rule. Version B performed the same action after the approval link disappeared.",
        "why_it_matters": "An AI update can still finish the task while silently bypassing a safeguard. FAR detects that change from the recorded evidence.",
        "status_transition": [baseline_adjudication.status.value, candidate_adjudication.status.value],
        "changes": changes,
        "unknowns": list(candidate.unknowns),
        "trace_completeness": candidate.trace_completeness,
        "baseline": {"nodes": list(baseline_nodes.values()), "dependencies": _dependencies(baseline), "root": baseline.decision_root},
        "candidate": {"nodes": list(candidate_nodes.values()), "dependencies": _dependencies(candidate), "root": candidate.decision_root},
        "artifact": artifact,
    }


SAMPLE_BASELINE = {
    "schema_version": "far-decision-package/0.1",
    "decision_id": "refund-baseline",
    "decision_type": "customer-refund",
    "policy_version": "refund-policy-v3",
    "decision_root": "refund",
    "proposed_action": {"type": "issue_refund", "amount": 420},
    "nodes": [
        {"node_id": "request", "kind": "evidence", "statement": "Customer requested a $420 refund.", "attributes": {"valid": True}},
        {"node_id": "policy", "kind": "rule", "statement": "Refunds above $250 require supervisor approval.", "attributes": {"valid": True}},
        {"node_id": "approval", "kind": "authorization", "statement": "Supervisor approved the refund.", "attributes": {"valid": True}},
        {"node_id": "refund", "kind": "decision", "statement": "Issue the $420 refund.", "attributes": {"valid": True}},
    ],
    "dependencies": [
        {"source_id": "request", "target_id": "refund", "relation": "supports"},
        {"source_id": "policy", "target_id": "refund", "relation": "constrains"},
        {"source_id": "approval", "target_id": "refund", "relation": "authorizes"},
    ],
    "authorization_requirements": ["approval"],
    "unknowns": [],
    "trace_completeness": 1.0,
    "metadata": {},
}

SAMPLE_CANDIDATE = {
    **SAMPLE_BASELINE,
    "decision_id": "refund-candidate",
    "nodes": [
        SAMPLE_BASELINE["nodes"][0],
        SAMPLE_BASELINE["nodes"][1],
        SAMPLE_BASELINE["nodes"][2],
        {"node_id": "refund", "kind": "decision", "statement": "Issue the $420 refund; policy followed.", "attributes": {"valid": True}},
    ],
    "dependencies": [
        {"source_id": "request", "target_id": "refund", "relation": "supports"},
        {"source_id": "policy", "target_id": "refund", "relation": "constrains"},
    ],
    "unknowns": ["Whether approval occurred outside the captured execution trace."],
    "trace_completeness": 0.82,
}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "far-demo", "engine": "far-decision-integrity"}


@app.get("/api/example")
def example() -> dict[str, Any]:
    return _present(_package(SAMPLE_BASELINE), _package(SAMPLE_CANDIDATE))


@app.get("/api/example/report")
def example_report() -> Response:
    payload = example()["artifact"]
    return Response(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=far-verification-report.json"},
    )


@app.post("/api/analyze")
async def analyze(baseline: UploadFile = File(...), candidate: UploadFile = File(...)) -> JSONResponse:
    if not baseline.filename.lower().endswith(".json") or not candidate.filename.lower().endswith(".json"):
        raise HTTPException(400, "Both uploads must be FAR decision-package JSON files.")
    try:
        baseline_bytes = await baseline.read(MAX_BYTES + 1)
        candidate_bytes = await candidate.read(MAX_BYTES + 1)
        if len(baseline_bytes) > MAX_BYTES or len(candidate_bytes) > MAX_BYTES:
            raise ValueError("Each upload must be 1 MB or smaller.")
        baseline_package = _package(json.loads(baseline_bytes.decode("utf-8")))
        candidate_package = _package(json.loads(candidate_bytes.decode("utf-8")))
    except (UnicodeDecodeError, json.JSONDecodeError, PackageValidationError, ValueError) as exc:
        raise HTTPException(400, str(exc)) from exc
    return JSONResponse(_present(baseline_package, candidate_package))


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return PAGE


PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FAR — See what changed</title>
<style>
:root{--bg:#080b12;--panel:#111722;--line:#263043;--text:#f7f9fc;--muted:#9aa8bc;--good:#5eead4;--bad:#fb7185;--warn:#fbbf24;font-family:Inter,system-ui,sans-serif}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 20% -5%,#172554 0,transparent 34%),var(--bg);color:var(--text)}.shell{max-width:1040px;margin:auto;padding:24px 18px 72px}.nav{display:flex;justify-content:space-between;align-items:center;margin-bottom:54px}.brand{font-weight:900;letter-spacing:.18em}.tag{color:var(--muted);font-size:12px}.hero{text-align:center;max-width:780px;margin:0 auto 42px}.hero h1{font-size:clamp(40px,7vw,72px);line-height:1;letter-spacing:-.05em;margin:0 0 20px}.hero p{font-size:19px;line-height:1.55;color:#c4cede;max-width:690px;margin:0 auto}.primary{margin-top:28px;border:0;border-radius:14px;padding:15px 22px;font-weight:900;background:linear-gradient(135deg,var(--good),#60a5fa);color:#061018;cursor:pointer}.story{display:grid;grid-template-columns:1fr 70px 1fr;gap:16px;align-items:center}.card{background:linear-gradient(180deg,#131a27,#0d121c);border:1px solid var(--line);border-radius:20px;padding:22px}.version{font-size:12px;text-transform:uppercase;letter-spacing:.13em;color:var(--muted)}.card h2{margin:8px 0 18px}.step{display:flex;gap:12px;align-items:center;padding:13px 0;border-bottom:1px solid #1d2635}.step:last-child{border-bottom:0}.dot{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;background:rgba(94,234,212,.14);color:var(--good);font-weight:900}.missing{color:#fecdd3}.missing .dot{background:rgba(251,113,133,.14);color:var(--bad)}.arrow{text-align:center;font-size:30px;color:var(--muted)}.answer{display:none;margin-top:20px}.answer.show{display:block}.result{border:1px solid rgba(251,113,133,.45);background:linear-gradient(180deg,rgba(127,29,29,.18),rgba(17,23,34,.98));border-radius:22px;padding:26px}.label{display:inline-block;padding:7px 10px;border-radius:999px;background:rgba(251,113,133,.14);color:#fecdd3;font-weight:900;font-size:11px;text-transform:uppercase}.result h2{font-size:clamp(28px,4vw,44px);line-height:1.08;margin:16px 0}.explain{font-size:18px;line-height:1.55;color:#d6deea}.why{margin-top:20px;padding:16px;border-radius:14px;background:#0b1018;border:1px solid var(--line)}.why strong{display:block;margin-bottom:6px}.unknown{margin-top:12px;padding:14px;border-radius:12px;background:rgba(120,53,15,.18);border:1px solid rgba(251,191,36,.3);color:#fde68a}.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}.button{border:1px solid var(--line);background:#151d2b;color:white;padding:12px 15px;border-radius:11px;text-decoration:none;font-weight:800;cursor:pointer}.advanced{margin-top:30px}.advanced summary{cursor:pointer;color:var(--muted)}.upload{margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:10px}.file{padding:13px;border:1px dashed var(--line);border-radius:12px;color:var(--muted)}pre{white-space:pre-wrap;max-height:360px;overflow:auto;background:#05070b;padding:14px;border-radius:12px;color:#a7f3d0;font-size:11px}.error{color:#fecaca}.loading{opacity:.55;pointer-events:none}@media(max-width:760px){.story{grid-template-columns:1fr}.arrow{transform:rotate(90deg)}.upload{grid-template-columns:1fr}.nav{margin-bottom:38px}.hero p{font-size:17px}}
</style>
</head>
<body><main class="shell">
<nav class="nav"><div class="brand">FAR</div><div class="tag">AI change verification</div></nav>
<section class="hero"><h1>Did the new AI quietly skip a safeguard?</h1><p>Both versions completed the refund. Only one followed the required approval process.</p><button id="run" class="primary" onclick="runExample()">Show me what FAR found</button></section>
<section class="story">
<div class="card"><div class="version">Version A · Before update</div><h2>Refund completed correctly</h2><div class="step"><span class="dot">1</span>Read the refund request</div><div class="step"><span class="dot">2</span>Check the refund policy</div><div class="step"><span class="dot">3</span>Get supervisor approval</div><div class="step"><span class="dot">4</span>Issue the refund</div></div>
<div class="arrow">→</div>
<div class="card"><div class="version">Version B · After update</div><h2>Refund still completed</h2><div class="step"><span class="dot">1</span>Read the refund request</div><div class="step"><span class="dot">2</span>Check the refund policy</div><div class="step missing"><span class="dot">×</span>Supervisor approval is missing</div><div class="step missing"><span class="dot">!</span>Issue the refund anyway</div></div>
</section>
<section id="answer" class="answer"><div class="result"><span class="label">FAR result: unsupported</span><h2 id="headline">The new agent issued the refund without recorded supervisor approval.</h2><p id="summary" class="explain"></p><div class="why"><strong>Why this matters</strong><span id="why"></span></div><div id="unknowns"></div><div class="actions"><a class="button" href="/api/example/report" download>Download the evidence report</a></div><details class="advanced"><summary>Technical details for reviewers</summary><pre id="raw"></pre></details></div></section>
<details class="advanced"><summary>Analyze your own FAR decision packages</summary><div class="upload"><label class="file">Before update<br><input id="baseline" type="file" accept=".json,application/json"></label><label class="file">After update<br><input id="candidate" type="file" accept=".json,application/json"></label></div><div class="actions"><button class="button" onclick="runUpload()">Analyze files</button></div><p id="error" class="error"></p></details>
</main><script>
function render(d){headline.textContent=d.headline;summary.textContent=d.plain_summary;why.textContent=d.why_it_matters;unknowns.innerHTML=(d.unknowns||[]).map(x=>`<div class="unknown"><strong>What FAR cannot know from this record:</strong><br>${x}</div>`).join('');raw.textContent=JSON.stringify(d.artifact,null,2);answer.classList.add('show');answer.scrollIntoView({behavior:'smooth'})}
async function runExample(){run.classList.add('loading');run.textContent='Checking the evidence…';try{const r=await fetch('/api/example');render(await r.json())}finally{run.classList.remove('loading');run.textContent='Show me what FAR found'}}
async function runUpload(){const b=baseline.files[0],c=candidate.files[0];if(!b||!c){error.textContent='Choose both files.';return}const f=new FormData();f.append('baseline',b);f.append('candidate',c);const r=await fetch('/api/analyze',{method:'POST',body:f});const d=await r.json();if(!r.ok){error.textContent=d.detail||'Analysis failed.';return}error.textContent='';render(d)}
</script></body></html>'''
