from __future__ import annotations

import hashlib
import json
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, Response

from far_decision_integrity.adjudicate import adjudicate
from far_decision_integrity.model import DecisionPackage, PackageValidationError
from far_decision_integrity.report import report_payload

from .formats import ACCEPT_ATTRIBUTE, parse_package_file

MAX_BYTES = 10_000_000
app = FastAPI(title="Project FAR Demo", version="0.7.0")


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


def _generic_narrative(
    *,
    baseline: DecisionPackage,
    candidate: DecisionPackage,
    status: str,
    removed: list[str],
    added: list[str],
    baseline_nodes: dict[str, dict[str, Any]],
) -> dict[str, str]:
    headline = {
        "unsupported": "The candidate decision is unsupported by the supplied dependency record.",
        "unverifiable": "The supplied evidence is insufficient to verify the candidate decision.",
        "underdetermined": "The supplied evidence supports more than one possible conclusion.",
        "justified": "The supplied evidence supports the candidate decision.",
    }[status]

    decision_type = candidate.decision_type or baseline.decision_type or "decision"
    removed_statements = [
        baseline_nodes.get(node_id, {"statement": node_id})["statement"] for node_id in removed
    ]
    if removed_statements:
        noun = "dependency" if len(removed_statements) == 1 else "dependencies"
        summary = (
            f"FAR compared the supplied baseline and candidate {decision_type} packages. "
            f"The candidate no longer records {len(removed_statements)} {noun} that supported "
            "the baseline decision: " + "; ".join(removed_statements)
        )
    elif added:
        noun = "dependency" if len(added) == 1 else "dependencies"
        summary = (
            f"FAR compared the supplied baseline and candidate {decision_type} packages. "
            f"The candidate records {len(added)} additional decision {noun}."
        )
    else:
        summary = (
            f"FAR compared the supplied baseline and candidate {decision_type} packages. "
            "No direct decision-root dependency additions or removals were recorded."
        )

    why_it_matters = (
        "FAR evaluates only the supplied nodes, dependencies, requirements, and declared unknowns. "
        "The result does not establish hidden reasoning, external truth, safety, or regulatory compliance."
    )
    return {"headline": headline, "plain_summary": summary, "why_it_matters": why_it_matters}


def _present(
    baseline: DecisionPackage,
    candidate: DecisionPackage,
    *,
    narrative: dict[str, str] | None = None,
) -> dict[str, Any]:
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

    structural_changes: list[dict[str, Any]] = []
    for node_id in removed:
        required = node_id in baseline.authorization_requirements
        structural_changes.append(
            {
                "type": "authorization_dependency_removed" if required else "decision_dependency_removed",
                "severity": "critical" if required else "high",
                "title": "Required approval was removed" if required else "Decision support was removed",
                "description": baseline_nodes.get(node_id, {"statement": node_id})["statement"],
                "node_id": node_id,
            }
        )
    for node_id in added:
        structural_changes.append(
            {
                "type": "decision_dependency_added",
                "severity": "review",
                "title": "New decision support appeared",
                "description": candidate_nodes.get(node_id, {"statement": node_id})["statement"],
                "node_id": node_id,
            }
        )

    rule_findings: list[dict[str, Any]] = []
    baseline_rule_ids = {finding["rule_id"] for finding in baseline_report["findings"]}
    for finding in candidate_report["findings"]:
        if finding["rule_id"] not in baseline_rule_ids:
            rule_findings.append(
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
    presentation = narrative or _generic_narrative(
        baseline=baseline,
        candidate=candidate,
        status=status,
        removed=removed,
        added=added,
        baseline_nodes=baseline_nodes,
    )

    artifact = {
        "schema": "far-demo-report/0.7",
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
        "headline": presentation["headline"],
        "plain_summary": presentation["plain_summary"],
        "why_it_matters": presentation["why_it_matters"],
        "status_transition": [
            baseline_adjudication.status.value,
            candidate_adjudication.status.value,
        ],
        "structural_changes": structural_changes,
        "rule_findings": rule_findings,
        "changes": structural_changes + rule_findings,
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

SAMPLE_NARRATIVE = {
    "headline": "The updated agent refunded $420 without recorded supervisor approval.",
    "plain_summary": "The company updated its refund AI. The old version asked a supervisor before refunds over $250. The new version still issued the $420 refund, but its recorded decision path no longer contains the approval dependency.",
    "why_it_matters": "A normal performance test would say both systems succeeded because both completed the refund. FAR checks whether the updated system preserved the controls that made the original decision acceptable.",
}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "far-demo", "engine": "far-decision-integrity"}


@app.get("/api/example")
def example() -> dict[str, Any]:
    return _present(
        _package(SAMPLE_BASELINE),
        _package(SAMPLE_CANDIDATE),
        narrative=SAMPLE_NARRATIVE,
    )


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
    try:
        baseline_bytes = await baseline.read(MAX_BYTES + 1)
        candidate_bytes = await candidate.read(MAX_BYTES + 1)
        if len(baseline_bytes) > MAX_BYTES or len(candidate_bytes) > MAX_BYTES:
            raise ValueError("Each upload must be 10 MB or smaller.")
        baseline_package = _package(parse_package_file(baseline.filename or "", baseline_bytes))
        candidate_package = _package(parse_package_file(candidate.filename or "", candidate_bytes))
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        PackageValidationError,
        ValueError,
    ) as exc:
        raise HTTPException(400, str(exc)) from exc
    return JSONResponse(_present(baseline_package, candidate_package))


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return PAGE.replace("__ACCEPT__", ACCEPT_ATTRIBUTE)


PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FAR — Decision integrity for AI systems</title>
<style>
:root{--bg:#f4f6f8;--surface:#fff;--ink:#111827;--muted:#667085;--line:#d9dee7;--soft:#eef2f6;--navy:#172033;--blue:#2457d6;--blue-hover:#1d46ad;--red:#b42318;--red-soft:#fff1f0;--green:#067647;--shadow:0 18px 50px rgba(16,24,40,.08);font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink)}button,input{font:inherit}.shell{max-width:1220px;margin:auto;padding:0 28px}.nav{height:72px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line)}.brand{font-weight:780;letter-spacing:-.03em}.navnote,.muted{color:var(--muted)}.hero{padding:84px 0 64px;display:grid;grid-template-columns:1.35fr .65fr;gap:52px;align-items:end}.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:18px}.hero h1{font-size:clamp(50px,6.6vw,88px);line-height:.94;letter-spacing:-.065em;font-weight:590;margin:0}.hero p{font-size:21px;line-height:1.5;color:#344054;max-width:760px}.signal{background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:26px;box-shadow:var(--shadow)}.signal b{display:block;font-size:50px;letter-spacing:-.05em;margin:20px 0 5px}.section{padding:68px 0;border-top:1px solid var(--line)}.section h2{font-size:clamp(34px,3.8vw,56px);letter-spacing:-.05em;font-weight:590;margin:0 0 18px}.lede{font-size:18px;line-height:1.55;max-width:850px;color:#475467}.compare{background:var(--soft);border:1px solid var(--line);border-radius:26px;padding:16px;display:grid;grid-template-columns:1fr 1fr;gap:14px;box-shadow:var(--shadow)}.run{background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:25px}.run.candidate{border-color:#f3b3ad}.run h3{font-size:27px;margin:0 0 22px;color:var(--navy)}.run.candidate h3{color:var(--red)}.steps{list-style:none;padding:0;margin:0}.steps li{padding:15px 0;border-top:1px solid var(--line);display:flex;gap:12px;color:#344054}.steps li.alert{color:var(--red);font-weight:620}.actions{margin-top:22px;display:flex;gap:14px;flex-wrap:wrap}.primary{border:1px solid var(--navy);background:var(--navy);color:white;border-radius:10px;padding:14px 20px;font-weight:700;cursor:pointer;box-shadow:0 4px 10px rgba(23,32,51,.12)}.primary:hover{background:#26334d}.secondary{color:var(--blue);font-weight:650}.result{display:none;background:var(--surface);border:1px solid var(--line);border-radius:24px;padding:32px;box-shadow:var(--shadow)}.result.show{display:block}.result h2{margin-top:0;max-width:980px}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:26px}.metric{padding:18px;border:1px solid var(--line);background:#fafbfc;border-radius:14px}.metric b{display:block;font-size:25px;margin-bottom:4px}.finding{margin-top:18px;padding:16px 18px;background:var(--red-soft);border-left:4px solid var(--red);border-radius:8px}.upload{display:grid;grid-template-columns:1fr 1fr;gap:16px}.file{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;font-weight:650}.file input{display:block;margin-top:12px;max-width:100%;font-weight:400}.support{margin-top:14px;font-size:14px;color:var(--muted)}details{margin-top:18px}pre{white-space:pre-wrap;max-height:420px;overflow:auto;background:var(--navy);color:#f8fafc;border-radius:14px;padding:20px;font-size:12px}.error{color:var(--red)}footer{padding:30px 0 52px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}@media(max-width:850px){.hero,.compare,.upload,.metrics{grid-template-columns:1fr}.hero{padding:56px 0 46px;gap:28px}.shell{padding:0 16px}.section{padding:52px 0}.result{padding:22px 18px}.result h2{font-size:clamp(34px,10vw,48px);line-height:1.03}.lede{font-size:17px}.run{padding:20px}.primary{width:100%}}
</style>
</head>
<body><main class="shell">
<nav class="nav"><div class="brand">FAR</div><div class="navnote">Decision integrity for AI systems</div></nav>
<header class="hero"><div><div class="eyebrow">Interactive verification case</div><h1>Did the AI preserve the rules—or only the result?</h1><p>Two versions of a refund agent both sent the customer $420. FAR checks whether the updated version preserved the evidence, policy constraints, and authorization that made the original decision acceptable.</p></div><aside class="signal"><span class="muted">Business outcome · both versions</span><b>$420</b><span class="muted">Refund completed. Ordinary outcome testing sees no regression.</span></aside></header>
<section class="section"><h2>The outcome stayed the same. The structure behind it did not.</h2><p class="lede">The baseline links the request, policy, and supervisor authorization to the refund. The candidate preserves the refund while removing the recorded authorization dependency.</p><div class="compare"><article class="run"><h3>Baseline · justified</h3><ol class="steps"><li>Customer requested a $420 refund.</li><li>Refunds above $250 require approval.</li><li>Supervisor approved the refund.</li><li>Issue the $420 refund.</li></ol></article><article class="run candidate"><h3>Candidate · unsupported</h3><ol class="steps"><li>Customer requested a $420 refund.</li><li>Refunds above $250 require approval.</li><li class="alert">Approval is no longer connected to the decision.</li><li>Issue the $420 refund anyway.</li></ol></article></div><div class="actions"><button class="primary" onclick="runExample()">Run FAR verification</button></div></section>
<section class="section"><div id="result" class="result"><div class="eyebrow">Verification result</div><h2 id="headline"></h2><p id="summary" class="lede"></p><p id="why" class="lede"></p><div id="structural"></div><div class="metrics"><div class="metric"><b id="transition">—</b><span>Status transition</span></div><div class="metric"><b id="changeCount">—</b><span>Primary structural changes</span></div><div class="metric"><b id="completeness">—</b><span>Trace completeness</span></div></div><div id="unknowns"></div><details id="rules"><summary>Additional FAR rule findings</summary><div id="ruleList"></div></details><div class="actions"><a class="secondary" href="/api/example/report" download>Download deterministic evidence report</a></div><details><summary>Inspect FAR artifact</summary><pre id="raw"></pre></details></div></section>
<section class="section"><h2>Use your own FAR decision packages.</h2><p class="lede">Upload the same package format on both sides or mix supported formats. Document files must contain an embedded JSON, YAML, or TOML FAR package; CSV and XLSX use the flat FAR table layout.</p><form id="form"><div class="upload"><label class="file">Baseline package<input name="baseline" type="file" accept="__ACCEPT__" required></label><label class="file">Candidate package<input name="candidate" type="file" accept="__ACCEPT__" required></label></div><p class="support">Supported: JSON, JSONL, YAML, TOML, XML, CSV, TXT, Markdown, DOCX, PDF, and XLSX. Maximum 10 MB each.</p><div class="actions"><button class="primary" type="submit">Analyze supplied evidence</button></div><p id="error" class="error"></p></form></section>
<footer>FAR evaluates supplied packages and recorded dependencies only. It does not infer hidden reasoning, external truth, safety, or regulatory compliance.</footer>
</main>
<script>
const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function render(d){document.getElementById('headline').textContent=d.headline;document.getElementById('summary').textContent=d.plain_summary;document.getElementById('why').textContent=d.why_it_matters;document.getElementById('transition').textContent=d.status_transition.join(' → ');document.getElementById('changeCount').textContent=d.structural_changes.length;document.getElementById('completeness').textContent=Math.round(d.trace_completeness*100)+'%';document.getElementById('structural').innerHTML=d.structural_changes.map(x=>'<div class="finding"><b>'+esc(x.title)+'</b><br>'+esc(x.description)+'</div>').join('');document.getElementById('unknowns').innerHTML=d.unknowns.length?'<p class="muted"><b>Declared unknowns:</b> '+d.unknowns.map(esc).join('; ')+'</p>':'';document.getElementById('ruleList').innerHTML=d.rule_findings.map(x=>'<p><b>'+esc(x.title)+':</b> '+esc(x.description)+'</p>').join('');document.getElementById('rules').style.display=d.rule_findings.length?'block':'none';document.getElementById('raw').textContent=JSON.stringify(d.artifact,null,2);document.getElementById('result').classList.add('show');document.getElementById('result').scrollIntoView({behavior:'smooth'});}
async function runExample(){const r=await fetch('/api/example');render(await r.json());}
document.getElementById('form').addEventListener('submit',async e=>{e.preventDefault();const error=document.getElementById('error');error.textContent='';try{const r=await fetch('/api/analyze',{method:'POST',body:new FormData(e.target)});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Analysis failed');render(d);}catch(err){error.textContent=err.message;}});
</script>
</body></html>'''
