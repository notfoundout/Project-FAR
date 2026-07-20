from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from s_core_w3_reference import (
    W3Error, canonical_json, component_view, construct_witness,
    cross_axis_coherent, recover_target, semantic_agreement,
    structural_digest, validate_package, validate_source, verify_witness,
)

FIXTURE = Path(__file__).with_name("../theory/evaluation/s-core-w3-reference-fixtures.json").resolve()


def load_source():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["source"]


def rename_source(source, mapping):
    value = copy.deepcopy(source)
    def r(x): return mapping.get(str(x), str(x))
    for item in value["carriers"]: item["id"] = r(item["id"])
    for axis in value["axes"].values():
        axis["members"] = [r(x) for x in axis["members"]]
        for item in axis["relations"]: item["id"] = r(item["id"]); item["args"] = [r(x) for x in item["args"]]
        for item in axis["attributes"]: item["id"] = r(item["id"]); item["owner"] = r(item["owner"])
    d = value["dynamics"]
    for item in d["rules"]: item["id"] = r(item["id"])
    for item in d["rule_versions"]: item["id"] = r(item["id"]); item["rule"] = r(item["rule"])
    for item in d["states"]:
        item["id"] = r(item["id"]); item["active_rule_versions"] = [r(x) for x in item["active_rule_versions"]]; item["commitments"] = {r(k): v for k, v in item["commitments"].items()}
    for item in d["transitions"]:
        item["id"] = r(item["id"]); item["from"] = r(item["from"]); item["to"] = r(item["to"])
        if item.get("rule_version") is not None: item["rule_version"] = r(item["rule_version"])
    h = d["history"]
    for item in h["events"]:
        item["id"] = r(item["id"]); item["state"] = r(item["state"])
        if item.get("transition") is not None: item["transition"] = r(item["transition"])
    for key in ("order", "causal", "dependency_ancestry"): h[key] = [[r(a), r(b)] for a, b in h[key]]
    for item in h["provenance"]: item["event"] = r(item["event"])
    for item in h["revisions"]:
        item["event"] = r(item["event"]); item["before_state"] = r(item["before_state"]); item["after_state"] = r(item["after_state"]); item["subject"] = r(item["subject"])
    for item in h["modifications"]:
        item["event"] = r(item["event"]); item["before_state"] = r(item["before_state"]); item["after_state"] = r(item["after_state"]); item["deactivates"] = [r(x) for x in item["deactivates"]]; item["activates"] = [r(x) for x in item["activates"]]
    for item in h["path_conditions"]: item["path"] = [r(x) for x in item["path"]]
    decomp = value["decomposition"]
    for item in decomp["components"]: item["id"] = r(item["id"]); item["members"] = [r(x) for x in item["members"]]
    for item in decomp["interfaces"]: item["id"] = r(item["id"]); item["members"] = [r(x) for x in item["members"]]; item["components"] = [r(x) for x in item["components"]]
    for item in decomp["cross_component_relations"]: item["id"] = r(item["id"]); item["args"] = [r(x) for x in item["args"]]
    return value


def translate(value, mapping):
    if isinstance(value, str): return mapping.get(value, value)
    if isinstance(value, list): return [translate(x, mapping) for x in value]
    if isinstance(value, dict): return {k: translate(v, mapping) for k, v in value.items()}
    return value


def normalize_recovered(value):
    result = copy.deepcopy(value)
    result["carriers"] = sorted(result["carriers"], key=canonical_json)
    for reduct in result["axes"].values():
        reduct["members"] = sorted(reduct["members"]); reduct["relations"] = sorted(reduct["relations"], key=canonical_json); reduct["attributes"] = sorted(reduct["attributes"], key=canonical_json)
    for state in result["dynamics"]["states"]:
        state["commitments"] = sorted(state.get("commitments", []), key=canonical_json); state["resources"] = sorted(state.get("resources", []), key=canonical_json); state["active_rule_versions"] = sorted(state.get("active_rule_versions", []))
    for transition in result["dynamics"]["transitions"]:
        for key in ("preconditions", "resource_conditions", "action_dependencies", "observation_dependencies"): transition[key] = sorted(transition.get(key, []))
    for item in result["dynamics"]["history"].get("modifications", []): item["deactivates"] = sorted(item.get("deactivates", [])); item["activates"] = sorted(item.get("activates", []))
    for key in ("rules", "rule_versions", "states", "transitions", "transition_statuses"): result["dynamics"][key] = sorted(result["dynamics"][key], key=canonical_json)
    for key in result["dynamics"]["history"]: result["dynamics"]["history"][key] = sorted(result["dynamics"]["history"][key], key=canonical_json)
    for key in ("interpretations", "value_literals", "equivalences"): result["semantics"][key] = sorted(result["semantics"][key], key=canonical_json)
    for key in result["decomposition"]: result["decomposition"][key] = sorted(result["decomposition"][key], key=canonical_json)
    result["provenance"] = sorted(result["provenance"], key=canonical_json)
    return result


class W3ReferenceTests(unittest.TestCase):
    def setUp(self): self.source = load_source(); self.package = construct_witness(self.source)
    def test_baseline_witness(self): self.assertTrue(verify_witness(self.source, self.package))
    def test_recovery_is_target_only(self):
        recovered = recover_target(self.package["A"], self.package["W"]["D"], self.package["W"]["kappa"]); modified = copy.deepcopy(self.package); modified["W"]["E"] = {}; modified["W"]["M"] = {}
        self.assertEqual(recovered, recover_target(modified["A"], modified["W"]["D"], modified["W"]["kappa"])); self.assertNotIn("source_key", canonical_json(self.package["A"]))
    def test_missing_direct_relation_is_rejected(self):
        bad = copy.deepcopy(self.package); occurrence = bad["W"]["E"]["occ:p4:support"]; bad["A"]["R"]["occurrence_role"] = [x for x in bad["A"]["R"]["occurrence_role"] if x[0] != occurrence]; self.assertFalse(verify_witness(self.source, bad))
    def test_undeclared_occurrence_is_rejected(self):
        bad = copy.deepcopy(self.package); bad["A"]["R"]["in_axis"].append(["unknown:occurrence", "axis:P4"]); self.assertFalse(verify_witness(self.source, bad))
    def test_semantic_mutation_is_rejected(self):
        bad = copy.deepcopy(self.package); subject = bad["W"]["E"]["commitment:c1"]; alternate = bad["W"]["M"]["values"][canonical_json("the supporting observation")]; next(x for x in bad["A"]["I"] if x["subject"] == subject)["denotation"] = alternate; self.assertFalse(semantic_agreement(self.source, bad)); self.assertFalse(verify_witness(self.source, bad))
    def test_shared_image_split_is_rejected(self):
        bad = copy.deepcopy(self.package); bad["W"]["E"]["commitment:c1"] = bad["W"]["E"]["commitment:c2"]; self.assertFalse(cross_axis_coherent(self.source, bad)); self.assertRaises(W3Error, validate_package, bad)
    def test_source_sort_conflict_is_rejected(self):
        bad = copy.deepcopy(self.source); next(x for x in bad["carriers"] if x["id"] == "rule:r1")["sort"] = "ground"; self.assertRaises(W3Error, validate_source, bad)
    def test_machinery_cycle_is_rejected(self):
        bad = copy.deepcopy(self.package); bad["W"]["kappa"]["edges"].append(["schema:FARA-WITNESS-1.0", "algorithm:validate-source"]); self.assertRaises(W3Error, validate_package, bad)
    def test_incomplete_machinery_is_rejected(self):
        bad = copy.deepcopy(self.package); del bad["W"]["kappa"]["field_producers"]["A.H"]; self.assertRaises(W3Error, validate_package, bad)
    def test_interface_loss_is_rejected(self):
        bad = copy.deepcopy(self.package); interface = bad["W"]["E"]["interface:commitment"]; member = bad["W"]["E"]["commitment:c1"]; bad["A"]["Res"]["interface_members"] = [x for x in bad["A"]["Res"]["interface_members"] if x != [interface, member]]; self.assertFalse(verify_witness(self.source, bad))
    def test_hidden_external_dependency_is_rejected(self):
        bad = copy.deepcopy(self.package); bad["W"]["kappa"]["external_dependencies"] = ["source-oracle"]; self.assertRaises(W3Error, validate_package, bad)
    def test_display_labels_are_not_structural(self):
        renamed = copy.deepcopy(self.source)
        for item in renamed["carriers"]: item["display_label"] = f"label::{item['id']}"
        other = construct_witness(renamed); self.assertEqual(structural_digest(self.package), structural_digest(other)); self.assertTrue(verify_witness(renamed, other))
    def test_source_isomorphism_equivariance(self):
        rename = {item_id: f"renamed::{index}" for index, item_id in enumerate(sorted(self.package["W"]["E"]), start=1)}; renamed_source = rename_source(self.source, rename); renamed_package = construct_witness(renamed_source); recovered = recover_target(self.package["A"], self.package["W"]["D"], self.package["W"]["kappa"]); renamed_recovered = recover_target(renamed_package["A"], renamed_package["W"]["D"], renamed_package["W"]["kappa"]); induced = {self.package["W"]["E"][old]: renamed_package["W"]["E"][new] for old, new in rename.items()}; self.assertEqual(normalize_recovered(translate(recovered, induced)), normalize_recovered(renamed_recovered)); self.assertTrue(verify_witness(renamed_source, renamed_package))
    def test_component_view_retains_interface_and_cross_relation(self):
        recovered = recover_target(self.package["A"], self.package["W"]["D"], self.package["W"]["kappa"]); view = component_view(recovered, self.package["W"]["E"]["component:analysis"]); self.assertIn(self.package["W"]["E"]["commitment:c1"], view["allowed"]); self.assertEqual(len(view["cross_component_relations"]), 1)
    def test_recovery_descriptor_cannot_be_replaced(self):
        bad = copy.deepcopy(self.package); bad["W"]["D"]["algorithm"] = "case_specific_decoder"; self.assertRaises(W3Error, validate_package, bad)


if __name__ == "__main__": unittest.main()
