#!/usr/bin/env python3
"""Independent, spec-derived reference oracle for far-ir/2.0 comparison-contract records.

Derived ONLY from:
  - docs/specification/far-ir-2.0-contract.md   (sections 3, 4, 5, 6, 9)
  - schemas/far-contract-v2.schema.json
  - theory/theorems/Project-FAR-Theory-Closure-v1.0.md  (section 2.3/2.4, Theorems 1, 2, 12)
  - theory/theorems/Project-FAR-Theory-Closure-v1.1.md  (section 5 terminal kernel)
No implementation code was read. Standard library only.

Two independent layers:
  1. `diagnose()`  -> the normative diagnostic code sequence (spec section 9).
  2. `mathematics()` -> a partition-lattice / kernel-inclusion judgement computed by a
     different route (sets of frozensets and pairwise kernel enumeration), used to
     cross-check layer 1 whenever the section 9.8 gate is passed.

Every place where the spec is ambiguous is an explicit `Options` field; the default is
one reading, never a claim that it is the intended one.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as _dt
import hashlib
import json
import math
import pathlib
import re
import sys
from fractions import Fraction
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "schemas" / "far-contract-v2.schema.json"


# --------------------------------------------------------------------------- options
@dataclasses.dataclass(frozen=True)
class Options:
    # A-EQ: how "canonical representation value" / "distinct behavior value" is compared.
    #   canonical_json : equal iff sorted-key compact JSON serializations are identical
    #                    (1 != 1.0, 0.0 != -0.0, true != 1, NFC != NFD)
    #   json_value     : JSON-Schema-style value equality (1 == 1.0, 0.0 == -0.0, true != 1)
    equality: str = "canonical_json"
    # A-HASH: canonical JSON for the freeze hash; ASCII-escaped or raw UTF-8.
    hash_ascii: bool = True
    # A-FMT: whether `format: date-time` is asserted (2020-12 default is annotation-only).
    assert_format: bool = True
    # A-DUPKEY: duplicate object keys in the JSON text: "last_wins" or "reject" (UNREADABLE).
    duplicate_keys: str = "last_wins"
    # A-OVERLAP: does an overlapping class set also emit QUOTIENT_NOT_PARTITION?
    overlap_implies_not_partition: bool = True
    # A-PAIRS: "unordered" = pairs (i<j); "ordered" = all (i,j), i != j.
    pair_mode: str = "unordered"
    # A-PAIRORDER: "interleaved" = per pair NC then NE; "grouped" = all NC then all NE.
    pair_grouping: str = "interleaved"
    # A-BIND: which decoder row a nonfunctional representation value decodes through.
    decoder_binding: str = "first"
    # A-NFROW: a later row offends if it differs from the "first" binding or from "any" earlier row.
    nonfunctional_rule: str = "first"
    # A-DUPMULT: duplicates counted "per_extra_occurrence" or "per_distinct_id".
    duplicate_multiplicity: str = "per_extra_occurrence"
    # A-EXPLICIT: CHECK_REQUIRES_EXPLICIT_TABLES emitted "once" or "per_table".
    explicit_tables_multiplicity: str = "once"


DEFAULT = Options()


# --------------------------------------------------------------------------- value semantics
def _jv_key(v: Any):
    """JSON-value identity key (JSON Schema equality: numbers by mathematical value,
    booleans never equal to numbers, strings by code points, objects key-order-free)."""
    if v is None:
        return ("null",)
    if isinstance(v, bool):
        return ("bool", v)
    if isinstance(v, (int, float)):
        if isinstance(v, float) and not math.isfinite(v):
            return ("nonfinite", repr(v))
        return ("num", Fraction(v))
    if isinstance(v, str):
        return ("str", v)
    if isinstance(v, list):
        return ("arr", tuple(_jv_key(x) for x in v))
    if isinstance(v, dict):
        return ("obj", tuple(sorted((k, _jv_key(x)) for k, x in v.items())))
    raise TypeError(type(v))


def canonical_text(v: Any, ascii_only: bool = True) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=ascii_only)


def value_key(v: Any, opts: Options):
    if opts.equality == "canonical_json":
        return canonical_text(v, ascii_only=False)
    if opts.equality == "json_value":
        return _jv_key(v)
    raise ValueError(opts.equality)


def contract_sha256(contract: Any, opts: Options) -> str:
    return hashlib.sha256(canonical_text(contract, opts.hash_ascii).encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- strict JSON intake
class Unreadable(Exception):
    pass


def parse_json_text(text: str, opts: Options) -> Any:
    def reject_constant(name: str):
        raise Unreadable(f"non-JSON constant {name}")

    def pairs_hook(pairs):
        obj: dict = {}
        for k, v in pairs:
            if k in obj and opts.duplicate_keys == "reject":
                raise Unreadable(f"duplicate object key {k!r}")
            obj[k] = v
        return obj

    try:
        return json.loads(text, parse_constant=reject_constant, object_pairs_hook=pairs_hook)
    except (ValueError, RecursionError) as exc:
        raise Unreadable(str(exc)) from exc


# --------------------------------------------------------------------------- mini JSON Schema (2020-12 subset)
_RFC3339 = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})[Tt](\d{2}):(\d{2}):(\d{2})(\.\d+)?([Zz]|[+-](\d{2}):(\d{2}))\Z"
)


def _is_rfc3339(s: str) -> bool:
    m = _RFC3339.match(s)
    if not m:
        return False
    y, mo, d, hh, mm, ss = (int(m.group(i)) for i in range(1, 7))
    try:
        _dt.date(y, mo, d)
    except ValueError:
        return False
    if hh > 23 or mm > 59 or ss > 60:
        return False
    if m.group(9) is not None and (int(m.group(9)) > 23 or int(m.group(10)) > 59):
        return False
    return True


def _ecma_pattern(p: str) -> re.Pattern:
    # ECMA-262 `$` (no m flag) matches only at end of input; Python `$` also matches
    # before a trailing newline. Translate unescaped `$` outside classes to `\Z`.
    out, i, in_class = [], 0, False
    while i < len(p):
        c = p[i]
        if c == "\\":
            out.append(p[i : i + 2]); i += 2; continue
        if c == "[":
            in_class = True
        elif c == "]":
            in_class = False
        elif c == "$" and not in_class:
            out.append(r"\Z"); i += 1; continue
        out.append(c); i += 1
    return re.compile("".join(out))


def _is_type(v: Any, t: str) -> bool:
    if t == "null":
        return v is None
    if t == "boolean":
        return isinstance(v, bool)
    if t == "object":
        return isinstance(v, dict)
    if t == "array":
        return isinstance(v, list)
    if t == "string":
        return isinstance(v, str)
    num = isinstance(v, (int, float)) and not isinstance(v, bool)
    if t == "number":
        return num
    if t == "integer":
        return num and (isinstance(v, int) or (math.isfinite(v) and float(v).is_integer()))
    raise ValueError(t)


class MiniSchema:
    """Evaluates only the keywords used by far-contract-v2.schema.json.
    Error granularity (A-SCHEMAMULT): one error per violated keyword application at an
    instance location; `required`/`additionalProperties` emit one error per property;
    `oneOf` emits one error at its own location without descending."""

    SUPPORTED = {
        "$schema", "$id", "$defs", "title", "description", "type", "additionalProperties",
        "required", "properties", "$ref", "const", "enum", "pattern", "minLength", "minItems",
        "uniqueItems", "items", "propertyNames", "oneOf", "allOf", "if", "then", "format",
    }

    def __init__(self, schema: dict, assert_format: bool):
        self.root = schema
        self.assert_format = assert_format
        self._check_supported(schema)

    def _check_supported(self, s):
        # property names inside `properties`/`$defs` are data, not keywords
        if isinstance(s, dict):
            for k, v in s.items():
                if k in ("properties", "$defs"):
                    for sub in v.values():
                        self._check_supported(sub)
                elif k in ("items", "additionalProperties", "propertyNames", "if", "then"):
                    self._check_supported(v)
                elif k in ("oneOf", "allOf"):
                    for sub in v:
                        self._check_supported(sub)
                elif k not in self.SUPPORTED:
                    raise NotImplementedError(f"schema keyword {k!r} not supported by oracle")

    def _resolve(self, ref: str):
        if not ref.startswith("#/"):
            raise NotImplementedError(ref)
        node = self.root
        for part in ref[2:].split("/"):
            node = node[part]
        return node

    def errors(self, inst: Any, schema: Any = None, path: tuple = ()) -> list:
        if schema is None:
            schema = self.root
        if schema is True or schema == {}:
            return []
        if schema is False:
            return [(path, "false schema")]
        errs: list = []
        if "$ref" in schema:
            errs += self.errors(inst, self._resolve(schema["$ref"]), path)
        if "type" in schema:
            types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
            if not any(_is_type(inst, t) for t in types):
                errs.append((path, f"type: expected {types}"))
        if "const" in schema and _jv_key(inst) != _jv_key(schema["const"]):
            errs.append((path, f"const: expected {schema['const']!r}"))
        if "enum" in schema and _jv_key(inst) not in {_jv_key(e) for e in schema["enum"]}:
            errs.append((path, f"enum: {inst!r} not in {schema['enum']}"))
        if isinstance(inst, str):
            if "pattern" in schema and not _ecma_pattern(schema["pattern"]).search(inst):
                errs.append((path, f"pattern: {schema['pattern']}"))
            if "minLength" in schema and len(inst) < schema["minLength"]:
                errs.append((path, "minLength"))
            if self.assert_format and schema.get("format") == "date-time" and not _is_rfc3339(inst):
                errs.append((path, "format: date-time"))
        if isinstance(inst, list):
            if "minItems" in schema and len(inst) < schema["minItems"]:
                errs.append((path, "minItems"))
            if schema.get("uniqueItems"):
                keys = [_jv_key(x) for x in inst]
                if len(set(keys)) != len(keys):
                    errs.append((path, "uniqueItems"))
            if "items" in schema:
                for i, x in enumerate(inst):
                    errs += self.errors(x, schema["items"], path + (i,))
        if isinstance(inst, dict):
            for req in schema.get("required", []):
                if req not in inst:
                    errs.append((path, f"required: {req}"))
            props = schema.get("properties", {})
            for k, sub in props.items():
                if k in inst:
                    errs += self.errors(inst[k], sub, path + (k,))
            if "additionalProperties" in schema:
                ap = schema["additionalProperties"]
                for k in inst:
                    if k not in props:
                        if ap is False:
                            errs.append((path, f"additionalProperties: {k}"))
                        else:
                            errs += self.errors(inst[k], ap, path + (k,))
            if "propertyNames" in schema:
                for k in inst:
                    if self.errors(k, schema["propertyNames"], path + (k,)):
                        errs.append((path + (k,), "propertyNames"))
        if "allOf" in schema:
            for sub in schema["allOf"]:
                errs += self.errors(inst, sub, path)
        if "oneOf" in schema:
            n = sum(1 for sub in schema["oneOf"] if not self.errors(inst, sub, path))
            if n != 1:
                errs.append((path, f"oneOf: {n} branches valid"))
        if "if" in schema and not self.errors(inst, schema["if"], path) and "then" in schema:
            errs += self.errors(inst, schema["then"], path)
        return errs


_SCHEMA_CACHE: dict = {}


def _schema(opts: Options) -> MiniSchema:
    key = opts.assert_format
    if key not in _SCHEMA_CACHE:
        _SCHEMA_CACHE[key] = MiniSchema(json.loads(SCHEMA_PATH.read_text("utf-8")), key)
    return _SCHEMA_CACHE[key]


# --------------------------------------------------------------------------- diagnostics (spec section 9)
def _dups(ids: list, opts: Options) -> list:
    """Indices of offending duplicate occurrences, in list order."""
    seen, reported, out = set(), set(), []
    for i, x in enumerate(ids):
        if x in seen:
            if opts.duplicate_multiplicity == "per_extra_occurrence" or x not in reported:
                out.append(i)
                reported.add(x)
        seen.add(x)
    return out


def _resolve_tables(c: dict, diags: list, opts: Options):
    """Spec section 9.8 table resolution. Returns (ids, beta, rho) or None when gated."""
    sd = c["source_domain"]
    if sd["kind"] != "finite_explicit" or sd["status"] != "EXPLICIT":
        diags.append("CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN")
        return None
    ids = [case["id"] for case in sd["cases"]]
    diags.extend("DUPLICATE_DOMAIN_CASE" for _ in _dups(ids, opts))
    tables = {}
    for name in ("required_behavior", "representation"):
        rows = c[name]["table"]
        diags.extend("DUPLICATE_CASE_VALUE" for _ in _dups([r["case_id"] for r in rows], opts))
        first: dict = {}
        for r in rows:
            first.setdefault(r["case_id"], r["value"])
        tables[name] = first
    for name in ("required_behavior", "representation"):
        if {r["case_id"] for r in c[name]["table"]} != set(ids):
            diags.append("CASE_TABLE_COVERAGE_MISMATCH")
    bad = [n for n in ("required_behavior", "representation") if c[n]["status"] != "EXPLICIT"]
    if bad:
        k = 1 if opts.explicit_tables_multiplicity == "once" else len(bad)
        diags.extend(["CHECK_REQUIRES_EXPLICIT_TABLES"] * k)
    if diags:  # cross-stage gate: non-empty for ANY reason
        return None
    return ids, tables["required_behavior"], tables["representation"]


def _check_factorization(c, ev, diags, opts):
    res = _resolve_tables(c, diags, opts)
    if res is None:
        return
    ids, beta, rho = res
    K = lambda v: value_key(v, opts)
    first_binding: dict = {}   # rep key -> behavior key of the first row (for A-NFROW)
    decode_with: dict = {}     # rep key -> behavior key used for decoding (A-BIND)
    seen_behaviors: dict = {}  # rep key -> all behavior keys seen so far
    for row in ev["decoder_table"]:
        rk, bk = K(row["representation_value"]), K(row["behavior_value"])
        if rk in first_binding:
            if opts.nonfunctional_rule == "first":
                offends = first_binding[rk] != bk
            else:
                offends = any(b != bk for b in seen_behaviors[rk])
            if offends:
                diags.append("NONFUNCTIONAL_DECODER")
            if opts.decoder_binding == "last":
                decode_with[rk] = bk
            seen_behaviors[rk].add(bk)
        else:
            first_binding[rk] = decode_with[rk] = bk
            seen_behaviors[rk] = {bk}
    for x in ids:
        rk = K(rho[x])
        if rk not in decode_with:  # membership test, not a None test: null is a legal value
            diags.append("DECODER_UNDEFINED")
        elif decode_with[rk] != K(beta[x]):
            diags.append("FACTORIZATION_FAILURE")


def _check_collision(c, ev, diags, opts):
    res = _resolve_tables(c, diags, opts)
    if res is None:
        return
    ids, beta, rho = res
    left, right = ev["left_case_id"], ev["right_case_id"]
    if left not in ids or right not in ids:
        diags.append("COLLISION_CASE_UNKNOWN")
        return
    K = lambda v: value_key(v, opts)
    if left == right:
        diags.append("COLLISION_REQUIRES_DISTINCT_CASES")
    if K(rho[left]) != K(rho[right]):
        diags.append("COLLISION_REPRESENTATION_DIFFERS")
    if K(beta[left]) == K(beta[right]):
        diags.append("COLLISION_BEHAVIOR_AGREES")


def _check_quotient(c, ev, diags, opts):
    res = _resolve_tables(c, diags, opts)
    if res is None:
        return
    ids, beta, _rho = res
    K = lambda v: value_key(v, opts)
    membership: dict = {}
    overlap = False
    for cls in ev["classes"]:
        for x in cls["case_ids"]:
            if x in membership:
                diags.append("QUOTIENT_OVERLAP")
                overlap = True
                membership[x].append(cls["id"])
            else:
                membership[x] = [cls["id"]]
    covered = set(membership) == set(ids)
    if not covered or (overlap and opts.overlap_implies_not_partition):
        diags.append("QUOTIENT_NOT_PARTITION")
        return
    n = len(ids)
    if opts.pair_mode == "unordered":
        pairs = [(ids[i], ids[j]) for i in range(n) for j in range(i + 1, n)]
    else:
        pairs = [(ids[i], ids[j]) for i in range(n) for j in range(n) if i != j]
    nc, ne, inter = [], [], []
    exact = ev["claims_exact_observational_quotient"]
    for x, y in pairs:
        # classes are compared by class-membership sets, not by class id
        same_class = _share_class(ev["classes"], x, y)
        same_beta = K(beta[x]) == K(beta[y])
        a = same_class and not same_beta
        b = exact and (same_class != same_beta)
        if a:
            nc.append("QUOTIENT_CLASS_NOT_BEHAVIOR_CONSTANT"); inter.append(nc[-1])
        if b:
            ne.append("QUOTIENT_NOT_EXACT_BEHAVIOR_KERNEL"); inter.append(ne[-1])
    diags.extend(inter if opts.pair_grouping == "interleaved" else nc + ne)


def _share_class(classes, x, y) -> bool:
    return any(x in cls["case_ids"] and y in cls["case_ids"] for cls in classes)


def diagnose_document(doc: Any, opts: Options = DEFAULT) -> list:
    errs = _schema(opts).errors(doc)
    if errs:
        errs.sort(key=lambda e: ("/".join(map(str, e[0])), e[1]))
        return ["SCHEMA_CONSTRAINT_VIOLATION"] * len(errs)
    diags: list = []
    c, rep = doc["contract"], doc["report"]
    ev, outcome = rep["evidence"], rep["outcome"]
    kind, status = ev["kind"], ev.get("status")
    checked = status == "CHECKED_FINITE_EXPLICIT"
    if kind == "unknown" and outcome != "Unknown":
        diags.append("UNKNOWN_EVIDENCE_REQUIRES_UNKNOWN_OUTCOME")
    if outcome == "Unknown" and kind != "unknown":
        diags.append("UNKNOWN_OUTCOME_REQUIRES_UNKNOWN_EVIDENCE")
    if c["mode"] == "Unknown" and outcome != "Unknown":
        diags.append("UNKNOWN_CONTRACT_MODE_REQUIRES_UNKNOWN_OUTCOME")
    if c["mode"] == "approximate" and checked:
        diags.append("W5_SEMANTICS_NOT_ESTABLISHED")
    if checked and outcome != ("REFUTED" if kind == "collision" else "PROVED"):
        diags.append("CHECKED_EVIDENCE_OUTCOME_MISMATCH")
    diags.extend("DUPLICATE_OBSERVATION_CONTEXT" for _ in _dups([o["id"] for o in c["observation_contexts"]], opts))
    diags.extend("DUPLICATE_TRANSFORMATION" for _ in _dups([t["id"] for t in c["admitted_transformations"]], opts))
    fr = doc["freeze"]
    if fr["status"] == "FROZEN" and fr["contract_sha256"] != contract_sha256(c, opts):
        diags.append("FREEZE_HASH_MISMATCH")
    if checked:
        {"factorization": _check_factorization, "collision": _check_collision,
         "quotient": _check_quotient}[kind](c, ev, diags, opts)
    return diags


def diagnose_text(text: str, opts: Options = DEFAULT) -> list:
    try:
        doc = parse_json_text(text, opts)
    except Unreadable:
        return ["UNREADABLE_CONTRACT"]
    return diagnose_document(doc, opts)


def diagnose_path(path: pathlib.Path, opts: Options = DEFAULT) -> list:
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return ["UNREADABLE_CONTRACT"]
    return diagnose_text(text, opts)


# --------------------------------------------------------------------------- independent mathematics
def _partition(ids, f) -> frozenset:
    blocks: dict = {}
    for x in ids:
        blocks.setdefault(f(x), set()).add(x)
    return frozenset(frozenset(b) for b in blocks.values())


def _kernel(ids, f) -> set:
    return {(x, y) for x in ids for y in ids if f(x) == f(y)}


def mathematics(doc: dict, opts: Options = DEFAULT) -> dict:
    """Partition-lattice view of a finite explicit record whose tables are well-formed.
    Independent of the diagnostic ordering logic above."""
    c, ev = doc["contract"], doc["report"]["evidence"]
    ids = list(dict.fromkeys(case["id"] for case in c["source_domain"]["cases"]))
    beta = {r["case_id"]: r["value"] for r in c["required_behavior"]["table"]}
    rho = {r["case_id"]: r["value"] for r in c["representation"]["table"]}
    if set(beta) != set(ids) or set(rho) != set(ids):
        return {"applicable": False}
    B = lambda x: value_key(beta[x], opts)
    R = lambda x: value_key(rho[x], opts)
    kb, kr = _kernel(ids, B), _kernel(ids, R)
    out = {
        "applicable": True,
        "factorizable": kr <= kb,  # Theorem 1: ker(rho) subset of ker(beta)
        "collisions": sorted((x, y) for (x, y) in kr - kb if ids.index(x) < ids.index(y)),
        "beta_blocks": len(_partition(ids, B)),
    }
    if ev["kind"] == "factorization":
        dec: dict = {}
        functional = True
        for row in ev["decoder_table"]:
            rk, bk = value_key(row["representation_value"], opts), value_key(row["behavior_value"], opts)
            if rk in dec and dec[rk] != bk:
                functional = False
            dec.setdefault(rk, bk)
        out["decoder_certifies"] = functional and all(R(x) in dec and dec[R(x)] == B(x) for x in ids)
    if ev["kind"] == "collision":
        l, r = ev["left_case_id"], ev["right_case_id"]
        out["witness_valid"] = l in ids and r in ids and l != r and (l, r) in kr and (l, r) not in kb
    if ev["kind"] == "quotient":
        blocks = [frozenset(cl["case_ids"]) for cl in ev["classes"]]
        claimed = frozenset(blocks)
        disjoint = sum(len(b) for b in blocks) == len(frozenset().union(*blocks))
        is_partition = disjoint and frozenset().union(*blocks) == frozenset(ids) and len(claimed) == len(blocks)
        target = _partition(ids, B)
        refines = is_partition and all(any(b <= t for t in target) for b in claimed)
        out.update(
            is_partition=is_partition,
            refines_beta=refines,
            equals_beta_partition=is_partition and claimed == target,
            claimed_blocks=len(blocks),
            minimal_by_count=refines and len(claimed) == len(target),
        )
    return out


def cross_check(doc: dict, codes: list, opts: Options = DEFAULT) -> list:
    """Return a list of inconsistencies between the diagnostic layer and the mathematics
    layer. Only meaningful when the section 9.8 gate was passed (no stage-2/9.2 codes)."""
    gate_codes = {
        "UNKNOWN_EVIDENCE_REQUIRES_UNKNOWN_OUTCOME", "UNKNOWN_OUTCOME_REQUIRES_UNKNOWN_EVIDENCE",
        "UNKNOWN_CONTRACT_MODE_REQUIRES_UNKNOWN_OUTCOME", "W5_SEMANTICS_NOT_ESTABLISHED",
        "CHECKED_EVIDENCE_OUTCOME_MISMATCH", "DUPLICATE_OBSERVATION_CONTEXT", "DUPLICATE_TRANSFORMATION",
        "FREEZE_HASH_MISMATCH", "CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN", "DUPLICATE_DOMAIN_CASE",
        "DUPLICATE_CASE_VALUE", "CASE_TABLE_COVERAGE_MISMATCH", "CHECK_REQUIRES_EXPLICIT_TABLES",
        "UNREADABLE_CONTRACT", "SCHEMA_CONSTRAINT_VIOLATION",
    }
    if set(codes) & gate_codes:
        return []
    ev = doc["report"]["evidence"]
    if ev["kind"] == "unknown" or ev.get("status") != "CHECKED_FINITE_EXPLICIT":
        return []
    m = mathematics(doc, opts)
    if not m["applicable"]:
        return ["tables not total although gate passed"]
    problems = []
    ok = not codes
    if ev["kind"] == "factorization":
        if ok != m["decoder_certifies"]:
            problems.append("factorization verdict != decoder_certifies")
        if ok and not m["factorizable"]:
            problems.append("accepted decoder but kernel inclusion fails")
    elif ev["kind"] == "collision":
        if ok != m["witness_valid"]:
            problems.append("collision verdict != witness_valid")
        if ok and m["factorizable"]:
            problems.append("accepted collision but representation factorizes")
    elif ev["kind"] == "quotient" and m["is_partition"]:
        want = m["equals_beta_partition"] if ev["claims_exact_observational_quotient"] else m["refines_beta"]
        if ok != want:
            problems.append("quotient verdict != partition-lattice verdict")
    return problems


# --------------------------------------------------------------------------- CLI
def _options_from_args(ns) -> Options:
    return Options(
        equality=ns.equality, hash_ascii=not ns.hash_utf8, assert_format=not ns.no_format,
        duplicate_keys=ns.duplicate_keys, overlap_implies_not_partition=not ns.overlap_only,
        pair_mode=ns.pair_mode, pair_grouping=ns.pair_grouping, decoder_binding=ns.decoder_binding,
        nonfunctional_rule=ns.nonfunctional_rule, duplicate_multiplicity=ns.duplicate_multiplicity,
        explicit_tables_multiplicity=ns.explicit_tables_multiplicity,
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument("--equality", choices=["canonical_json", "json_value"], default=DEFAULT.equality)
    ap.add_argument("--hash-utf8", action="store_true")
    ap.add_argument("--no-format", action="store_true")
    ap.add_argument("--duplicate-keys", choices=["last_wins", "reject"], default=DEFAULT.duplicate_keys)
    ap.add_argument("--overlap-only", action="store_true")
    ap.add_argument("--pair-mode", choices=["unordered", "ordered"], default=DEFAULT.pair_mode)
    ap.add_argument("--pair-grouping", choices=["interleaved", "grouped"], default=DEFAULT.pair_grouping)
    ap.add_argument("--decoder-binding", choices=["first", "last"], default=DEFAULT.decoder_binding)
    ap.add_argument("--nonfunctional-rule", choices=["first", "any"], default=DEFAULT.nonfunctional_rule)
    ap.add_argument("--duplicate-multiplicity", choices=["per_extra_occurrence", "per_distinct_id"],
                    default=DEFAULT.duplicate_multiplicity)
    ap.add_argument("--explicit-tables-multiplicity", choices=["once", "per_table"],
                    default=DEFAULT.explicit_tables_multiplicity)
    ns = ap.parse_args(argv)
    opts = _options_from_args(ns)
    rc = 0
    for f in ns.files:
        codes = diagnose_path(f, opts)
        print(json.dumps({"file": str(f), "valid": not codes, "codes": codes}))
        rc |= bool(codes)
    return rc


if __name__ == "__main__":
    sys.exit(main())
