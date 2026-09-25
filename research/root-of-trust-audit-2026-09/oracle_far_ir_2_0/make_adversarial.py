#!/usr/bin/env python3
"""Generate the far-ir/2.0 adversarial corpus in audit_oracle_v2/adversarial/.

Expected diagnostic sequences are HAND-DERIVED from docs/specification/far-ir-2.0-contract.md
and written literally below; they are not computed by oracle.py. The only computed value
is the FROZEN freeze hash (sorted-key compact JSON, ASCII-escaped: the variant that
reproduces all four registered conformance fixture hashes).

`alternatives` records the expected sequence under a different reading of a spec ambiguity
(option names are oracle.Options fields). `schema_multiplicity_ambiguous` marks records whose
number of SCHEMA_CONSTRAINT_VIOLATION codes depends on undefined schema-error granularity.
"""
import copy
import hashlib
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent / "adversarial"

FF, DU, NF = "FACTORIZATION_FAILURE", "DECODER_UNDEFINED", "NONFUNCTIONAL_DECODER"
NC, NE = "QUOTIENT_CLASS_NOT_BEHAVIOR_CONSTANT", "QUOTIENT_NOT_EXACT_BEHAVIOR_KERNEL"
NP, OV = "QUOTIENT_NOT_PARTITION", "QUOTIENT_OVERLAP"
SCV = "SCHEMA_CONSTRAINT_VIOLATION"
A, B, C, D = "case.a", "case.b", "case.c", "case.d"


def sha(contract):
    text = json.dumps(contract, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rows(pairs):
    return [{"case_id": k, "value": v} for k, v in pairs]


def contract(cases=(A, B), beta=((A, "even"), (B, "odd")), rho=((A, 0), (B, 1)), **kw):
    c = {
        "id": "adv.contract",
        "contract_version": "2.0",
        "mode": kw.get("mode", "exact"),
        "source_domain": {
            "status": kw.get("sd_status", "EXPLICIT"),
            "kind": kw.get("sd_kind", "finite_explicit"),
            "description": kw.get("sd_description", "Explicit adversarial cases"),
            "cases": [{"id": x, "value": x} for x in cases],
        },
        "required_behavior": {"status": kw.get("beta_status", "EXPLICIT"), "description": "Required behavior", "table": rows(beta)},
        "representation": {"status": kw.get("rho_status", "EXPLICIT"), "description": "Candidate representation", "table": rows(rho)},
        "observation_contexts": [{"id": o, "description": "Observation", "status": "EXPLICIT"} for o in kw.get("obs", ["obs.primary"])],
        "admitted_transformations": [{"id": t, "kind": "equivalence", "description": "Literal equality", "status": "EXPLICIT"} for t in kw.get("trans", ["eq.identity"])],
        "interpretation_profile": {"id": "interp.adv", "description": "Literal finite-table interpretation", "status": "EXPLICIT"},
        "target_model_class": {"id": "target.adv", "description": "Listed cases only", "status": "EXPLICIT"},
        "frame": {"id": "frame.empty", "description": "No background premises", "status": "EXPLICIT"},
    }
    if "approximation" in kw:
        c["approximation"] = kw["approximation"]
    return c


def fact(decoder, status="CHECKED_FINITE_EXPLICIT"):
    return {"kind": "factorization", "status": status,
            "decoder_table": [{"representation_value": r, "behavior_value": b} for r, b in decoder]}


def coll(left, right, status="CHECKED_FINITE_EXPLICIT"):
    return {"kind": "collision", "status": status, "left_case_id": left, "right_case_id": right}


def quot(classes, exact=True, status="CHECKED_FINITE_EXPLICIT"):
    return {"kind": "quotient", "status": status, "claims_exact_observational_quotient": exact,
            "classes": [{"id": f"class.{i}", "case_ids": list(cs)} for i, cs in enumerate(classes)]}


UNK_EV = {"kind": "unknown", "reason": "Not decided under this contract"}
GOOD_DEC = [(0, "even"), (1, "odd")]


def record(c, evidence, outcome, freeze="FROZEN"):
    doc = {
        "format_version": "far-ir/2.0",
        "id": "adv.record",
        "contract": c,
        "report": {"outcome": outcome, "evidence": evidence, "failure_report": []},
        "provenance": {"producer": "audit_oracle_v2 adversarial corpus", "created_at": "2026-09-25T00:00:00Z", "sources": []},
    }
    if freeze == "FROZEN":
        doc["freeze"] = {"status": "FROZEN", "frozen_at": "2026-09-25T00:00:00Z", "contract_sha256": sha(c)}
    elif freeze == "DRAFT":
        doc["freeze"] = {"status": "DRAFT", "frozen_at": None, "contract_sha256": None}
    else:
        doc["freeze"] = freeze
    return doc


Q4 = dict(cases=(A, B, C, D), beta=((A, "x"), (B, "x"), (C, "y"), (D, "y")), rho=((A, "a"), (B, "b"), (C, "c"), (D, "d")))
SAME = ((A, "same"), (B, "same"))
APPROX = {"status": "DECLARED_ONLY", "w5_semantics_established": False, "metric": None, "loss": None, "cost": None}

CASES = []


def add(cid, cls, doc, expected, cite, why, alternatives=None, schema_mult=False, raw=None):
    CASES.append(dict(id=cid, defect_class=cls, doc=doc, raw=raw, expected_codes=expected, cite=cite,
                      why=why, alternatives=alternatives or [], schema_multiplicity_ambiguous=schema_mult))


# ---------------------------------------------------------------- factorization
add("ADV-01", "factorization claimed over a collision", record(contract(rho=SAME), fact([("same", "even")]), "PROVED"),
    [FF], "§3.1, §9.3; Theory v1.0 Thm 1", "r(a)=r(b) but beta differs, so d(r(b))='even'!='odd'.")
add("ADV-02", "nonfunctional decoder masking a collision", record(contract(rho=SAME), fact([("same", "even"), ("same", "odd")]), "PROVED"),
    [NF, FF], "§9.3, §9.8", "Row 2 rebinds 'same'; exactly one case then mis-decodes under either binding.",
    [{"options": {"decoder_binding": "last"}, "expected_codes": [NF, FF]}])
add("ADV-03", "decoder wrong on every case (multiplicity)", record(contract(), fact([(0, "odd"), (1, "even")]), "PROVED"),
    [FF, FF], "§9.7", "One FACTORIZATION_FAILURE per failing case in source_domain order.")
add("ADV-04", "decoder missing a reachable representation value", record(contract(), fact([(0, "even")]), "PROVED"),
    [DU], "§3.1, §9.3", "r(b)=1 has no decoder row.")
add("ADV-05", "decoder row defined off-image (functional)", record(contract(), fact(GOOD_DEC + [(2, "odd")]), "PROVED"),
    [], "§9.3 (no code for unused rows); Theory v1.0 §2.3", "Only rho[X] matters; an unused functional row is not a defect.")
add("ADV-06", "decoder nonfunctional off-image", record(contract(), fact(GOOD_DEC + [(2, "x"), (2, "y")]), "PROVED"),
    [NF], "§9.3", "NONFUNCTIONAL_DECODER is defined over decoder_table rows, not only reachable values (stricter than Theory §2.3).")
add("ADV-07", "case listed twice in source domain", record(contract(cases=(A, B, A)), fact(GOOD_DEC), "PROVED"),
    ["DUPLICATE_DOMAIN_CASE"], "§9.2, §9.8", "Repeated case id; tables still cover the id set; gate suppresses the (correct) factorization.")
add("ADV-08", "behavior table assigns two rows to one case (same value)",
    record(contract(beta=((A, "even"), (A, "even"), (B, "odd"))), fact(GOOD_DEC), "PROVED"),
    ["DUPLICATE_CASE_VALUE"], "§9.2", "Two rows for one case_id, regardless of value agreement.")
add("ADV-09", "representation table assigns conflicting rows to one case",
    record(contract(rho=((A, 0), (A, 1), (B, 1))), fact(GOOD_DEC), "PROVED"),
    ["DUPLICATE_CASE_VALUE"], "§9.2", "Representation is not a function of the case.")
add("ADV-10", "representation not total", record(contract(rho=((A, 0),)), fact(GOOD_DEC), "PROVED"),
    ["CASE_TABLE_COVERAGE_MISMATCH"], "§3.1 incomplete coverage; §9.2", "case.b has no representation value.")
add("ADV-11", "behavior row for a case absent from the domain",
    record(contract(beta=((A, "even"), (B, "odd"), (C, "odd"))), fact(GOOD_DEC), "PROVED"),
    ["CASE_TABLE_COVERAGE_MISMATCH"], "§9.2", "Behavior table covers a non-declared case.")
add("ADV-12", "table-resolution ordering with several defects",
    record(contract(cases=(A, B, A), beta=((A, "even"), (A, "even")), rho=((A, 0), (B, 1), (B, 1), (C, 2)), rho_status="DECLARED"),
           fact([(0, "odd")]), "PROVED"),
    ["DUPLICATE_DOMAIN_CASE", "DUPLICATE_CASE_VALUE", "DUPLICATE_CASE_VALUE", "CASE_TABLE_COVERAGE_MISMATCH",
     "CASE_TABLE_COVERAGE_MISMATCH", "CHECK_REQUIRES_EXPLICIT_TABLES"],
    "§9.8 table-resolution order", "Order: domain dup, beta dup, rho dup, beta coverage, rho coverage, explicit-tables; decoder never examined.")
add("ADV-13", "non-finite domain stops table resolution",
    record(contract(cases=(A, B, A), rho=((A, 0),), sd_kind="described"), fact([(0, "odd")]), "PROVED"),
    ["CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN"], "§9.8 item 1", "Resolution stops immediately; no other §9.2 code may accompany it.")
add("ADV-14", "freeze defect suppresses factorization failure",
    record(contract(), fact([(0, "odd"), (1, "even")]), "PROVED", freeze={"status": "FROZEN", "frozen_at": "2026-09-25T00:00:00Z", "contract_sha256": "0" * 64}),
    ["FREEZE_HASH_MISMATCH"], "§9.8 cross-stage gate", "Spec's own example: exactly [FREEZE_HASH_MISMATCH].")
add("ADV-15", "checked factorization with outcome REFUTED", record(contract(), fact(GOOD_DEC), "REFUTED"),
    ["CHECKED_EVIDENCE_OUTCOME_MISMATCH"], "§3.1, §9.6", "Checked factorization must be PROVED.")

# ---------------------------------------------------------------- collision
add("ADV-16", "checked collision with outcome PROVED", record(contract(rho=SAME), coll(A, B), "PROVED"),
    ["CHECKED_EVIDENCE_OUTCOME_MISMATCH"], "§3.2, §9.6", "Checked collision must be REFUTED.")
add("ADV-17", "collision whose behaviors agree",
    record(contract(rho=SAME, beta=((A, "even"), (B, "even"))), coll(A, B), "REFUTED"),
    ["COLLISION_BEHAVIOR_AGREES"], "§3.2, §9.4", "beta(x1)=beta(x2): not a collision.")
add("ADV-18", "collision whose representations differ", record(contract(), coll(A, B), "REFUTED"),
    ["COLLISION_REPRESENTATION_DIFFERS"], "§3.2, §9.4", "r(a)=0 != r(b)=1.")
add("ADV-19", "collision naming the same case twice", record(contract(), coll(A, A), "REFUTED"),
    ["COLLISION_REQUIRES_DISTINCT_CASES", "COLLISION_BEHAVIOR_AGREES"], "§9.8 within §9.4",
    "Distinctness fails; r(a)=r(a) so no REPRESENTATION_DIFFERS; beta(a)=beta(a) so BEHAVIOR_AGREES.")
add("ADV-20", "collision naming a case outside the domain", record(contract(rho=SAME), coll(A, "case.z"), "REFUTED"),
    ["COLLISION_CASE_UNKNOWN"], "§9.8 within §9.4", "Appended and the check stops.")

# ---------------------------------------------------------------- quotient
add("ADV-21", "quotient merges behaviorally distinct cases, claims exact", record(contract(**Q4), quot([(A, B, C), (D,)]), "PROVED"),
    [NC, NE, NC, NE, NE], "§3.3, §9.5, §9.8", "Pairs (a,c),(b,c) share a class but differ; (c,d) differ in class but agree.",
    [{"options": {"pair_mode": "ordered"}, "expected_codes": [NC, NE, NC, NE, NC, NE, NC, NE, NE, NE]},
     {"options": {"pair_grouping": "grouped"}, "expected_codes": [NC, NC, NE, NE, NE]}])
add("ADV-22", "quotient merges distinct cases, exactness not claimed", record(contract(**Q4), quot([(A, B, C), (D,)], exact=False), "PROVED"),
    [NC, NC], "§3.3, §9.5", "Every class must be behavior-constant even without the exactness claim.",
    [{"options": {"pair_mode": "ordered"}, "expected_codes": [NC, NC, NC, NC]}])
add("ADV-23", "quotient splits a behavior class (non-minimal), claims exact", record(contract(**Q4), quot([(A,), (B,), (C, D)]), "PROVED"),
    [NE], "§3.3, §9.5; Theory v1.0 Thm 2(3)", "beta(a)=beta(b) but a,b in different classes: finer than ker(beta), so not the minimal quotient.",
    [{"options": {"pair_mode": "ordered"}, "expected_codes": [NE, NE]}])
add("ADV-24", "quotient splits a behavior class, exactness not claimed", record(contract(**Q4), quot([(A,), (B,), (C, D)], exact=False), "PROVED"),
    [], "§3.3", "A behavior-constant refinement is accepted when exactness is not claimed.")
add("ADV-25", "quotient omits a case", record(contract(**Q4), quot([(A, B), (C,)]), "PROVED"),
    [NP], "§3.3, §9.5", "case.d uncovered.")
add("ADV-26", "quotient names a case outside the domain", record(contract(**Q4), quot([(A, B), (C, D, "case.e")]), "PROVED"),
    [NP], "§3.3, §9.5", "Union of classes != source_domain.")
add("ADV-27", "quotient classes overlap", record(contract(**Q4), quot([(A, B), (B, C, D)]), "PROVED"),
    [OV, NP], "§9.5, §9.8", "Overlapping classes are not a partition (literal reading).",
    [{"options": {"overlap_implies_not_partition": False}, "expected_codes": [OV, NC, NE, NC, NE]}])
add("ADV-28", "quotient classes permuted (set-of-sets identity)", record(contract(**Q4), quot([(D, C), (B, A)]), "PROVED"),
    [], "§3.3", "Class order and in-class order are not semantic.")

# ---------------------------------------------------------------- Unknown / cross-field
add("ADV-29", "Unknown evidence with PROVED outcome", record(contract(), UNK_EV, "PROVED"),
    ["UNKNOWN_EVIDENCE_REQUIRES_UNKNOWN_OUTCOME"], "§4, §9.6", "Unknown evidence must carry outcome Unknown.")
add("ADV-30", "Unknown outcome with checked factorization evidence", record(contract(), fact(GOOD_DEC), "Unknown"),
    ["UNKNOWN_OUTCOME_REQUIRES_UNKNOWN_EVIDENCE", "CHECKED_EVIDENCE_OUTCOME_MISMATCH"], "§4, §9.8 stage 2", "Two cross-field codes, fixed order.")
add("ADV-31", "Unknown contract mode certifying PROVED", record(contract(mode="Unknown"), fact(GOOD_DEC), "PROVED"),
    ["UNKNOWN_CONTRACT_MODE_REQUIRES_UNKNOWN_OUTCOME"], "§4", "Unknown mode cannot certify a non-Unknown outcome.")
add("ADV-32", "approximate mode with checked evidence", record(contract(mode="approximate", approximation=APPROX), fact(GOOD_DEC), "PROVED"),
    ["W5_SEMANTICS_NOT_ESTABLISHED"], "§6", "W3 rejects checked evidence under approximate mode.")
add("ADV-33", "approximate mode without approximation block", record(contract(mode="approximate"), fact(GOOD_DEC), "PROVED"),
    [SCV], "schema Contract.allOf if/then", "approximation is required when mode=approximate.", schema_mult=True)
add("ADV-34", "duplicate observation context and transformation",
    record(contract(obs=["obs.p", "obs.p"], trans=["eq.i", "eq.i"]), fact(GOOD_DEC), "PROVED"),
    ["DUPLICATE_OBSERVATION_CONTEXT", "DUPLICATE_TRANSFORMATION"], "§9.6, §9.8", "Fixed stage-2 order.")
add("ADV-35", "Unknown conflated with absence in decoder",
    record(contract(beta=((A, "Unknown"), (B, None))), fact([(0, None), (1, "Unknown")]), "PROVED"),
    [FF, FF], "§4; Theory v1.0 P3, Thm 12", "null (absence) and 'Unknown' are distinct behavior values.")
add("ADV-36", "collision separating Unknown from absence is genuine",
    record(contract(rho=SAME, beta=((A, "Unknown"), (B, None))), coll(A, B), "REFUTED"),
    [], "§3.2; Theory v1.0 Thm 12", "Behaviors differ, representation identifies them: valid REFUTED witness.")
add("ADV-37", "null behavior value decoded legitimately",
    record(contract(beta=((A, None), (B, "odd"))), fact([(0, None), (1, "odd")]), "PROVED"),
    [], "§9.3 (DECODER_UNDEFINED = no matching row)", "A row whose behavior_value is null exists; it is not 'undefined'.")
add("ADV-38", "null representation value decoded legitimately",
    record(contract(rho=((A, None), (B, 1))), fact([(None, "even"), (1, "odd")]), "PROVED"),
    [], "§9.3", "null is a matchable canonical representation value.")

# ---------------------------------------------------------------- value typing / canonicalization
add("ADV-39", "number vs string representation", record(contract(rho=((A, 1), (B, "1"))), coll(A, B), "REFUTED"),
    ["COLLISION_REPRESENTATION_DIFFERS"], "§9.4 'canonical representation value'", "1 and \"1\" are distinct JSON values under every reading.")
add("ADV-40", "boolean vs number representation (collision)", record(contract(rho=((A, 1), (B, True))), coll(A, B), "REFUTED"),
    ["COLLISION_REPRESENTATION_DIFFERS"], "§9.4; JSON value model", "true != 1 in JSON (and in JSON Schema equality); only host-language == conflates them.",
    [{"options": {"equality": "json_value"}, "expected_codes": ["COLLISION_REPRESENTATION_DIFFERS"]}])
add("ADV-41", "boolean vs number representation (factorization)",
    record(contract(rho=((A, 1), (B, True))), fact([(1, "even"), (True, "odd")]), "PROVED"),
    [], "§9.3", "Two distinct representation values, functional decoder; conflating them would yield NONFUNCTIONAL_DECODER.",
    [{"options": {"equality": "json_value"}, "expected_codes": []}])
add("ADV-42", "integer vs float representation 1 vs 1.0",
    record(contract(rho=((A, 1), (B, 1.0))), coll(A, B), "REFUTED", freeze="DRAFT"),
    ["COLLISION_REPRESENTATION_DIFFERS"], "§9.4 (canonical value undefined)", "AMBIGUOUS: canonical-text reading distinguishes; JSON-number reading equates.",
    [{"options": {"equality": "json_value"}, "expected_codes": []}])
add("ADV-43", "signed zero behavior 0.0 vs -0.0",
    record(contract(rho=SAME, beta=((A, 0.0), (B, -0.0))), coll(A, B), "REFUTED", freeze="DRAFT"),
    [], "§9.4 (behavior equality undefined)", "AMBIGUOUS: canonical text '0.0'!='-0.0'; numeric equality equates.",
    [{"options": {"equality": "json_value"}, "expected_codes": ["COLLISION_BEHAVIOR_AGREES"]}])
add("ADV-44", "object key order in representation",
    record(contract(rho=((A, {"p": 1, "q": 2}), (B, {"q": 2, "p": 1}))), coll(A, B), "REFUTED"),
    [], "§9.4 canonical value; §5 canonical JSON", "Key order is not part of a JSON object's value; representations are shared.",
    [{"options": {"equality": "json_value"}, "expected_codes": []}])
add("ADV-45", "Unicode NFC vs NFD behavior (collision)",
    record(contract(rho=SAME, beta=((A, "é"), (B, "é"))), coll(A, B), "REFUTED", freeze="DRAFT"),
    [], "§9.4; spec defines no normalization", "Distinct code-point sequences are distinct values; normalizing would give BEHAVIOR_AGREES.")
add("ADV-46", "Unicode NFC vs NFD behavior (decoder)",
    record(contract(beta=((A, "é"), (B, "odd"))), fact([(0, "é"), (1, "odd")]), "PROVED", freeze="DRAFT"),
    [FF], "§9.3", "Decoded NFD string differs from required NFC string.")

# ---------------------------------------------------------------- domain size edges
add("ADV-47", "empty domain factorization (vacuous)", record(contract(cases=(), beta=(), rho=()), fact([]), "PROVED"),
    [], "§3.1 (no case-count lower bound); Theory v1.0 §2.3", "Vacuously PROVED; flagged as a spec gap, not a defect.")
add("ADV-48", "empty domain quotient", record(contract(cases=(), beta=(), rho=()), quot([(A,)]), "PROVED"),
    [NP], "§9.5; schema QuotientEvidence minItems", "Schema forces >=1 non-empty class, which cannot partition the empty set.")
add("ADV-49", "single-case domain exact quotient", record(contract(cases=(A,), beta=((A, "x"),), rho=((A, "a"),)), quot([(A,)]), "PROVED"),
    [], "§3.3", "One class equals ker(beta) on a singleton.")

# ---------------------------------------------------------------- intake / schema
nl = record(contract(), fact(GOOD_DEC), "PROVED")
nl["contract"]["source_domain"]["cases"][0]["id"] = "case.a\n"
nl["freeze"]["contract_sha256"] = sha(nl["contract"])
add("ADV-50", "identifier with trailing newline", nl, [SCV], "schema Identifier pattern (ECMA-262 `$`)",
    "`$` does not match before a trailing newline in JSON Schema regex semantics.", schema_mult=True)
nan_doc = record(contract(beta=((A, "even"), (B, "odd"))), fact(GOOD_DEC), "PROVED", freeze="DRAFT")
nan_text = json.dumps(nan_doc, indent=1).replace('"value": "odd"', '"value": NaN', 1)
add("ADV-51", "NaN literal in behavior table", None, ["UNREADABLE_CONTRACT"], "§9.1; RFC 8259",
    "NaN is not JSON; a permissive parser would instead produce a never-equal value.", raw=nan_text)
dup_doc = record(contract(), fact(GOOD_DEC), "PROVED", freeze="DRAFT")
dup_text = json.dumps(dup_doc, indent=1).replace('"case_id": "case.b",\n     "value": 1', '"case_id": "case.b",\n     "value": 1,\n     "value": 0', 1)
assert dup_text.count('"value": 0') >= 2
add("ADV-52", "duplicate JSON object key", None, [FF], "§9.1 ('well-formed JSON' undefined for duplicate names)",
    "AMBIGUOUS: last-wins makes r(b)=0 -> FF; reject -> UNREADABLE; first-wins -> accept.",
    [{"options": {"duplicate_keys": "reject"}, "expected_codes": ["UNREADABLE_CONTRACT"]}], raw=dup_text)
add("ADV-53", "claims_exact given as integer 1", record(contract(**Q4), dict(quot([(A, B), (C, D)]), claims_exact_observational_quotient=1), "PROVED"),
    [SCV], "schema QuotientEvidence boolean", "1 is not a JSON boolean.", schema_mult=True)
add("ADV-54", "w5_semantics_established given as 0",
    record(contract(mode="approximate", approximation=dict(APPROX, w5_semantics_established=0)), fact(GOOD_DEC, "DECLARED_UNCHECKED"), "PROVED"),
    [SCV], "§6; schema const false", "JSON Schema const distinguishes 0 from false.", schema_mult=True)
add("ADV-55", "FROZEN with null hash", record(contract(), fact(GOOD_DEC), "PROVED", freeze={"status": "FROZEN", "frozen_at": "2026-09-25T00:00:00Z", "contract_sha256": None}),
    [SCV], "§5; schema Freeze if/then", "FROZEN requires a 64-hex hash.", schema_mult=True)
add("ADV-56", "FROZEN with non-RFC3339 time", record(contract(), fact(GOOD_DEC), "PROVED", freeze={"status": "FROZEN", "frozen_at": "2026-09-25 00:00:00", "contract_sha256": sha(contract())}),
    [SCV, SCV], "§5 'RFC3339 freeze time'; schema format", "AMBIGUOUS: format is annotation-only by default in 2020-12.",
    [{"options": {"assert_format": False}, "expected_codes": []}], schema_mult=True)
add("ADV-57", "DRAFT with stale hash", record(contract(), fact(GOOD_DEC), "PROVED", freeze={"status": "DRAFT", "frozen_at": None, "contract_sha256": "0" * 64}),
    [], "§9.6 FREEZE_HASH_MISMATCH (FROZEN only)", "Spec checks the hash only for FROZEN; flagged as a gap.")
add("ADV-58", "DECLARED_UNCHECKED false factorization", record(contract(), fact([(0, "odd"), (1, "even")], "DECLARED_UNCHECKED"), "PROVED"),
    [], "§9.8 stage 3", "Unchecked evidence runs no claim-specific check; flagged as a gap (PROVED without check).")
na = contract(sd_description="Café cases")
add("ADV-59", "non-ASCII contract hash canonicalization", record(na, fact(GOOD_DEC), "PROVED"),
    [], "§5 'canonical JSON' undefined", "AMBIGUOUS: hash made with ASCII escaping; raw-UTF-8 canonicalization mismatches.",
    [{"options": {"hash_ascii": False}, "expected_codes": ["FREEZE_HASH_MISMATCH"]}])
add("ADV-60", "uppercase hex freeze hash", record(contract(), fact(GOOD_DEC), "PROVED", freeze={"status": "FROZEN", "frozen_at": "2026-09-25T00:00:00Z", "contract_sha256": sha(contract()).upper()}),
    [SCV, SCV], "schema pattern ^[0-9a-f]{64}$", "Uppercase hex violates the base and FROZEN-branch patterns.", schema_mult=True)

# ---------------------------------------------------------------- multiplicity / binding sensitivity
add("ADV-61", "nonfunctional decoder: binding sensitivity", record(contract(), fact([(0, "even"), (0, "odd"), (1, "odd")]), "PROVED"),
    [NF], "§9.3 (binding for nonfunctional value undefined)", "AMBIGUOUS count: first-binding decodes a correctly; last-binding adds FF.",
    [{"options": {"decoder_binding": "last"}, "expected_codes": [NF, FF]}])
add("ADV-62", "nonfunctional decoder: offending-row sensitivity", record(contract(), fact([(0, "even"), (0, "odd"), (0, "even"), (1, "odd")]), "PROVED"),
    [NF], "§9.8 'per offending decoder row'", "AMBIGUOUS count: row 3 agrees with row 1 but not row 2.",
    [{"options": {"nonfunctional_rule": "any"}, "expected_codes": [NF, NF]}])
add("ADV-63", "valid all-Unknown record", record(contract(mode="Unknown"), UNK_EV, "Unknown"),
    [], "§4", "Unknown is a first-class value; this record is consistent.")
add("ADV-64", "Unknown evidence with OPEN outcome", record(contract(), UNK_EV, "OPEN"),
    ["UNKNOWN_EVIDENCE_REQUIRES_UNKNOWN_OUTCOME"], "§4", "OPEN is not Unknown.")
add("ADV-65", "outcome spelled 'unknown'", record(contract(), UNK_EV, "unknown"),
    [SCV], "schema TypedOutcome enum", "Enum is case-sensitive.", schema_mult=True)
add("ADV-66", "behavior table status Unknown under checked evidence", record(contract(beta_status="Unknown"), fact(GOOD_DEC), "PROVED"),
    ["CHECK_REQUIRES_EXPLICIT_TABLES"], "§3, §9.2", "Checked evidence requires EXPLICIT tables.")
add("ADV-67", "finite domain with DECLARED status", record(contract(sd_status="DECLARED"), fact(GOOD_DEC), "PROVED"),
    ["CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN"], "§3, §9.2", "Requires kind finite_explicit AND status EXPLICIT.")
add("ADV-68", "cross-field defect gates a bad collision",
    record(contract(obs=["obs.p", "obs.p"], rho=SAME, beta=((A, "even"), (B, "even"))), coll(A, B), "REFUTED"),
    ["DUPLICATE_OBSERVATION_CONTEXT"], "§9.8 cross-stage gate", "COLLISION_BEHAVIOR_AGREES must not be reported.")
rev = record(contract(), fact(GOOD_DEC), "PROVED")
rev["contract"] = dict(reversed(list(rev["contract"].items())))
add("ADV-69", "contract keys in non-sorted order", rev, [], "§5 canonical JSON", "Hash binds canonical content, not file key order.")
add("ADV-70", "duplicate quotient class ids", record(contract(**Q4), dict(quot([(A, B), (C, D)]), classes=[{"id": "k", "case_ids": [A, B]}, {"id": "k", "case_ids": [C, D]}]), "PROVED"),
    [], "§9.5 (no code); schema (no uniqueness)", "Accepted; flagged as a gap.")
add("ADV-71", "wrong format_version", dict(record(contract(), fact(GOOD_DEC), "PROVED"), format_version="far-ir/2.1"),
    [SCV], "§1; schema const", "Only far-ir/2.0 is in scope.", schema_mult=True)
add("ADV-72", "both tables non-EXPLICIT (multiplicity)", record(contract(beta_status="DECLARED", rho_status="DECLARED"), fact(GOOD_DEC), "PROVED"),
    ["CHECK_REQUIRES_EXPLICIT_TABLES"], "§9.2", "AMBIGUOUS count: one condition or one per table.",
    [{"options": {"explicit_tables_multiplicity": "per_table"}, "expected_codes": ["CHECK_REQUIRES_EXPLICIT_TABLES"] * 2}])
add("ADV-73", "case listed three times (multiplicity)", record(contract(cases=(A, B, A, A)), fact(GOOD_DEC), "PROVED"),
    ["DUPLICATE_DOMAIN_CASE"] * 2, "§9.7 'once per offending item'", "AMBIGUOUS count: per extra occurrence (2) or per repeated id (1).",
    [{"options": {"duplicate_multiplicity": "per_distinct_id"}, "expected_codes": ["DUPLICATE_DOMAIN_CASE"]}])
add("ADV-74", "integers beyond IEEE-754 exact range",
    record(contract(rho=((A, 9007199254740993), (B, 9007199254740992))), coll(A, B), "REFUTED", freeze="DRAFT"),
    ["COLLISION_REPRESENTATION_DIFFERS"], "§9.4; RFC 8259 §6", "AMBIGUOUS: exact integers differ; a double-precision parser collapses them and would accept the collision.")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    for case in CASES:
        name = f"{case['id']}.json"
        text = case["raw"] if case["raw"] is not None else json.dumps(case["doc"], indent=1, ensure_ascii=False)
        (OUT / name).write_text(text + "\n", encoding="utf-8")
        index.append({
            "id": case["id"], "file": name, "defect_class": case["defect_class"],
            "expected_valid": not case["expected_codes"], "expected_codes": case["expected_codes"],
            "alternatives": case["alternatives"],
            "codes_interpretation_dependent": any(a["expected_codes"] != case["expected_codes"] for a in case["alternatives"]),
            "verdict_interpretation_dependent": any(bool(a["expected_codes"]) != bool(case["expected_codes"]) for a in case["alternatives"]),
            "schema_multiplicity_ambiguous": case["schema_multiplicity_ambiguous"],
            "spec_citation": case["cite"], "justification": case["why"],
        })
    (OUT / "index.json").write_text(json.dumps({"corpus": "far-ir-2.0 adversarial (audit_oracle_v2)", "cases": index}, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {len(index)} records to {OUT}")


if __name__ == "__main__":
    main()
