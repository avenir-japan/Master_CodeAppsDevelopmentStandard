"""Markdown 見出しリンク検証の回帰テスト。"""

import tempfile
import unittest
from pathlib import Path

from validate_skill import Report, scan_heading_links


class HeadingLinkTests(unittest.TestCase):
    def test_valid_links_and_code_fence_examples(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "target.md").write_text("# Teams 1:1\n## 項目（必須）\n## 項目（必須）\n", encoding="utf-8")
            (root / "source.md").write_text(
                "[one](target.md#teams-11)\n"
                "[two](target.md#項目必須-1)\n"
                "```markdown\n[example](target.md#存在しない)\n```\n",
                encoding="utf-8",
            )
            report = Report("test")
            scan_heading_links(root, report)
            self.assertEqual([], report.errors)

    def test_missing_file_and_missing_heading(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "target.md").write_text("# Actual\n", encoding="utf-8")
            (root / "source.md").write_text(
                "[old](target.md#old)\n[missing](gone.md#heading)\n",
                encoding="utf-8",
            )
            report = Report("test")
            scan_heading_links(root, report)
            self.assertEqual(2, len(report.errors))
            self.assertIn("見出しリンクがない", report.errors[0])
            self.assertIn("リンク先ファイルがない", report.errors[1])


if __name__ == "__main__":
    unittest.main()
