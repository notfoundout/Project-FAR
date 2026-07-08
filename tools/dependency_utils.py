#!/usr/bin/env python3
"""Shared dependency-registry helpers."""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "theory/dependencies/dependency-registry.yaml"
SCHEMA = ROOT / "theory/dependencies/dependency-schema.yaml"


def load_registry() -> dict:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    return data if isinstance(data, dict) else {}


def dependencies() -> list[dict]:
    values = load_registry().get("dependencies") or []
    return values if isinstance(values, list) else []


def node_id(value: str) -> str:
    return str(value)
