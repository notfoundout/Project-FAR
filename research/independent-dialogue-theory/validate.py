#!/usr/bin/env python3
"""Validate the independent dialogue-theory closure report."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    seals = load("SEALS.json")
    for seal in seals["ordering"]:
        path = ROOT / seal["object"]
        require(path.is_file(), f"missing sealed object: {path}")
        require(sha256(path) == seal["sha256"], f"seal mismatch: {seal['object']}")

    corpus = load("corpus/CORPUS-MANIFEST.json")
    for record in corpus["files"]:
        path = ROOT / "corpus" / record["path"]
        require(path.is_file(), f"missing corpus file: {record['path']}")
        require(sha256(path) == record["sha256"], f"corpus hash mismatch: {record['id']}")
        require(path.stat().st_size == record["bytes"], f"corpus size mismatch: {record['id']}")
        require(path.read_bytes().count(b"\n") == record["lines"], f"corpus LF-line mismatch: {record['id']}")

    source = load("SOURCE-MANIFEST.json")
    require(len(source["target_documents"]) == 8, "target source count must be 8")
    require(len(source["pi0_bib_v1_recovered_documents"]) == 11, "recovered PI0 body count must be 11")
    require({row["label"] for row in source["pi0_bib_v1_recovered_documents"]} == {1, 2, 3, 4, 5, 6, 7, 10, 11, 12}, "PI0 missing-label coverage mismatch")

    u0 = load("U0.json")
    require(u0["count"] == 88 == len(u0["items"]), "U0 count mismatch")
    require([row["id"] for row in u0["items"]] == [f"u{i:03d}" for i in range(1, 89)], "U0 IDs/order mismatch")
    per_target = Counter(row["target"] for row in u0["items"])
    require(per_target == Counter({f"S{i}": 8 for i in range(1, 12)}), "U0 per-target count mismatch")
    require(all(row["verbatim_designation"] and row["locator"] and row["Ax"] for row in u0["items"]), "incomplete U0 K4 metadata")

    wstar = load("W-STAR.json")
    mandatory = wstar["mandatory_cells"]
    require(len(mandatory) == 176, "mandatory matrix count mismatch")
    require(len({(row["target"], row["item"]) for row in mandatory}) == 176, "duplicate mandatory cell")
    require({row["target"] for row in mandatory} == {"S1", "S2"}, "mandatory target mismatch")
    require(all(row["B1"] in {"YES", "NO", "OPEN"} and row["B2"] in {"YES", "NO", "OPEN"} for row in mandatory), "blank/invalid mandatory status")

    secondary = wstar["secondary_stratum"]["cells"]
    require(len(secondary) == 792, "secondary population mismatch")
    require([row["rank"] for row in secondary] == list(range(1, 793)), "secondary ranks mismatch")
    require(len({(row["target"], row["item"]) for row in secondary}) == 792, "duplicate secondary cell")
    require(sum(row["selected_B1"] for row in secondary) == 100, "B1 traversal mismatch")
    require(sum(row["selected_B2"] for row in secondary) == 400, "B2 traversal mismatch")
    require(all(row["B1"] in {"YES", "NO", "OPEN"} and row["B2"] in {"YES", "NO", "OPEN"} for row in secondary), "blank/invalid secondary status")

    global_rows = mandatory + secondary
    counts = Counter(row["B2"] for row in global_rows)
    require(counts == Counter({"OPEN": 909, "YES": 59}), f"global B2 mismatch: {counts}")
    require(wstar["global_counts"]["cell_population"] == 968, "global cell population mismatch")

    calibration = wstar["fragments"]["calibration"]
    native = wstar["fragments"]["native"]
    require(len(calibration) == 89 and len(native) == 88, "fragment count mismatch")
    require(all(row["status"] in {"JOINT-YES", "JOINT-NO", "JOINT-OPEN"} for row in calibration + native), "invalid joint status")
    require(Counter(row["status"] for row in calibration) == Counter({"JOINT-OPEN": 86, "JOINT-YES": 3}), "calibration joint counts mismatch")
    require(Counter(row["status"] for row in native) == Counter({"JOINT-OPEN": 86, "JOINT-YES": 2}), "native joint counts mismatch")
    require([row["id"] for row in wstar["joint_profiles"]] == ["J0", "J-u058", "J-u059", "J-star"], "joint profile set mismatch")
    require(len(wstar["frontiers"]["open_frontier"]) == 86, "OPEN frontier count mismatch")
    require(wstar["frontiers"]["proved_failure_frontier_JOINT_NO"] == [], "unexpected proved failure")

    frames = load("FRAMES.json")
    require(frames["generated_before_common_theory"] is True, "frame ordering flag absent")
    require(len(frames["frames"]) == 6, "frame count mismatch")
    require(all("irreflex" not in json.dumps(row["Gamma"]).lower() for row in frames["frames"]), "content leaked into frame")

    state = load("STATE.json")
    require(state["sealed_objects"]["u0_E1_sha256"] == sha256(ROOT / "U0.json"), "STATE U0 hash mismatch")
    require(state["sealed_objects"]["w_star_sha256"] == sha256(ROOT / "W-STAR.json"), "STATE W-star hash mismatch")
    require(state["sealed_objects"]["frames_sha256"] == sha256(ROOT / "FRAMES.json"), "STATE frame hash mismatch")
    terminal = (ROOT / "TERMINAL-REPORT.md").read_text(encoding="utf-8")
    require("The dialogue-built theory is INTERNALLY TERMINAL—THEORY UNRESOLVED" in terminal, "exact terminal sentence absent")

    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for markdown in ROOT.rglob("*.md"):
        if "corpus" in markdown.parts:
            continue
        for raw in link_re.findall(markdown.read_text(encoding="utf-8")):
            target = raw.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            require((markdown.parent / target).exists(), f"broken relative link in {markdown.name}: {raw}")

    print("PASS: corpus, seals, sources, U0, W-star, fragments, frames, state, terminal verdict, and links")


if __name__ == "__main__":
    main()
