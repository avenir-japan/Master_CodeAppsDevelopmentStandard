"""Markdown 見出しリンク検証の回帰テスト。"""

import tempfile
import unittest
from pathlib import Path

from validate_skill import Report, scan_heading_links, validate_skill


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


class ScriptDirectoryTests(unittest.TestCase):
    def test_scriptless_skill_does_not_warn(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "example"
            skill.mkdir()
            (skill / "references").mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: example\ndescription: Example\ncategory: guide\ntriggers:\n  - example\n---\n"
                "# Example\nNo scripts are used.\n",
                encoding="utf-8",
            )
            self.assertEqual([], validate_skill(skill).warnings)

    def test_missing_referenced_script_directory_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "example"
            skill.mkdir()
            (skill / "references").mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: example\ndescription: Example\ncategory: guide\ntriggers:\n  - example\n---\n"
                "# Example\nRun [checker](scripts/check.py).\n",
                encoding="utf-8",
            )
            self.assertTrue(any("scripts/ が無い" in w for w in validate_skill(skill).warnings))

    def test_command_reference_warns_but_external_script_does_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "example"
            skill.mkdir()
            (skill / "references").mkdir()
            doc = skill / "SKILL.md"
            doc.write_text(
                "---\nname: example\ndescription: Example\ncategory: guide\ntriggers:\n  - example\n---\n"
                "```powershell\npython ../standard/scripts/check.py\n```\n",
                encoding="utf-8",
            )
            self.assertEqual([], validate_skill(skill).warnings)
            doc.write_text(doc.read_text(encoding="utf-8") + "```powershell\npython scripts/check.py\n```\n", encoding="utf-8")
            self.assertTrue(any("scripts/ が無い" in w for w in validate_skill(skill).warnings))

    def test_referenced_script_directory_present_does_not_warn(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "example"
            skill.mkdir()
            (skill / "references").mkdir()
            (skill / "scripts").mkdir()
            (skill / "scripts" / "check.py").write_text("", encoding="utf-8")
            (skill / "SKILL.md").write_text(
                "---\nname: example\ndescription: Example\ncategory: guide\ntriggers:\n  - example\n---\n"
                "# Example\nRun [checker](scripts/check.py).\n",
                encoding="utf-8",
            )
            self.assertEqual([], validate_skill(skill).warnings)


if __name__ == "__main__":
    unittest.main()
