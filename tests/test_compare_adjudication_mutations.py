from __future__ import annotations

import copy
import unittest

from mechanization.far_mechanization.compare_adjudication import (
    ADJUDICATION_SCHEMA,
    PACKAGE_SCHEMA,
    InterfaceError,
    adjudicate,
    artifact_sha256,
    compare_packages,
    normalize_package,
)


def base_package(package_id: str, statement: str) -> dict:
    return {
        "schema": PACKAGE_SCHEMA,
        "package_id": package_id,
        "subject_id": "subject-001",
        "claims": [
            {
                "claim_id": "claim-001",
                "statement": statement,
                "status": "observed",
                "support": ["evidence-001"],
                "assumptions": [],
                "contradicts": [],
                "boundaries": ["bounded observation"],
            }
        ],
        "boundaries": ["No truth certification"],
        "metadata": {},
    }


class PackageMutationCampaign(unittest.TestCase):
    def test_registered_package_mutations_are_killed(self) -> None:
        original = base_package("left", "A")

        def delete_schema(value):
            value.pop("schema")

        def alter_schema(value):
            value["schema"] = "far-evidence-package/9.9"

        def inject_field(value):
            value["winner"] = "left"

        def duplicate_claim(value):
            value["claims"].append(copy.deepcopy(value["claims"][0]))

        def unsupported_status(value):
            value["claims"][0]["status"] = "certain"

        def nested_metadata(value):
            value["metadata"]["hidden"] = {"score": 1}

        def dangling_contradiction(value):
            value["claims"][0]["contradicts"] = ["missing"]

        def duplicate_support(value):
            value["claims"][0]["support"].append("evidence-001")

        mutations = {
            "delete-schema": delete_schema,
            "alter-schema": alter_schema,
            "inject-field": inject_field,
            "duplicate-claim": duplicate_claim,
            "unsupported-status": unsupported_status,
            "nested-metadata": nested_metadata,
            "dangling-contradiction": dangling_contradiction,
            "duplicate-support": duplicate_support,
        }
        survivors = []
        for name, mutate in mutations.items():
            candidate = copy.deepcopy(original)
            mutate(candidate)
            try:
                normalize_package(candidate)
            except InterfaceError:
                continue
            survivors.append(name)
        self.assertEqual(survivors, [], f"surviving package mutations: {survivors}")


class AdjudicationMutationCampaign(unittest.TestCase):
    def test_registered_adjudication_mutations_are_killed(self) -> None:
        comparison = compare_packages(
            base_package("left", "A"),
            base_package("right", "Not A"),
        )
        finding_id = comparison["findings"][0]["finding_id"]
        original = {
            "schema": ADJUDICATION_SCHEMA,
            "comparison_sha256": artifact_sha256(comparison),
            "adjudicator": "reviewer-001",
            "decisions": [
                {
                    "finding_id": finding_id,
                    "disposition": "unresolved",
                    "rationale": "Bounded evidence is insufficient.",
                    "support": [],
                    "limitations": ["No independent replication"],
                }
            ],
            "dissent": [],
            "metadata": {},
        }

        def alter_hash(value):
            value["comparison_sha256"] = "f" * 64

        def delete_decision(value):
            value["decisions"] = []

        def duplicate_decision(value):
            value["decisions"].append(copy.deepcopy(value["decisions"][0]))

        def alter_finding(value):
            value["decisions"][0]["finding_id"] = "finding-unknown"

        def truth_disposition(value):
            value["decisions"][0]["disposition"] = "true"

        def inject_field(value):
            value["certified"] = True

        def delete_rationale(value):
            value["decisions"][0]["rationale"] = ""

        def forge_id(value):
            value["adjudication_id"] = "adjudication-forged"

        mutations = {
            "alter-comparison-hash": alter_hash,
            "delete-decision": delete_decision,
            "duplicate-decision": duplicate_decision,
            "unknown-finding": alter_finding,
            "truth-disposition": truth_disposition,
            "inject-field": inject_field,
            "delete-rationale": delete_rationale,
            "forge-id": forge_id,
        }
        survivors = []
        for name, mutate in mutations.items():
            candidate = copy.deepcopy(original)
            mutate(candidate)
            try:
                adjudicate(comparison, candidate)
            except InterfaceError:
                continue
            survivors.append(name)
        self.assertEqual(survivors, [], f"surviving adjudication mutations: {survivors}")


if __name__ == "__main__":
    unittest.main()
