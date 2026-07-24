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
app = FastAPI(title="Project FAR Demo", version="0.6.1")


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
        summary = (
            f"FAR compared the supplied baseline and candidate {decision_type} packages. "
            f"The candidate no longer records {len(removed_statements)} dependency"
            f"{'ies' if len(removed_statements) != 1 else 'y'} that supported the baseline decision: "
            + "; ".join(removed_statements)
        )
    elif added:
        summary = (
            f"FAR compared the supplied baseline and candidate {decision_type} packages. "
            f"The candidate records {len(added)} additional decision dependenc"
            f"{'ies' if len(added) != 1 else 'y'}."
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
    presentation = narrative or _generic_narrative(
        baseline=baseline,
        candidate=candidate,
        status=status,
        removed=removed,
        added=added,
        baseline_nodes=baseline_nodes,
    )

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
        "headline": presentation["headline"],
        "plain_summary": presentation["plain_summary"],
        "why_it_matters": presentation["why_it_matters"],
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
:root{--bg:#f5f4ef;--ink:#11120f;--muted:#6d7068;--line:rgba(17,18,15,.13);--panel:rgba(255,255,255,.72);--dark:#151713;--lime:#d9ff6a;--violet:#9b8cff;--red:#df5b4b;--shadow:0 30px 90px rgba(17,18,15,.08);font-family:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 82% 8%,rgba(155,140,255,.18),transparent 30%),radial-gradient(circle at 12% 34%,rgba(217,255,106,.2),transparent 28%),var(--bg);color:var(--ink)}button,input{font:inherit}.shell{max-width:1260px;margin:auto;padding:0 28px}.nav{height:74px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line)}.brand{font-weight:760;letter-spacing:-.03em}.navnote,.muted{color:var(--muted)}.hero{padding:96px 0 72px;display:grid;grid-template-columns:1.35fr .65fr;gap:54px;align-items:end}.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:22px}.hero h1{font-size:clamp(54px,7vw,96px);line-height:.92;letter-spacing:-.07em;font-weight:570;margin:0}.hero p{font-size:22px;line-height:1.45;color:#3c3f37;max-width:760px}.signal{background:var(--panel);border:1px solid var(--line);border-radius:26px;padding:28px;box-shadow:var(--shadow)}.signal b{display:block;font-size:54px;letter-spacing:-.06em;margin:24px 0 6px}.section{padding:78px 0;border-top:1px solid var(--line)}.section h2{font-size:clamp(36px,4vw,60px);letter-spacing:-.055em;font-weight:560;margin:0 0 20px}.lede{font-size:19px;line-height:1.55;max-width:820px;color:#44473f}.compare{background:var(--dark);color:white;border-radius:30px;padding:22px;display:grid;grid-template-columns:1fr 1fr;gap:14px;box-shadow:0 36px 100px rgba(17,18,15,.15)}.run{background:#1d201a;border:1px solid rgba(255,255,255,.08);border-radius:22px;padding:26px}.run h3{font-size:28px;margin:0 0 24px}.steps{list-style:none;padding:0;margin:0}.steps li{padding:15px 0;border-top:1px solid rgba(255,255,255,.09);display:flex;gap:12px}.bad{color:#ffab9f}.actions{margin-top:20px;display:flex;gap:14px;flex-wrap:wrap}.primary{border:0;background:var(--lime);border-radius:999px;padding:15px 22px;font-weight:720;cursor:pointer}.secondary{color:inherit}.result{display:none;background:var(--panel);border:1px solid var(--line);border-radius:28px;padding:34px;box-shadow:var(--shadow)}.result.show{display:block}.result h2{margin-top:0}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:28px}.metric{padding:18px;border:1px solid var(--line);border-radius:16px}.metric b{display:block;font-size:26px}.upload{display:grid;grid-template-columns:1fr 1fr;gap:16px}.file{background:white;border:1px solid var(--line);border-radius:18px;padding:20px}.file input{display:block;margin-top:12px;max-width:100%}pre{white-space:pre-wrap;max-height:420px;overflow:auto;background:#10120f;color:#e9ece5;border-radius:18px;padding:20px;font-size:12px}.error{color:var(--red)}footer{padding:32px 0 56px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}@media(max-width:850px){.hero,.compare,.upload,.metrics{grid-template-columns:1fr}.hero{padding-top:62px}.shell{padding:0 16px}}
</style>
</head>
<body><main class="shell">
<nav class="nav"><div class="brand">FAR</div><div class="navnote">Decision integrity for AI systems</div></nav>
<header class="hero"><div><div class="eyebrow">Interactive verification case</div><h1>Did the AI preserve the rules—or only the result?</h1><p>Two versions of a refund agent both sent the customer $420. FAR checks whether the updated version preserved the evidence, policy constraints, and authorization that made the original decision acceptable.</p></div><aside class="signal"><span class="muted">Business outcome · both versions</span><b>$420</b><span class="muted">Refund completed. Ordinary outcome testing sees no regression.</span></aside></header>
<section class="section"><h2>The outcome stayed the same. The structure behind it did not.</h2><p class="lede">The baseline links the request, policy, and supervisor authorization to the refund. The candidate preserves the refund while removing the recorded authorization dependency.</p><div class="compare"><article class="run"><h3>Baseline · justified</h3><ol class="steps"><li>Customer requested a $420 refund.</li><li>Refunds above $250 require approval.</li><li>Supervisor approved the refund.</li><li>Issue the $420 refund.</li></ol></article><article class="run"><h3 class="bad">Candidate · unsupported</h3><ol class="steps"><li>Customer requested a $420 refund.</li><li>Refunds above $250 require approval.</li><li class="bad">Approval is no longer connected to the decision.</li><li>Issue the $420 refund anyway.</li></ol></article></div><div class="actions"><button class="primary" onclick="runExample()">Run FAR verification</button></div></section>
<section class="section"><div id="result" class="result"><div class="eyebrow">Verification result</div><h2 id="headline"></h2><p id="summary" class="lede"></p><p id="why" class="lede"></p><div class="metrics"><div class="metric"><b id="transition">—</b><span>Status transition</span></div><div class="metric"><b id="changeCount">—</b><span>Recorded changes</span></div><div class="metric"><b id="completeness">—</b><span>Trace completeness</span></div></div><div id="unknowns"></div><div class="actions"><a class="secondary" href="/api/example/report" download>Download deterministic evidence report</a></div><details><summary>Inspect FAR artifact</summary><pre id="raw"></pre></details></div></section>
<section class="section"><h2>Use your own FAR decision packages.</h2><p class="lede">Uploaded analyses receive generic, evidence-derived summaries. The sample refund narrative is never applied to unrelated packages.</p><form id="form"><div class="upload"><label class="file">Baseline package<input name="baseline" type="file" accept="application/json,.json" required></label><label class="file">Candidate package<input name="candidate" type="file" accept="application/json,.json" required></label></div><div class="actions"><button class="primary" type="submit">Analyze supplied evidence</button></div><p id="error" class="error"></p></form></section>
<footer>FAR evaluates supplied packages and recorded dependencies only. It does not infer hidden reasoning, external truth, safety, or regulatory compliance.</footer>
</main>
<script>
function render(d){document.getElementById('headline').textContent=d.headline;document.getElementById('summary').textContent=d.plain_summary;document.getElementById('why').textContent=d.why_it_matters;document.getElementById('transition').textContent=d.status_transition.join(' → ');document.getElementById('changeCount').textContent=d.changes.length;document.getElementById('completeness').textContent=Math.round(d.trace_completeness*100)+'%';document.getElementById('unknowns').innerHTML=d.unknowns.length?'<p class="muted"><b>Declared unknowns:</b> '+d.unknowns.map(x=>String(x).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))).join('; ')+'</p>':'';document.getElementById('raw').textContent=JSON.stringify(d.artifact,null,2);document.getElementById('result').classList.add('show');document.getElementById('result').scrollIntoView({behavior:'smooth'});}
async function runExample(){const r=await fetch('/api/example');render(await r.json());}
document.getElementById('form').addEventListener('submit',async e=>{e.preventDefault();const error=document.getElementById('error');error.textContent='';try{const r=await fetch('/api/analyze',{method:'POST',body:new FormData(e.target)});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Analysis failed');render(d);}catch(err){error.textContent=err.message;}});
</script>
</body></html>'''
