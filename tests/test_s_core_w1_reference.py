from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from tools.s_core_w1_reference import (
    DIRECT_AXES,
    W1Error,
    canonical_json,
    construct_target,
    structural_digest,
    validate_source,
    verify_all,
    verify_axis,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "theory/evaluation/s-core-w1-reference-fixtures.json"


class SCoreW1ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.source = cls.data["source"]

    def build(self):
        return construct_target(copy.deepcopy(self.source))

    def test_fixture_schema_and_direct_axis_set(self) -> None:
        self.assertEqual(self.data["schema_version"], "1.0")
        self.assertEqual(self.data["fixture_set_id"], "SCORE-W1-FIXTURES-001")
        self.assertEqual(DIRECT_AXES, ("P1", "P2", "P3", "P4", "P6", "P8I"))
        validate_source(self.source)

    def test_baseline_constructs_and_verifies_every_axis(self) -> None:
        target, correspondence = self.build()
        self.assertTrue(verify_all(self.source, target, correspondence))
        for axis in DIRECT_AXES:
            self.assertTrue(verify_axis(self.source, target, correspondence, axis), axis)

    def test_fara_object_representation_and_structure_separation(self) -> None:
        target, _ = self.build()
        object_ids = {item["id"] for item in target["U"]}
        representation_ids = {item["id"] for item in target["Rep"]}
        self.assertTrue(object_ids)
        self.assertTrue(representation_ids)
        self.assertTrue(object_ids.isdisjoint(representation_ids))
        self.assertEqual(len(target["U"]), len(target["Rep"]))
        self.assertEqual(len(target["Pi"]), len(target["U"]))
        self.assertEqual(set(target["S"]["representations"]), representation_ids)
        for object_id, rep_id in target["R"]["represented_by"]:
            self.assertIn(object_id, object_ids)
            self.assertIn(rep_id, representation_ids)

    def test_source_element_map_is_injective_and_shared_images_are_reused(self) -> None:
        target, correspondence = self.build()
        for axis in DIRECT_AXES:
            phi = correspondence[axis]["phi"]
            self.assertEqual(len(phi), len(set(phi.values())))
        self.assertEqual(
            correspondence["P2"]["phi"]["commitment:c1"],
            correspondence["P4"]["phi"]["commitment:c1"],
        )
        self.assertEqual(
            correspondence["P4"]["phi"]["ground:g1"],
            correspondence["P8I"]["phi"]["ground:g1"],
        )
        self.assertTrue(verify_all(self.source, target, correspondence))

    def test_relation_and_attribute_namespaces_are_independent(self) -> None:
        source = {
            "axes": {
                "P1": {
                    "elements": [
                        {"id": "x", "sort": "thing"},
                        {"id": "y", "sort": "thing"},
                    ],
                    "relations": [{"role": "same.id", "args": ["x", "y"]}],
                    "attributes": [{"owner": "x", "role": "same.id", "value": "v"}],
                }
            }
        }
        target, correspondence = construct_target(source)
        self.assertNotEqual(
            correspondence["P1"]["rho"]["same.id"]["role_object"],
            correspondence["P1"]["alpha"]["same.id"]["role_object"],
        )
        self.assertTrue(verify_axis(source, target, correspondence, "P1"))

    def test_spurious_relation_is_rejected_by_reflection(self) -> None:
        target, correspondence = self.build()
        mutated = copy.deepcopy(target)
        support = correspondence["P4"]["rho"]["P4.support"]
        occurrence = "mutation:spurious-support"
        positions = {
            item["payload"]: item["id"]
            for item in mutated["U"]
            if item["kind"] == "position_code"
        }
        mutated["R"]["in_axis"].append([occurrence, "axis:P4"])
        mutated["R"]["occurrence_role"].append([occurrence, support["role_object"]])
        mutated["R"]["argument"].append([
            occurrence, positions[1], correspondence["P4"]["phi"]["ground:g2"]
        ])
        mutated["R"]["argument"].append([
            occurrence, positions[2], correspondence["P4"]["phi"]["commitment:c1"]
        ])
        self.assertFalse(verify_axis(self.source, mutated, correspondence, "P4"))

    def test_collapsed_source_images_are_rejected(self) -> None:
        target, correspondence = self.build()
        mutated = copy.deepcopy(correspondence)
        mutated["P3"]["phi"]["alternative:b"] = mutated["P3"]["phi"]["alternative:a"]
        self.assertFalse(verify_axis(self.source, target, mutated, "P3"))

    def test_support_and_defeat_role_collapse_is_rejected(self) -> None:
        target, correspondence = self.build()
        mutated = copy.deepcopy(correspondence)
        mutated["P4"]["rho"]["P4.defeat"]["role_object"] = (
            mutated["P4"]["rho"]["P4.support"]["role_object"]
        )
        self.assertFalse(verify_axis(self.source, target, mutated, "P4"))

    def test_missing_live_alternative_is_rejected(self) -> None:
        target, correspondence = self.build()
        mutated = copy.deepcopy(target)
        role_object = correspondence["P3"]["rho"]["P3.live_alternative"]["role_object"]
        live_occurrences = [
            occurrence
            for occurrence, role in mutated["R"]["occurrence_role"]
            if role == role_object and [occurrence, "axis:P3"] in mutated["R"]["in_axis"]
        ]
        self.assertEqual(len(live_occurrences), 2)
        removed = live_occurrences[0]
        mutated["R"]["occurrence_role"] = [
            fact for fact in mutated["R"]["occurrence_role"] if fact[0] != removed
        ]
        self.assertFalse(verify_axis(self.source, mutated, correspondence, "P3"))

    def test_consequence_role_loss_is_rejected(self) -> None:
        target, correspondence = self.build()
        mutated = copy.deepcopy(target)
        descriptor = correspondence["P6"]["alpha"]["P6.consequence_role"]
        occurrences = [
            occurrence
            for occurrence, role in mutated["R"]["attribute_role"]
            if role == descriptor["role_object"] and [occurrence, "axis:P6"] in mutated["R"]["in_axis"]
        ]
        self.assertEqual(len(occurrences), 1)
        removed = occurrences[0]
        mutated["R"]["attribute_role"] = [
            fact for fact in mutated["R"]["attribute_role"] if fact[0] != removed
        ]
        self.assertFalse(verify_axis(self.source, mutated, correspondence, "P6"))

    def test_evidential_upgrade_is_rejected(self) -> None:
        target, correspondence = self.build()
        mutated = copy.deepcopy(target)
        descriptor = correspondence["P8I"]["alpha"]["P8I.evidence_status"]
        commitment_image = correspondence["P8I"]["phi"]["commitment:c1"]
        owners = {occ: owner for occ, owner in mutated["R"]["attribute_owner"]}
        roles = {occ: role for occ, role in mutated["R"]["attribute_role"]}
        occurrence = next(
            occ for occ, owner in owners.items()
            if owner == commitment_image and roles.get(occ) == descriptor["role_object"]
        )
        stronger_id = "mutation:value:formally_proved"
        for fact in mutated["R"]["attribute_value"]:
            if fact[0] == occurrence:
                fact[1] = stronger_id
        self.assertFalse(verify_axis(self.source, mutated, correspondence, "P8I"))

    def test_display_label_alpha_renaming_does_not_change_structure(self) -> None:
        renamed = copy.deepcopy(self.source)
        for reduct in renamed["axes"].values():
            for element in reduct.get("elements", []):
                element["label"] = f"renamed::{element.get('label', element['id'])}"
            for relation in reduct.get("relations", []):
                relation["display_role"] = f"renamed::{relation.get('display_role', relation['role'])}"
            for attribute in reduct.get("attributes", []):
                attribute["display_role"] = f"renamed::{attribute.get('display_role', attribute['role'])}"
        target_a, corr_a = construct_target(self.source)
        target_b, corr_b = construct_target(renamed)
        self.assertEqual(structural_digest(target_a), structural_digest(target_b))
        self.assertEqual(canonical_json(corr_a), canonical_json(corr_b))
        self.assertTrue(verify_all(renamed, target_b, corr_b))

    def test_shared_element_sort_change_is_rejected(self) -> None:
        malformed = copy.deepcopy(self.source)
        item = next(x for x in malformed["axes"]["P4"]["elements"] if x["id"] == "commitment:c1")
        item["sort"] = "ground"
        with self.assertRaisesRegex(W1Error, "changes sort"):
            validate_source(malformed)


if __name__ == "__main__":
    unittest.main()
