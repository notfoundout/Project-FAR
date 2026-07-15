from __future__ import annotations

from collections import Counter
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import detect_research_gaps
import repository_alerts


class LiveGapCountTests(unittest.TestCase):
    def test_live_gap_counts_equal_detect_gaps_severity_counts(self) -> None:
        expected = Counter(str(gap.get("severity", "")).title() for gap in detect_research_gaps.detect_gaps())
        self.assertEqual(repository_alerts.gap_counts(), expected)

    def test_gap_counts_does_not_read_markdown_report(self) -> None:
        original_read_text = Path.read_text

        def guarded_read_text(path: Path, *args, **kwargs):
            if Path(path) == repository_alerts.GAPS:
                raise AssertionError("gap_counts read the generated Markdown report")
            return original_read_text(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", guarded_read_text):
            self.assertEqual(repository_alerts.gap_counts()["Critical"], Counter(str(gap.get("severity", "")).title() for gap in detect_research_gaps.detect_gaps())["Critical"])

    def test_stale_or_missing_report_does_not_change_live_counts(self) -> None:
        expected = repository_alerts.gap_counts()
        with mock.patch.object(repository_alerts, "GAPS", ROOT / "does-not-exist-report.md"):
            self.assertEqual(repository_alerts.gap_counts(), expected)
        original_read_text = Path.read_text

        def stale_report_guard(path: Path, *args, **kwargs):
            if Path(path) == repository_alerts.GAPS:
                raise AssertionError("stale report read")
            return original_read_text(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", stale_report_guard):
            self.assertEqual(repository_alerts.gap_counts(), expected)


if __name__ == "__main__":
    unittest.main()
