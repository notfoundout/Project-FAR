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
app = FastAPI(title="Project FAR Demo", version="0.2.0")


def _package(payload: dict[str, Any]) -> DecisionPackage:
    return DecisionPackage.from_dict(payload)


def _sha(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def _node_map(package: DecisionPackage) -> dict[str, dict[str, Any]]:
    return {
        node.node_id: {
            "id": node.node_id,
            "kind": node.kind,
            "statement": node.statement,
            "attributes": node.attributes,
        }
        for node in package.nodes
    }


def _present(baseline: DecisionPackage, candidate: DecisionPackage) -> dict[str, Any]:
    baseline_result = adjudicate(baseline)
    candidate_result = adjudicate(candidate)
    baseline_report = report_payload(baseline_result)
    candidate_report = report_payload(candidate_result)
    baseline_nodes = _node_map(baseline)
    candidate_nodes = _node_map(candidate)

    baseline_incoming = {
        d.source_id for d in baseline.dependencies if d.target_id == baseline.decision_root
    }
    candidate_incoming = {
        d.source_id for d in candidate.dependencies if d.target_id == candidate.decision_root
    }
    lost_dependencies = sorted(baseline_incoming - candidate_incoming)
    new_dependencies = sorted(candidate_incoming - baseline_incoming)

    changes: list[dict[str, Any]] = []
    for node_id in lost_dependencies:
        node = baseline_nodes.get(node_id, {"statement": node_id})
        changes.append({
            "type": "dependency_removed",
            "severity": "critical" if node_id in baseline.authorization_requirements else "high",
            "title": "Required decision dependency disappeared",
            "description": node["statement"],
            "node_id": node_id,
        })
    for node_id in new_dependencies:
        node = candidate_nodes.get(node_id, {"statement": node_id})
        changes.append({
            "type": "dependency_added",
            "severity": "review",
            "title": "New decision dependency appeared",
            "description": node["statement"],
            "node_id": node_id,
        })

    baseline_rules = {f["rule_id"] for f in baseline_report["findings"]}
    for finding in candidate_report["findings"]:
        if finding["rule_id"] not in baseline_rules:
            changes.append({
                "type": finding["rule_id"],
                "severity": "critical" if finding["severity"] == "error" else "review",
                "title": finding["rule_id"].replace("-", " ").title(),
                "description": finding["message"],
                "node_id": finding.get("node_id"),
            })

    status = candidate_result.status.value
    headline = {
        "unsupported": "The updated agent no longer has sufficient recorded support for this action.",
        "unverifiable": "The available trace is too incomplete to verify the updated decision.",
        "underdetermined": "Multiple materially different conclusions remain possible.",
        "justified": "The recorded evidence supports the updated decision.",
    }[status]

    artifact = {
        "schema": "far-demo-report/0.2",
        "baseline": baseline_report,
        "candidate": candidate_report,
        "comparison": {
            "lost_dependencies": lost_dependencies,
            "new_dependencies": new_dependencies,
            "status_transition": [baseline_result.status.value, candidate_result.status.value],
        },
        "claim_boundary": "FAR evaluates only the supplied decision packages and recorded dependencies. It does not infer hidden reasoning, external truth, safety, or regulatory compliance.",
    }
    artifact["sha256"] = _sha(artifact)

    return {
        "status": status,
        "headline": headline,
        "status_transition": [baseline_result.status.value, candidate_result.status.value],
        "changes": changes,
        "unknowns": list(candidate.unknowns),
        "trace_completeness": candidate.trace_completeness,
        "baseline": {"nodes": list(baseline_nodes.values()), "dependencies": [d.__dict__ for d in baseline.dependencies], "root": baseline.decision_root},
        "candidate": {"nodes": list(candidate_nodes.values()), "dependencies": [d.__dict__ for d in candidate.dependencies], "root": candidate.decision_root},
        "artifact": artifact,
    }


BASELINE = {
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

CANDIDATE = {
    **BASELINE,
    "decision_id": "refund-candidate",
    "nodes": [
        BASELINE["nodes"][0], BASELINE["nodes"][1], BASELINE["nodes"][2],
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
    return _present(_package(BASELINE), _package(CANDIDATE))


@app.get("/api/example/report")
def example_report() -> Response:
    data = _present(_package(BASELINE), _package(CANDIDATE))["artifact"]
    return Response(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=far-verification-report.json"},
    )


@app.post("/api/analyze")
async def analyze(baseline: UploadFile = File(...), candidate: UploadFile = File(...)) -> JSONResponse:
    if not baseline.filename.lower().endswith(".json") or not candidate.filename.lower().endswith(".json"):
        raise HTTPException(400, "Both uploads must be FAR decision-package JSON files.")
    try:
        raw_b = await baseline.read(MAX_BYTES + 1)
        raw_c = await candidate.read(MAX_BYTES + 1)
        if len(raw_b) > MAX_BYTES or len(raw_c) > MAX_BYTES:
            raise ValueError("Each upload must be 1 MB or smaller.")
        b = _package(json.loads(raw_b.decode()))
        c = _package(json.loads(raw_c.decode()))
    except (UnicodeDecodeError, json.JSONDecodeError, PackageValidationError, ValueError) as exc:
        raise HTTPException(400, str(exc)) from exc
    return JSONResponse(_present(b, c))


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return PAGE


PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FAR — Agent Verification</title>
<style>
:root{--bg:#070a10;--panel:#0f1420;--line:#222b3d;--text:#f5f7fb;--muted:#94a3b8;--cyan:#5eead4;--blue:#60a5fa;--red:#fb7185;--amber:#fbbf24;font-family:Inter,ui-sans-serif,system-ui,sans-serif}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 15% -10%,#14213d 0,transparent 35%),var(--bg);color:var(--text)}.shell{max-width:1180px;margin:auto;padding:28px 20px 80px}.nav{display:flex;justify-content:space-between;align-items:center;margin-bottom:72px}.brand{font-weight:900;letter-spacing:.18em}.pill{border:1px solid var(--line);padding:8px 12px;border-radius:999px;color:var(--muted);font-size:12px}.hero{max-width:820px;margin-bottom:48px}.eyebrow{color:var(--cyan);font-weight:800;text-transform:uppercase;letter-spacing:.16em;font-size:12px}.hero h1{font-size:clamp(42px,7vw,82px);line-height:.96;letter-spacing:-.055em;margin:18px 0}.hero p{font-size:20px;line-height:1.6;color:#bac5d6;max-width:720px}.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}button,.button{appearance:none;border:0;border-radius:12px;padding:14px 19px;font-weight:800;cursor:pointer;text-decoration:none}.primary{background:linear-gradient(135deg,var(--cyan),var(--blue));color:#041018}.secondary{background:#121927;color:white;border:1px solid var(--line)}.workspace{display:grid;grid-template-columns:1.1fr .9fr;gap:18px}.card{background:linear-gradient(180deg,rgba(18,25,39,.94),rgba(11,16,26,.94));border:1px solid var(--line);border-radius:20px;padding:22px;box-shadow:0 24px 80px rgba(0,0,0,.22)}.card h2,.card h3{margin-top:0}.timeline{display:grid;grid-template-columns:1fr 1fr;gap:14px}.run{border:1px solid var(--line);border-radius:16px;padding:16px}.runhead{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px}.version{font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.12em}.step{position:relative;padding:12px 12px 12px 34px;margin:8px 0;border-radius:10px;background:#0b111c;color:#cbd5e1;font-size:13px}.step:before{content:'';position:absolute;left:13px;top:16px;width:8px;height:8px;border-radius:50%;background:var(--cyan)}.step.bad{border:1px solid rgba(251,113,133,.5);background:rgba(127,29,29,.15)}.step.bad:before{background:var(--red)}.missing{border:1px dashed var(--red);color:#fecdd3;background:rgba(127,29,29,.1)}.verdict{display:flex;gap:14px;align-items:flex-start}.status{padding:7px 10px;border-radius:999px;background:rgba(251,113,133,.14);color:#fecdd3;font-weight:900;text-transform:uppercase;font-size:11px}.headline{font-size:25px;line-height:1.25;margin:0}.metricgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:20px 0}.metric{background:#0a0f18;border:1px solid var(--line);border-radius:13px;padding:14px}.metric strong{display:block;font-size:20px}.metric span{font-size:11px;color:var(--muted)}.change{border-left:3px solid var(--red);padding:10px 14px;margin:12px 0;background:#0b111c;border-radius:0 10px 10px 0}.change small{color:var(--muted)}.unknown{padding:13px;border:1px solid rgba(251,191,36,.25);background:rgba(120,53,15,.13);border-radius:12px;color:#fde68a}.advanced{margin-top:18px}.uploadbox{display:none;margin-top:16px;padding:16px;border:1px dashed var(--line);border-radius:14px}.uploadbox.open{display:block}.files{display:grid;grid-template-columns:1fr 1fr;gap:10px}.file{padding:13px;background:#0a0f18;border-radius:10px;border:1px solid var(--line);font-size:12px}.error{color:#fecaca}.loading{opacity:.55;pointer-events:none}pre{white-space:pre-wrap;max-height:380px;overflow:auto;background:#05080d;padding:14px;border-radius:12px;font-size:11px;color:#a7f3d0}details summary{cursor:pointer;color:var(--muted)}@media(max-width:850px){.workspace{grid-template-columns:1fr}.timeline{grid-template-columns:1fr}.nav{margin-bottom:42px}.metricgrid{grid-template-columns:1fr}.hero p{font-size:17px}.files{grid-template-columns:1fr}}
</style></head><body><main class="shell">
<nav class="nav"><div class="brand">FAR</div><div class="pill">Evidence-bound agent verification</div></nav>
<section class="hero"><div class="eyebrow">Project FAR verification demo</div><h1>See what changed inside an AI agent update.</h1><p>FAR reconstructs the evidence behind two versions, identifies missing authorization and weakened dependencies, and reports what the record can—and cannot—support.</p><div class="cta"><button class="primary" id="run" onclick="runExample()">Run live verification</button><button class="secondary" onclick="toggleUpload()">Analyze FAR packages</button></div></section>
<section id="upload" class="uploadbox"><div class="files"><label class="file">Baseline package<br><input id="baseline" type="file" accept=".json,application/json"></label><label class="file">Candidate package<br><input id="candidate" type="file" accept=".json,application/json"></label></div><div class="cta"><button class="primary" onclick="runUpload()">Verify packages</button></div><p id="error" class="error"></p></section>
<section class="workspace">
<div class="card"><h2>Execution comparison</h2><div class="timeline"><div class="run"><div class="runhead"><strong>Baseline</strong><span class="version">Approved path</span></div><div class="step">Load refund request</div><div class="step">Apply refund policy</div><div class="step">Supervisor approval recorded</div><div class="step">Issue refund</div></div><div class="run"><div class="runhead"><strong>Candidate</strong><span class="version">Updated agent</span></div><div class="step">Load refund request</div><div class="step">Apply refund policy</div><div class="step missing">Approval dependency missing</div><div class="step bad">Issue refund anyway</div></div></div></div>
<div class="card"><div class="verdict"><span id="status" class="status">Not run</span><div><p id="headline" class="headline">Run the verification to generate an evidence-bound result.</p></div></div><div class="metricgrid"><div class="metric"><strong id="transition">—</strong><span>Status transition</span></div><div class="metric"><strong id="count">—</strong><span>Material changes</span></div><div class="metric"><strong id="complete">—</strong><span>Trace completeness</span></div></div><div id="changes"></div><div id="unknowns"></div><div class="cta"><a id="download" class="button secondary" href="/api/example/report" download>Download FAR report</a></div><details class="advanced"><summary>Inspect deterministic evidence artifact</summary><pre id="raw">Run verification first.</pre></details></div>
</section></main><script>
function toggleUpload(){document.getElementById('upload').classList.toggle('open')}
function render(d){status.textContent=d.status;headline.textContent=d.headline;transition.textContent=d.status_transition.join(' → ');count.textContent=d.changes.length;complete.textContent=Math.round(d.trace_completeness*100)+'%';changes.innerHTML=d.changes.map(x=>`<div class="change"><strong>${x.title}</strong><p>${x.description}</p><small>${x.type} · ${x.severity}</small></div>`).join('')||'<p>No material change established.</p>';unknowns.innerHTML=(d.unknowns||[]).map(x=>`<div class="unknown"><strong>Known unknown</strong><br>${x}</div>`).join('');raw.textContent=JSON.stringify(d.artifact,null,2);document.querySelector('.workspace').scrollIntoView({behavior:'smooth'})}
async function runExample(){const b=document.getElementById('run');b.classList.add('loading');b.textContent='Verifying…';try{const r=await fetch('/api/example');render(await r.json())}finally{b.classList.remove('loading');b.textContent='Run live verification'}}
async function runUpload(){const b=baseline.files[0],c=candidate.files[0];if(!b||!c){error.textContent='Select both FAR decision-package JSON files.';return}const f=new FormData();f.append('baseline',b);f.append('candidate',c);const r=await fetch('/api/analyze',{method:'POST',body:f});const d=await r.json();if(!r.ok){error.textContent=d.detail||'Verification failed.';return}error.textContent='';render(d)}
</script></body></html>'''
