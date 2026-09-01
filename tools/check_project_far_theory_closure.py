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
REPLICATION = ROOT / "docs/research/project-far-core-v1.1-correction-replication-v1.0.md"
ACCEPTANCE = ROOT / "docs/governance/project-far-theory-closure-acceptance-v1.1.md"
CORRECTION_AUDIT = ROOT / "docs/audits/project-far-core-theory-v1.1-correction-audit.md"
PROGRAM = ROOT / "theory/evaluation/post-closure-assurance-and-application-program-v1.0.json"
W1_PROMOTION = ROOT / "theory/evaluation/pca-w1-independent-review-promotion-v1.0.json"
W1_REVIEW = ROOT / "docs/research/pca-w1-independent-review/07-final-independent-review.json"
ASSURANCE_LEDGER = ROOT / "theory/evaluation/far-core-assurance-v1.0.json"
FORMALIZATION_LEDGER = ROOT / "theory/evaluation/far-core-formalization-ledger-v1.0.json"
OLD_PROGRAM = ROOT / "theory/evaluation/post-terminal-public-evaluation-program-v1.0.json"
REPOSITORY_TRUTH = ROOT / "governance/repository-truth-authority-v1.json"
EXPORT_MANIFEST = ROOT / "exports/far-spec-v1/manifest.json"
EXPECTED_V1_SHA256 = "b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5"
EXPECTED_EXPORT_VERSION = "1.2.0"
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
            if not all(len(values) <= 1 for values in grouped.values()):
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
        REPLICATION,
        ACCEPTANCE,
        CORRECTION_AUDIT,
        PROGRAM,
        W1_PROMOTION,
        W1_REVIEW,
        ASSURANCE_LEDGER,
        FORMALIZATION_LEDGER,
        OLD_PROGRAM,
        REPOSITORY_TRUTH,
        EXPORT_MANIFEST,
    ]
    for rel in rels:
        path = root / rel.relative_to(ROOT)
        if not path.is_file():
            errors.append(f"missing authority/provenance surface: {path.relative_to(root)}")
    if errors:
        return errors

    historical_bytes = (root / HISTORICAL_THEORY.relative_to(ROOT)).read_bytes()
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
        "does **not** say that no representation can be sufficient for every contract",
        "indexed by `L,J,I`",
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
    if current.get("independent_review_status") != "complete_confirmed_14_proved_exact_scopes_novelty_not_established":
        errors.append("v1.1 ledger independent-review promotion drifted")
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

    replication_text = (root / REPLICATION.relative_to(ROOT)).read_text(encoding="utf-8")
    for needle in ("REPLICATED_INTERNAL", "Question", "Execution", "Observation", "Discovery replicated", "not independent review", "10.1214/aoms/1177729032"):
        if needle not in replication_text:
            errors.append(f"correction replication record missing {needle!r}")

    acceptance_text = (root / ACCEPTANCE.relative_to(ROOT)).read_text(encoding="utf-8")
    for needle in (
        "Question → Execution → Observation → Discovery → Replication → Acceptance → Promotion → Repository Change",
        "Accepted governance authority upon merge",
        "internally replicated",
        "export version `1.2.0`",
    ):
        if needle not in acceptance_text:
            errors.append(f"v1.1 acceptance/promotion record missing {needle!r}")

    program = _load(root / PROGRAM.relative_to(ROOT))
    if program.get("program_id") != "POST-CLOSURE-001" or program.get("status") != "active":
        errors.append("post-closure program identity/status mismatch")
    if program.get("governing_theory") != "PROJECT-FAR-CORE-THEORY-1.1":
        errors.append("post-closure program does not govern v1.1")
    if program.get("core_theory_closed") is not True:
        errors.append("post-closure program reopens the terminal kernel")
    workstreams = {w.get("id"): w for w in program.get("workstreams", [])}
    if workstreams.get("PCA-W1-INDEPENDENT-REVIEW", {}).get("state") != "complete":
        errors.append("PCA-W1 must reflect the promoted sealed independent review")
    if workstreams.get("PCA-W2-PROOF-ASSISTANT-FORMALIZATION", {}).get("state") != "complete":
        errors.append("PCA-W2 must reflect completed 14/14 formalization")
    if workstreams.get("PCA-W3-CONTRACT-SCHEMA", {}).get("state") != "complete":
        errors.append("PCA-W3 must reflect the completed versioned contract-schema implementation")
    if workstreams.get("PCA-W4-DOMAIN-CONTRACTS", {}).get("state") != "complete":
        errors.append("PCA-W4 must reflect the completed finite-explicit domain-contract campaign")
    next_action = program.get("next_action", {})
    if next_action.get("workstream") != "PCA-W6-EMPIRICAL-AUDIT-UTILITY" or next_action.get("theory_target") != "PROJECT-FAR-CORE-THEORY-1.1":
        errors.append("post-closure next action must be W6 empirical audit utility against v1.1")

    promotion = _load(root / W1_PROMOTION.relative_to(ROOT))
    review = _load(root / W1_REVIEW.relative_to(ROOT))
    if promotion.get("disposition") != "ACCEPTED_COMPLETE" or promotion.get("terminal_counts") != {
        "PROVED": 14, "REFUTED": 0, "OPEN": 0, "UNDERDETERMINED": 0, "NOT_APPLICABLE": 0
    }:
        errors.append("W1 promotion disposition/counts drifted")
    if review.get("final", {}).get("claim_counts") != {
        "PROVED": 14, "REFUTED": 0, "OPEN": 0, "UNDERDETERMINED": 0, "NOT APPLICABLE": 0
    }:
        errors.append("sealed W1 final-review counts drifted")
    assurance = _load(root / ASSURANCE_LEDGER.relative_to(ROOT))
    assurance_by_id = {item["id"]: item for item in assurance.get("claims", [])}
    formalization = _load(root / FORMALIZATION_LEDGER.relative_to(ROOT))
    formal_by_id = {item["id"]: item for item in formalization.get("claims", [])}
    if set(assurance_by_id) != EXPECTED_CLAIMS or set(formal_by_id) != EXPECTED_CLAIMS:
        errors.append("assurance/formalization ledger coverage drifted")
    for identifier in sorted(EXPECTED_CLAIMS):
        if assurance_by_id.get(identifier, {}).get("truth_disposition") != "PROVED":
            errors.append(f"{identifier}: promoted truth disposition drifted")
        formal = formal_by_id.get(identifier, {})
        if formal.get("formalization_status") != "FORMALIZED" or formal.get("kernel_check") != "PASS":
            errors.append(f"{identifier}: W2 outcome/kernel status drifted")

    old_program = _load(root / OLD_PROGRAM.relative_to(ROOT))
    if old_program.get("status") != "superseded" or old_program.get("superseded_by") != "POST-CLOSURE-001":
        errors.append("historical post-terminal program is still current")

    truth = _load(root / REPOSITORY_TRUTH.relative_to(ROOT))
    status = truth.get("project_status", {})
    if status.get("governing_core") != "PROJECT-FAR-CORE-THEORY-1.1":
        errors.append("repository truth authority does not point to v1.1")
    if status.get("historical_core_sha256") != EXPECTED_V1_SHA256:
        errors.append("repository truth authority does not preserve v1.0 hash")
    if status.get("completed_contract_schema_workstream") != "PCA-W3-CONTRACT-SCHEMA":
        errors.append("repository truth authority does not record completed W3")
    if status.get("completed_domain_contracts_workstream") != "PCA-W4-DOMAIN-CONTRACTS":
        errors.append("repository truth authority does not record completed W4")
    if status.get("completed_approximation_cost_workstream") != "PCA-W5-APPROXIMATION-AND-COST":
        errors.append("repository truth authority does not record completed W5")
    if status.get("active_workstream") != "PCA-W6-EMPIRICAL-AUDIT-UTILITY":
        errors.append("repository truth authority does not point to W6")
    if status.get("formalization_status") != "14_formalized_0_partial_obstruction_0_contradiction":
        errors.append("repository truth authority does not record completed W2 formalization")
    if status.get("domain_contracts_status") != "six_finite_explicit_native_contracts_six_lossy_collisions_six_scoped_repairs_internal_mapping_only":
        errors.append("repository truth authority does not record the bounded W4 result")
    export_truth = truth.get("specification_export", {})
    if export_truth.get("export_version") != EXPECTED_EXPORT_VERSION:
        errors.append("repository truth authority export version mismatch")
    if export_truth.get("governing_core") != "PROJECT-FAR-CORE-THEORY-1.1":
        errors.append("repository truth authority export does not mirror v1.1")
    if export_truth.get("historical_core_status") != "historical":
        errors.append("repository truth authority does not mark embedded v1.0 export historical")

    export_manifest = _load(root / EXPORT_MANIFEST.relative_to(ROOT))
    if export_manifest.get("export_version") != EXPECTED_EXPORT_VERSION or export_manifest.get("exporter_version") != EXPECTED_EXPORT_VERSION:
        errors.append("FAR spec export must be regenerated at version 1.2.0")
    if export_manifest.get("core_theory_id") != "PROJECT-FAR-CORE-THEORY-1.1":
        errors.append("FAR spec export does not identify v1.1 as governing core")
    entries = {row.get("path"): row for row in export_manifest.get("artifacts", [])}
    old_entry = entries.get("theorems/Project-FAR-Theory-Closure-v1.0.md", {})
    if old_entry.get("status") != "historical" or old_entry.get("sha256") != EXPECTED_V1_SHA256:
        errors.append("FAR spec export must preserve v1.0 exactly as historical")
    current_entry = entries.get("theorems/Project-FAR-Theory-Closure-v1.1.md", {})
    if current_entry.get("status") != "canonical" or current_entry.get("source") != "theory/theorems/Project-FAR-Theory-Closure-v1.1.md":
        errors.append("FAR spec export must carry v1.1 as canonical theorem")
    ledger_entry = entries.get("theorems/project-far-core-theory-v1.1.json", {})
    if ledger_entry.get("status") != "canonical" or ledger_entry.get("source") != "theory/terminal/project-far-core-theory-v1.1.json":
        errors.append("FAR spec export must carry v1.1 machine ledger as canonical")

    required_text = {
        "README.md": ["PROJECT-FAR-CORE-THEORY-1.1", "PCA-W2-PROOF-ASSISTANT-FORMALIZATION", "PCA-W3-CONTRACT-SCHEMA", "PCA-W4-DOMAIN-CONTRACTS", "PCA-W5-APPROXIMATION-AND-COST", "Historical v1.0"],
        "docs/project-status.md": ["PROJECT-FAR-CORE-THEORY-1.1", "PCA-W2-PROOF-ASSISTANT-FORMALIZATION", "PCA-W3-CONTRACT-SCHEMA", "PCA-W4-DOMAIN-CONTRACTS", "PCA-W5-APPROXIMATION-AND-COST", "FAR-CORE-010"],
        "docs/ROADMAP.md": ["PROJECT-FAR-CORE-THEORY-1.1", "Export version `1.2.0`", "simultaneous universal least-informativeness"],
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
