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
app = FastAPI(title="Project FAR Demo", version="0.6.0")


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
                    "title": "FAR found missing authorization"
                    if finding["rule_id"] == "authorization-dependency-missing"
                    else finding["rule_id"].replace("-", " ").title(),
                    "description": finding["message"],
                    "node_id": finding.get("node_id"),
                }
            )

    status = candidate_adjudication.status.value
    headline = {
        "unsupported": "The updated agent refunded $420 without recorded supervisor approval.",
        "unverifiable": "There is not enough evidence to verify the updated agent's decision.",
        "underdetermined": "The evidence supports more than one possible conclusion.",
        "justified": "The recorded evidence supports the updated agent's decision.",
    }[status]

    artifact = {
        "schema": "far-demo-report/0.6",
        "engine": "far-decision-integrity/1.0.0",
        "baseline": baseline_report,
        "candidate": candidate_report,
        "comparison": {
            "removed_decision_dependencies": removed,
            "added_decision_dependencies": added,
            "status_transition": [
                baseline_adjudication.status.value,
                candidate_adjudication.status.value,
            ],
        },
        "claim_boundary": "FAR evaluates only the supplied packages and recorded dependencies. It does not infer hidden reasoning, external truth, safety, or regulatory compliance.",
    }
    artifact["sha256"] = _sha(artifact)

    return {
        "status": status,
        "headline": headline,
        "plain_summary": "The company updated its refund AI. The old version asked a supervisor before refunds over $250. The new version still issued the $420 refund, but its recorded decision path no longer contains the approval dependency.",
        "why_it_matters": "A normal performance test would say both systems succeeded because both completed the refund. FAR checks whether the updated system preserved the controls that made the original decision acceptable.",
        "status_transition": [
            baseline_adjudication.status.value,
            candidate_adjudication.status.value,
        ],
        "changes": changes,
        "unknowns": list(candidate.unknowns),
        "trace_completeness": candidate.trace_completeness,
        "baseline": {
            "nodes": list(baseline_nodes.values()),
            "dependencies": _dependencies(baseline),
            "root": baseline.decision_root,
        },
        "candidate": {
            "nodes": list(candidate_nodes.values()),
            "dependencies": _dependencies(candidate),
            "root": candidate.decision_root,
        },
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
async def analyze(
    baseline: UploadFile = File(...), candidate: UploadFile = File(...)
) -> JSONResponse:
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
<title>FAR — Decision integrity for AI systems</title>
<style>
:root{--bg:#f5f4ef;--ink:#11120f;--muted:#6d7068;--line:rgba(17,18,15,.13);--panel:rgba(255,255,255,.7);--panel2:#151713;--lime:#d9ff6a;--violet:#9b8cff;--red:#df5b4b;--green:#17805c;--shadow:0 30px 90px rgba(17,18,15,.08);font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 82% 8%,rgba(155,140,255,.18),transparent 30%),radial-gradient(circle at 12% 34%,rgba(217,255,106,.2),transparent 28%),var(--bg);color:var(--ink)}button,input{font:inherit}a{color:inherit}.shell{max-width:1380px;margin:auto;padding:0 28px}.nav{height:76px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20;background:rgba(245,244,239,.82);backdrop-filter:blur(18px)}.brand{display:flex;align-items:center;gap:12px;font-weight:750;letter-spacing:-.03em}.mark{width:28px;height:28px;border-radius:9px;background:conic-gradient(from 210deg,var(--lime),var(--violet),#111,var(--lime));box-shadow:inset 0 0 0 1px rgba(255,255,255,.5)}.navnote{font-size:13px;color:var(--muted)}.hero{min-height:680px;padding:92px 0 76px;display:grid;grid-template-columns:minmax(0,1.25fr) minmax(330px,.75fr);gap:70px;align-items:end}.eyebrow{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:28px}.hero h1{font-size:clamp(58px,7.7vw,112px);line-height:.9;letter-spacing:-.075em;font-weight:570;margin:0;max-width:980px}.hero p{font-size:clamp(20px,2vw,28px);line-height:1.38;letter-spacing:-.025em;color:#35372f;max-width:760px;margin:34px 0 0}.heroaside{align-self:stretch;display:flex;flex-direction:column;justify-content:flex-end}.signal{border:1px solid var(--line);background:var(--panel);backdrop-filter:blur(18px);border-radius:26px;padding:26px;box-shadow:var(--shadow)}.signalhead{display:flex;justify-content:space-between;font-size:13px;color:var(--muted);margin-bottom:38px}.signalvalue{font-size:58px;line-height:1;letter-spacing:-.06em}.signallabel{font-size:15px;line-height:1.45;color:var(--muted);margin-top:12px}.section{padding:92px 0;border-top:1px solid var(--line)}.sectionhead{display:grid;grid-template-columns:180px 1fr;gap:50px;margin-bottom:54px}.sectionlabel{font-size:13px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}.sectiontitle{font-size:clamp(38px,4.5vw,68px);line-height:1;letter-spacing:-.055em;font-weight:560;margin:0;max-width:980px}.lede{font-size:20px;line-height:1.55;color:#44473f;max-width:820px;margin:24px 0 0}.scenario{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.scenario article{min-height:230px;background:rgba(255,255,255,.62);border:1px solid var(--line);border-radius:22px;padding:24px;box-shadow:0 16px 48px rgba(17,18,15,.04)}.scenario .n{font-size:12px;color:var(--muted);margin-bottom:62px}.scenario h3{font-size:23px;line-height:1.12;letter-spacing:-.035em;margin:0 0 12px}.scenario p{font-size:15px;line-height:1.52;color:var(--muted);margin:0}.policy{margin-top:22px;background:var(--panel2);color:white;border-radius:26px;padding:34px 38px;display:grid;grid-template-columns:170px 1fr;gap:40px;align-items:start}.policy span{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:#aeb2a8}.policy p{font-size:clamp(27px,3vw,46px);line-height:1.08;letter-spacing:-.04em;margin:0}.comparewrap{background:#11130f;color:white;border-radius:30px;padding:22px;box-shadow:0 36px 100px rgba(17,18,15,.15)}.comparetop{display:flex;justify-content:space-between;align-items:center;padding:8px 8px 22px}.comparetop span{font-size:13px;color:#aeb2a8}.compare{display:grid;grid-template-columns:1fr 1fr;gap:14px}.run{background:#1a1d18;border:1px solid rgba(255,255,255,.08);border-radius:22px;padding:26px}.runhead{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;margin-bottom:34px}.runname{font-size:28px;letter-spacing:-.04em}.status{font-size:12px;border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:8px 10px}.ok{color:#8ef0bd}.bad{color:#ff9b8e}.steps{list-style:none;padding:0;margin:0}.steps li{display:grid;grid-template-columns:34px 1fr auto;gap:12px;padding:17px 0;border-top:1px solid rgba(255,255,255,.09);align-items:center;font-size:16px}.steps li:last-child{border-bottom:1px solid rgba(255,255,255,.09)}.idx{color:#8d9387}.chip{font-size:11px;border-radius:999px;padding:6px 8px;background:rgba(255,255,255,.07);color:#adb3a7}.failed{color:#ffab9f}.failed .chip{background:rgba(223,91,75,.16);color:#ffb4a9}.delta{margin-top:16px;padding:20px;border-radius:18px;background:linear-gradient(135deg,rgba(155,140,255,.16),rgba(217,255,106,.1));display:grid;grid-template-columns:1fr auto;gap:24px;align-items:center}.delta strong{font-size:22px;letter-spacing:-.03em}.delta span{font-size:13px;color:#b8beb2}.primary{border:0;background:var(--lime);color:#111;border-radius:999px;padding:15px 22px;font-weight:720;cursor:pointer;transition:.2s transform,.2s box-shadow}.primary:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(217,255,106,.22)}.answer{display:none}.answer.show{display:block;animation:rise .5s ease}.resultcard{background:rgba(255,255,255,.74);border:1px solid var(--line);border-radius:30px;padding:38px;box-shadow:var(--shadow)}.resultgrid{display:grid;grid-template-columns:190px 1fr;gap:46px}.verdict{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--red)}.result h2{font-size:clamp(42px,5vw,76px);line-height:.98;letter-spacing:-.062em;font-weight:560;margin:0 0 28px;max-width:960px}.result p{font-size:20px;line-height:1.55;max-width:850px;color:#3f423b}.insights{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:38px}.insight{border:1px solid var(--line);border-radius:18px;padding:20px;background:rgba(245,244,239,.75)}.insight b{display:block;font-size:28px;letter-spacing:-.04em;margin-bottom:8px}.insight span{font-size:13px;line-height:1.4;color:var(--muted)}.unknown{margin-top:24px;padding:19px 0;border-top:1px solid var(--line);font-size:14px;color:var(--muted);max-width:900px}.actions{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-top:28px}.secondary{border-bottom:1px solid var(--ink);padding-bottom:3px;text-decoration:none;font-size:14px}.advanced{margin-top:34px}.advanced summary{cursor:pointer;font-size:14px;color:var(--muted)}pre{white-space:pre-wrap;max-height:420px;overflow:auto;background:#10120f;color:#e9ece5;border-radius:18px;padding:20px;font-size:12px;line-height:1.5}.uploadgrid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}.file{background:white;border:1px solid var(--line);border-radius:18px;padding:22px}.file input{display:block;margin-top:14px;max-width:100%}.error{color:var(--red)}.footer{padding:36px 0 58px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:24px;font-size:13px;color:var(--muted)}@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}@media(max-width:980px){.hero{grid-template-columns:1fr;min-height:auto}.heroaside{max-width:500px}.scenario{grid-template-columns:1fr 1fr}.sectionhead,.resultgrid,.policy{grid-template-columns:1fr}.compare{grid-template-columns:1fr}.insights{grid-template-columns:1fr}}@media(max-width:640px){.shell{padding:0 16px}.nav{height:64px}.navnote{display:none}.hero{padding:64px 0 58px}.hero h1{font-size:52px}.section{padding:64px 0}.scenario,.uploadgrid{grid-template-columns:1fr}.scenario article{min-height:190px}.scenario .n{margin-bottom:38px}.comparewrap{padding:12px;border-radius:24px}.run{padding:20px}.steps li{grid-template-columns:28px 1fr}.chip{display:none}.resultcard{padding:24px}.footer{flex-direction:column}}
</style>
</head>
<body><main class="shell">
<nav class="nav"><div class="brand"><span class="mark"></span>FAR</div><div class="navnote">Decision integrity for AI systems</div></nav>
<header class="hero"><div><div class="eyebrow">Interactive verification case</div><h1>Did the AI preserve the rules—or only the result?</h1><p>Two versions of a refund agent both sent the customer $420. FAR checks whether the updated version preserved the evidence, policy constraints, and authorization that made the original decision acceptable.</p></div><aside class="heroaside"><div class="signal"><div class="signalhead"><span>Business outcome</span><span>Both versions</span></div><div class="signalvalue">$420</div><div class="signallabel">Refund completed successfully. A normal outcome test sees no regression.</div></div></aside></header>
<section class="section"><div class="sectionhead"><div class="sectionlabel">01 · Operating context</div><div><h2 class="sectiontitle">A routine AI update creates a hidden governance question.</h2><p class="lede">The company is not asking whether the refund happened. It is asking whether the updated system still followed the control structure that authorized it.</p></div></div><div class="scenario"><article><div class="n">01</div><h3>Customer request</h3><p>A customer asks the company to return $420 after a disputed purchase.</p></article><article><div class="n">02</div><h3>Automated handling</h3><p>An AI agent reads the request, checks policy, and can issue refunds without an employee manually completing every step.</p></article><article><div class="n">03</div><h3>Human control</h3><p>Refunds above $250 require explicit supervisor approval before money is released.</p></article><article><div class="n">04</div><h3>System update</h3><p>The company deploys a faster version and needs to know whether the safeguard survived the change.</p></article></div><div class="policy"><span>Binding policy</span><p>For any refund above $250, supervisor approval must be connected to the final refund decision.</p></div></section>
<section class="section"><div class="sectionhead"><div class="sectionlabel">02 · Recorded decision paths</div><div><h2 class="sectiontitle">The outcome stayed the same. The structure behind it did not.</h2><p class="lede">FAR compares the dependencies behind the final action, not just the final action itself.</p></div></div><div class="comparewrap"><div class="comparetop"><span>Decision path comparison</span><span>Policy version: refund-policy-v3</span></div><div class="compare"><article class="run"><div class="runhead"><div class="runname">Baseline agent</div><div class="status ok">Justified</div></div><ol class="steps"><li><span class="idx">01</span><span>Customer requested a $420 refund.</span><span class="chip">Evidence</span></li><li><span class="idx">02</span><span>Refunds above $250 require approval.</span><span class="chip">Policy</span></li><li><span class="idx">03</span><span>Supervisor approved the refund.</span><span class="chip">Authorization</span></li><li><span class="idx">04</span><span>Issue the $420 refund.</span><span class="chip">Decision</span></li></ol></article><article class="run"><div class="runhead"><div class="runname">Updated agent</div><div class="status bad">Unsupported</div></div><ol class="steps"><li><span class="idx">01</span><span>Customer requested a $420 refund.</span><span class="chip">Evidence</span></li><li><span class="idx">02</span><span>Refunds above $250 require approval.</span><span class="chip">Policy</span></li><li class="failed"><span class="idx">×</span><span>The approval node exists, but is no longer connected to the refund decision.</span><span class="chip">Broken link</span></li><li class="failed"><span class="idx">04</span><span>Issue the $420 refund anyway.</span><span class="chip">Decision</span></li></ol></article></div><div class="delta"><div><strong>Material change: authorization dependency removed</strong><br><span>The updated system preserved the result while weakening the decision path.</span></div><button id="run" class="primary" onclick="runExample()">Run FAR verification</button></div></div></section>
<section id="answer" class="section answer"><div class="resultcard"><div class="resultgrid"><div class="verdict">Verification result</div><div class="result"><h2 id="headline">The updated agent refunded $420 without recorded supervisor approval.</h2><p id="summary"></p><p id="why"></p><div class="insights"><div class="insight"><b id="transition">—</b><span>Integrity status changed between versions</span></div><div class="insight"><b id="changeCount">—</b><span>Material structural changes detected</span></div><div class="insight"><b id="completeness">—</b><span>Candidate trace completeness</span></div></div><div id="unknowns"></div><div class="actions"><a class="secondary" href="/api/example/report" download>Download deterministic evidence report</a></div><details class="advanced"><summary>Inspect the FAR artifact</summary><pre id="raw"></pre></details></div></div></div></section>
<section class="section"><div class="sectionhead"><div class="sectionlabel">03 · Use your own evidence</div><div><h2 class="sectiontitle">Compare two FAR decision packages.</h2><p class="lede">The public demo accepts the versioned FAR decision-package schema. Raw logs must first be transformed into explicit nodes, dependencies, requirements, and unknowns.</p></div></div><details class="advanced"><summary>Open package analyzer</summary><div class="uploadgrid"><label class="file">Baseline package<input id="baseline" type="file" accept=".json,application/json"></label><label class="file">Candidate package<input id="candidate" type="file" accept=".json,application/json"></label></div><div class="actions"><button class="primary" onclick="runUpload()">Analyze packages</button></div><p id="error" class="error"></p></details></section>
<footer class="footer"><span>Project FAR · Evidence-bound verification</span><span>This demo does not infer hidden reasoning or certify safety, truth, or compliance.</span></footer>
</main><script>
function render(d){headline.textContent=d.headline;summary.textContent=d.plain_summary;why.textContent=d.why_it_matters;transition.textContent=d.status_transition.join(' → ');changeCount.textContent=d.changes.length;completeness.textContent=Math.round(d.trace_completeness*100)+'%';unknowns.innerHTML=(d.unknowns||[]).map(x=>`<div class="unknown"><strong>Unresolved boundary:</strong><br>${x}</div>`).join('');raw.textContent=JSON.stringify(d.artifact,null,2);answer.classList.add('show');answer.scrollIntoView({behavior:'smooth'})}
async function runExample(){run.classList.add('loading');run.textContent='Verifying…';try{const r=await fetch('/api/example');render(await r.json())}finally{run.classList.remove('loading');run.textContent='Run FAR verification'}}
async function runUpload(){const b=baseline.files[0],c=candidate.files[0];if(!b||!c){error.textContent='Choose both FAR decision-package files.';return}const f=new FormData();f.append('baseline',b);f.append('candidate',c);const r=await fetch('/api/analyze',{method:'POST',body:f});const d=await r.json();if(!r.ok){error.textContent=d.detail||'Analysis failed.';return}error.textContent='';render(d)}
</script></body></html>'''
