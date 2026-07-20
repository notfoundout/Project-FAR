#!/usr/bin/env python3
"""Executable reference algorithms for the S_core W0 normalization kernel.

This module corroborates the project-authored mathematical proof on finite
fixtures. It is not a proof assistant development and makes no FARA adequacy
claim.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
import json
from typing import Iterable, Mapping

AXES = ("P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8I")


@dataclass(frozen=True)
class RelationFact:
    name: str
    args: tuple[str, ...]


@dataclass(frozen=True)
class FiniteSourceContract:
    nodes: tuple[str, ...]
    sorts: tuple[tuple[str, str], ...]
    relations: tuple[RelationFact, ...]
    references: tuple[tuple[str, tuple[str, ...]], ...]
    material_seed: tuple[str, ...]
    axis_tags: tuple[tuple[str, tuple[str, ...]], ...]

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "FiniteSourceContract":
        nodes_raw = data.get("nodes")
        sorts_raw = data.get("sorts")
        relations_raw = data.get("relations")
        references_raw = data.get("references")
        seed_raw = data.get("material_seed")
        tags_raw = data.get("axis_tags")
        if not isinstance(nodes_raw, list) or not all(isinstance(x, str) for x in nodes_raw):
            raise ValueError("nodes must be a list of strings")
        if len(nodes_raw) != len(set(nodes_raw)):
            raise ValueError("nodes must be unique")
        if not isinstance(sorts_raw, dict):
            raise ValueError("sorts must be an object")
        if not isinstance(relations_raw, list):
            raise ValueError("relations must be a list")
        if not isinstance(references_raw, dict):
            raise ValueError("references must be an object")
        if not isinstance(seed_raw, list) or not all(isinstance(x, str) for x in seed_raw):
            raise ValueError("material_seed must be a list of strings")
        if not isinstance(tags_raw, dict):
            raise ValueError("axis_tags must be an object")

        relations: list[RelationFact] = []
        for item in relations_raw:
            if (
                not isinstance(item, list)
                or len(item) != 2
                or not isinstance(item[0], str)
                or not isinstance(item[1], list)
                or not all(isinstance(x, str) for x in item[1])
            ):
                raise ValueError("each relation must be [name, [arguments]]")
            relations.append(RelationFact(item[0], tuple(item[1])))

        references: list[tuple[str, tuple[str, ...]]] = []
        for node, targets in references_raw.items():
            if not isinstance(node, str) or not isinstance(targets, list) or not all(isinstance(x, str) for x in targets):
                raise ValueError("references must map strings to string lists")
            references.append((node, tuple(targets)))

        tags: list[tuple[str, tuple[str, ...]]] = []
        for axis in AXES:
            values = tags_raw.get(axis)
            if not isinstance(values, list) or not all(isinstance(x, str) for x in values):
                raise ValueError(f"axis_tags.{axis} must be a list of strings")
            tags.append((axis, tuple(values)))
        unexpected_axes = set(tags_raw) - set(AXES)
        if unexpected_axes:
            raise ValueError(f"unexpected axes: {sorted(unexpected_axes)}")

        contract = cls(
            nodes=tuple(nodes_raw),
            sorts=tuple(sorted((str(k), str(v)) for k, v in sorts_raw.items())),
            relations=tuple(relations),
            references=tuple(sorted(references)),
            material_seed=tuple(seed_raw),
            axis_tags=tuple(tags),
        )
        contract.validate()
        return contract

    def sort_map(self) -> dict[str, str]:
        return dict(self.sorts)

    def reference_map(self) -> dict[str, tuple[str, ...]]:
        return dict(self.references)

    def tag_map(self) -> dict[str, tuple[str, ...]]:
        return dict(self.axis_tags)

    def validate(self) -> None:
        node_set = set(self.nodes)
        sort_map = self.sort_map()
        if set(sort_map) != node_set:
            missing = sorted(node_set - set(sort_map))
            extra = sorted(set(sort_map) - node_set)
            raise ValueError(f"sort declarations must exactly cover nodes; missing={missing} extra={extra}")
        for node, targets in self.references:
            if node not in node_set:
                raise ValueError(f"undeclared reference source: {node}")
            for target in targets:
                if target not in node_set:
                    raise ValueError(f"undeclared reference endpoint: {target}")
        for fact in self.relations:
            for arg in fact.args:
                if arg not in node_set:
                    raise ValueError(f"undeclared relation endpoint: {arg}")
        for node in self.material_seed:
            if node not in node_set:
                raise ValueError(f"undeclared material seed: {node}")
        if len(self.material_seed) != len(set(self.material_seed)):
            raise ValueError("material_seed must not contain duplicates")
        for axis, tagged in self.axis_tags:
            if axis not in AXES:
                raise ValueError(f"unknown axis: {axis}")
            for node in tagged:
                if node not in node_set:
                    raise ValueError(f"undeclared axis-tag node: {node}")

    def closure(self, seeds: Iterable[str] | None = None) -> frozenset[str]:
        reference_map = self.reference_map()
        start = tuple(self.material_seed if seeds is None else seeds)
        unknown = set(start) - set(self.nodes)
        if unknown:
            raise ValueError(f"closure seed contains undeclared nodes: {sorted(unknown)}")
        visited = set(start)
        pending = list(start)
        while pending:
            node = pending.pop()
            for target in reference_map.get(node, ()):  # validation guarantees declaration
                if target not in visited:
                    visited.add(target)
                    pending.append(target)
        return frozenset(visited)

    def reduct_nodes(self, axis: str) -> frozenset[str]:
        if axis not in AXES:
            raise ValueError(f"unknown axis: {axis}")
        material = self.closure()
        axis_seed = material.intersection(self.tag_map()[axis])
        return self.closure(axis_seed).intersection(material) if axis_seed else frozenset()

    def applicable_axes(self) -> tuple[str, ...]:
        return tuple(axis for axis in AXES if self.reduct_nodes(axis))

    def renamed(self, mapping: Mapping[str, str]) -> "FiniteSourceContract":
        if set(mapping) != set(self.nodes):
            raise ValueError("renaming must be total on the node carrier")
        images = list(mapping.values())
        if len(images) != len(set(images)):
            raise ValueError("renaming must be injective")
        sort_map = self.sort_map()
        target_sort_by_name: dict[str, str] = {}
        for old, new in mapping.items():
            old_sort = sort_map[old]
            inferred = _infer_fixture_sort(new)
            if inferred is not None and inferred != old_sort:
                raise ValueError("renaming must preserve sorts")
            target_sort_by_name[new] = old_sort
        return FiniteSourceContract(
            nodes=tuple(mapping[node] for node in self.nodes),
            sorts=tuple(sorted(target_sort_by_name.items())),
            relations=tuple(RelationFact(fact.name, tuple(mapping[arg] for arg in fact.args)) for fact in self.relations),
            references=tuple(sorted((mapping[node], tuple(mapping[target] for target in targets)) for node, targets in self.references)),
            material_seed=tuple(mapping[node] for node in self.material_seed),
            axis_tags=tuple((axis, tuple(mapping[node] for node in tagged)) for axis, tagged in self.axis_tags),
        )

    def canonical_code(self) -> str:
        sort_map = self.sort_map()
        groups: dict[str, list[str]] = {}
        for node in self.nodes:
            groups.setdefault(sort_map[node], []).append(node)
        ordered_sorts = sorted(groups)
        per_sort_orders = [list(permutations(sorted(groups[sort_name]))) for sort_name in ordered_sorts]
        codes: list[str] = []
        for chosen_orders in product(*per_sort_orders):
            mapping: dict[str, str] = {}
            for sort_name, ordering in zip(ordered_sorts, chosen_orders):
                for index, node in enumerate(ordering):
                    mapping[node] = f"{sort_name}:{index}"
            codes.append(self._code_under(mapping, ordered_sorts, groups))
        if not codes:
            raise ValueError("canonicalization requires a finite carrier")
        return min(codes)

    def _code_under(self, mapping: Mapping[str, str], ordered_sorts: list[str], groups: Mapping[str, list[str]]) -> str:
        payload = {
            "sort_sizes": [[sort_name, len(groups[sort_name])] for sort_name in ordered_sorts],
            "relations": sorted([fact.name, [mapping[arg] for arg in fact.args]] for fact in self.relations),
            "references": sorted([mapping[node], sorted(mapping[target] for target in targets)] for node, targets in self.references),
            "material_seed": sorted(mapping[node] for node in self.material_seed),
            "axis_tags": [[axis, sorted(mapping[node] for node in tagged)] for axis, tagged in self.axis_tags],
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _infer_fixture_sort(name: str) -> str | None:
    prefixes = {
        "event_": "event",
        "state_": "state",
        "commitment_": "commitment",
        "stake_": "stake",
        "alternative_": "alternative",
        "ground_": "ground",
        "transition_": "transition",
        "consequence_": "consequence",
        "history_": "history",
        "provenance_": "provenance",
    }
    for prefix, sort_name in prefixes.items():
        if name.startswith(prefix):
            return sort_name
    return None


def transport_set(values: Iterable[str], mapping: Mapping[str, str]) -> frozenset[str]:
    return frozenset(mapping[value] for value in values)


def load_fixture_set(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("schema_version") != "1.0":
        raise ValueError("fixture schema_version must equal 1.0")
    return data
