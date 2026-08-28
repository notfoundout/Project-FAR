#!/usr/bin/env python3
"""Fail-closed consistency check for the Project FAR core-theory authority chain."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_THEORY = ROOT / "theory/theorems/Project-FAR-Theory-Closure-v1.0.md"
HISTORICAL_LEDGER = ROOT / "theory/terminal/project-far-core-theory-v1.0.json"
CURRENT_THEORY = ROOT / "theory/theorems/Project-FAR-Theory-Closure-v1.1.md"
CURRENT_LEDGER = ROOT / "theory/terminal/project-far-core-theory-v1.1.json"
REGRESSIONS = ROOT / "theory/evaluation/project-far-core-theory-v1.1-regressions.json"
PROGRAM = ROOT / "theory/evaluation/post-closure-assurance-and-application-program-v1.0.json"
OLD_PROGRAM = ROOT / "theory/evaluation/post-terminal-public-evaluation-program-v1.0.json"
REPOSITORY_TRUTH = ROOT / "governance/repository-truth-authority-v1.json"
EXPECTED_V1_SHA256 = "b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5"
EXPECTED_VERDICT = "NONTRIVIAL CONTRACT-FREE MINIMAL ARCHITECTURE IS IMPOSSIBLE; CONTRACT-RELATIVE SUFFICIENCY AND A UNIQUE MINIMAL OBSERVATIONAL QUOTIENT ARE PROVED."
EXPECTED_CLAIMS = {f"FAR-CORE-{i:03d}" for i in range(1, 15)}


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _claim(ledger: dict, claim_id: str) -> dict:
    return next(row for row in ledger.get("claims", []) if row.get("id") == claim_id)


def _check_regressions(regressions: dict, errors: list[str]) -> None:
    cases = {row.get("id"): row for row in regressions.get("cases", [])}

    c4 = cases.get("CE-CORE-004-IDENTITY-SUFFICES")
    if not c4:
        errors.append("missing FAR-CORE-004 identity regression")
    else:
        rep = c4.get("representation", {})
        contracts = c4.get("contracts", {})
        for name in ("constant", "injective"):
            behavior = contracts.get(name, {})
            grouped: dict[str, set[str]] = {}
            for x, r in rep.items():
                grouped.setdefault(r, set()).add(behavior.get(x))
            sufficient = all(len(values) <= 1 for values in grouped.values())
            if not sufficient:
                errors.append(f"FAR-CORE-004 regression: identity must be sufficient for {name}")
        if c4.get("expected", {}).get("representation_minimal_for_constant") is not False:
            errors.append("FAR-CORE-004 regression must record identity as nonminimal for constant observer")
        if c4.get("expected", {}).get("no_single_representation_minimal_for_both") is not True:
            errors.append("FAR-CORE-004 regression lost incompatible-minima expectation")

    c10 = cases.get("CE-CORE-010-FRAME-DOES-NOT-INDEX-T")
    if not c10:
        errors.append("missing FAR-CORE-010 frame regression")
    else:
        theory = set(c10.get("common_theory", []))
        closures = c10.get("closures", {})
        r0 = theory - set(closures.get("Cn_Gamma0_intersect_T", []))
        r1 = theory - set(closures.get("Cn_Gamma1_intersect_T", []))
        expected = c10.get("expected", {})
        if expected.get("exact_theory_same_under_frames") is not True:
            errors.append("FAR-CORE-010 regression must preserve exact theory under frame-only change")
        if sorted(r0) != sorted(expected.get("residue_Gamma0", [])):
            errors.append("FAR-CORE-010 Gamma0 residue fixture mismatch")
        if sorted(r1) != sorted(expected.get("residue_Gamma1", [])):
            errors.append("FAR-CORE-010 Gamma1 residue fixture mismatch")
        if r0 == r1 or expected.get("residue_changes_with_frame") is not True:
            errors.append("FAR-CORE-010 regression must show frame-sensitive residue")


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    rels = [
        HISTORICAL_THEORY,
        HISTORICAL_LEDGER,
        CURRENT_THEORY,
        CURRENT_LEDGER,
        REGRESSIONS,
        PROGRAM,
        OLD_PROGRAM,
        REPOSITORY_TRUTH,
    ]
    paths = [root / p.relative_to(ROOT) for p in rels]
    for path in paths:
        if not path.is_file():
            errors.append(f"missing authority surface: {path.relative_to(root)}")
    if errors:
        return errors

    historical_theory = root / HISTORICAL_THEORY.relative_to(ROOT)
    historical_bytes = historical_theory.read_bytes()
    if hashlib.sha256(historical_bytes).hexdigest() != EXPECTED_V1_SHA256:
        errors.append("historical v1.0 theory bytes changed; immutable base violated")
    if EXPECTED_VERDICT not in historical_bytes.decode("utf-8"):
        errors.append("historical v1.0 theory lost terminal verdict")

    historical_ledger = _load(root / HISTORICAL_LEDGER.relative_to(ROOT))
    if historical_ledger.get("theory_id") != "PROJECT-FAR-CORE-THEORY-1.0":
        errors.append("historical v1.0 ledger identity drifted")

    current_text = (root / CURRENT_THEORY.relative_to(ROOT)).read_text(encoding="utf-8")
    for needle in (
        "PROJECT-FAR-CORE-THEORY-1.1",
        EXPECTED_VERDICT,
        "universal sufficiency alone",
        "exact common theory is indexed by `L,J,I`",
        "10.1214/aoms/1177729032",
        "PCA-W1-INDEPENDENT-REVIEW",
    ):
        if needle not in current_text:
            errors.append(f"current v1.1 theory missing {needle!r}")

    current = _load(root / CURRENT_LEDGER.relative_to(ROOT))
    if current.get("theory_id") != "PROJECT-FAR-CORE-THEORY-1.1":
        errors.append("current core theory identity mismatch")
    if current.get("terminal_verdict") != EXPECTED_VERDICT:
        errors.append("current machine ledger terminal verdict mismatch")
    if current.get("preserved_base", {}).get("sha256") != EXPECTED_V1_SHA256:
        errors.append("v1.1 ledger does not pin immutable v1.0 SHA-256")
    claims = {row.get("id") for row in current.get("claims", [])}
    if claims != EXPECTED_CLAIMS:
        errors.append(f"core claim set mismatch: {sorted(claims ^ EXPECTED_CLAIMS)}")
    proved = {row["id"] for row in current.get("claims", []) if row.get("status") == "proved"}
    if proved != {f"FAR-CORE-{i:03d}" for i in range(1, 14)}:
        errors.append("FAR-CORE-001..013 must remain exactly the proved claim set")
    if _claim(current, "FAR-CORE-014").get("status") != "supported_derived":
        errors.append("FAR-CORE-014 must remain supported_derived")

    c4 = _claim(current, "FAR-CORE-004")
    if "least-informative sufficient" not in c4.get("claim", "") or "universal sufficiency alone is not denied" not in c4.get("claim", ""):
        errors.append("FAR-CORE-004 corrected minimality/sufficiency boundary drifted")

    c10 = _claim(current, "FAR-CORE-010")
    if "L,J,I" not in c10.get("claim", "") or "Γ" not in c10.get("claim", ""):
        errors.append("FAR-CORE-010 exact-theory/residue dependency split drifted")

    _check_regressions(_load(root / REGRESSIONS.relative_to(ROOT)), errors)

    program = _load(root / PROGRAM.relative_to(ROOT))
    if program.get("program_id") != "POST-CLOSURE-001" or program.get("status") != "registered":
        errors.append("post-closure program identity/status mismatch")
    if program.get("governing_theory") != "PROJECT-FAR-CORE-THEORY-1.1":
        errors.append("post-closure program does not govern v1.1")
    if program.get("core_theory_closed") is not True:
        errors.append("post-closure program reopens the terminal kernel")
    workstreams = {w.get("id"): w for w in program.get("workstreams", [])}
    if workstreams.get("PCA-W1-INDEPENDENT-REVIEW", {}).get("state") != "open":
        errors.append("PCA-W1 must remain open; hostile correction audit is not independent review")
    next_action = program.get("next_action", {})
    if next_action.get("workstream") != "PCA-W1-INDEPENDENT-REVIEW" or next_action.get("review_target") != "PROJECT-FAR-CORE-THEORY-1.1":
        errors.append("post-closure next action must be independent review of v1.1")

    old_program = _load(root / OLD_PROGRAM.relative_to(ROOT))
    if old_program.get("status") != "superseded" or old_program.get("superseded_by") != "POST-CLOSURE-001":
        errors.append("historical post-terminal program is still current")

    truth = _load(root / REPOSITORY_TRUTH.relative_to(ROOT))
    status = truth.get("project_status", {})
    if status.get("governing_core") != "PROJECT-FAR-CORE-THEORY-1.1":
        errors.append("repository truth authority does not point to v1.1")
    if status.get("historical_core_sha256") != EXPECTED_V1_SHA256:
        errors.append("repository truth authority does not preserve v1.0 hash")

    required_text = {
        "README.md": ["PROJECT-FAR-CORE-THEORY-1.1", "PCA-W1-INDEPENDENT-REVIEW", "historical v1.0"],
        "docs/project-status.md": ["PROJECT-FAR-CORE-THEORY-1.1", "PCA-W1-INDEPENDENT-REVIEW", "FAR-CORE-010"],
        "docs/governance/project-far-theory-closure-acceptance-v1.1.md": ["identity representation", "frame-subtracted residue", "not independently reviewed"],
        "docs/audits/project-far-core-theory-v1.1-correction-audit.md": ["10.1214/aoms/1177729032", "FAR-CORE-014", "independent review still open"],
    }
    for relative, needles in required_text.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing current authority surface: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{relative}: missing {needle!r}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Project FAR theory-closure conformity: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Project FAR theory-closure conformity: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
