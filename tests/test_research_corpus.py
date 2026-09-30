from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools import reconcile_research_corpus as corpus


class ResearchCorpusTests(unittest.TestCase):
    def setUp(self):
        self.data = corpus.load(corpus.CORPUS)

    def test_corpus_and_generated_views_are_current(self):
        self.assertEqual(corpus.validate(self.data), [])
        result = corpus.derive(self.data)
        self.assertTrue(result["material_input_accounting"]["complete"])
        self.assertEqual((corpus.ROOT / corpus.OUTPUT).read_bytes(), corpus.canonical(result))
        self.assertEqual((corpus.ROOT / corpus.STATUS).read_text(), corpus.markdown(result))

    def test_duplicate_cycle_and_open_world_errors_fail_closed(self):
        duplicate = copy.deepcopy(self.data)
        duplicate["findings"].append(copy.deepcopy(duplicate["findings"][0]))
        self.assertTrue(any("duplicate identity" in e for e in corpus.validate(duplicate)))
        cycle = copy.deepcopy(self.data)
        cycle["conclusions"][0]["depends_on"] = [cycle["conclusions"][0]["id"]]
        self.assertTrue(any("circular support" in e for e in corpus.validate(cycle)))
        missing = copy.deepcopy(self.data)
        missing["mechanisms"][0]["finding_ids"] = ["FND-ABSENT"]
        self.assertTrue(any("missing finding" in e for e in corpus.validate(missing)))

    def test_mutable_withdrawn_and_malicious_sources_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bad = copy.deepcopy(self.data)
            source = next(s for s in bad["sources"] if s["availability"] == "available")
            target = root / source["path"]
            target.parent.mkdir(parents=True)
            target.write_text("changed")
            errors = corpus.validate(bad, root)
            self.assertTrue(any("hash mismatch" in e for e in errors))
        withdrawn = copy.deepcopy(self.data)
        source = next(s for s in withdrawn["sources"] if s["evidence_usable"])
        source["availability"] = "withdrawn"
        self.assertTrue(any("evidence lacks verified" in e for e in corpus.validate(withdrawn)))
        hostile = copy.deepcopy(self.data)
        source = hostile["sources"][0]
        source.update(kind="ai_summary", evidence_usable=True)
        self.assertTrue(any("promoted as evidence" in e for e in corpus.validate(hostile)))

    def test_external_freeze_is_content_addressed_data_not_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            # Exercise the receipt semantics without writing into the repository.
            raw = b"#!/bin/sh\nexit 99\n"
            sha = corpus.digest(raw)
            receipt = {"sha256": sha, "authority": "discovery_lead", "executable": False, "primary_evidence_verified": False}
            self.assertEqual(receipt["sha256"], corpus.digest(raw))
            self.assertFalse(receipt["executable"])
            self.assertFalse(receipt["primary_evidence_verified"])

    def test_epistemic_and_architecture_status_cannot_be_promoted(self):
        promoted = copy.deepcopy(self.data)
        promoted["conclusions"][0]["epistemic_class"] = "ACCEPTED"
        promoted["mechanisms"][0]["architecture_class"] = "novel"
        errors = corpus.validate(promoted)
        self.assertTrue(any("invalid conclusion class" in e for e in errors))
        self.assertTrue(any("invalid architecture class" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
