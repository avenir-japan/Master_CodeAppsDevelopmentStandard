"""Focused tests for the pre-deployment workflow definition guard."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_flow_definition.py"
spec = importlib.util.spec_from_file_location("validate_flow_definition", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FlowDefinitionValidationTests(unittest.TestCase):
    def test_rejects_unencoded_runtime_content(self):
        definition = {"actions": [{"inputs": {"contentBase64": "@body('Get_file')"}}]}
        self.assertEqual(
            module.validate_content_base64(definition),
            ["$.actions[0].inputs.contentBase64: runtime contentBase64 must use @base64(...)"],
        )

    def test_rejects_empty_content(self):
        self.assertEqual(
            module.validate_content_base64({"contentBase64": " "}),
            ["$.contentBase64: contentBase64 must be a non-empty string"],
        )

    def test_accepts_encoded_content_and_unrelated_actions(self):
        definition = {"actions": [{"inputs": {"contentBase64": "@base64(body('Get_file'))"}},
                                  {"inputs": {"body": "@body('Get_file')"}}]}
        self.assertEqual(module.validate_content_base64(definition), [])

    def test_cli_checks_exported_definition(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            definition_path = Path(temporary_directory) / "flow.json"
            payload = {"properties": {"definition": {"actions": [{"contentBase64": "@body('File')"}]}}}
            definition_path.write_text(json.dumps(payload), encoding="utf-8")
            rejected = subprocess.run(
                [sys.executable, str(SCRIPT), str(definition_path)], capture_output=True, text=True, check=False
            )
            self.assertEqual(rejected.returncode, 1)
            self.assertIn("$.actions[0].contentBase64", rejected.stderr)

            payload["properties"]["definition"]["actions"][0]["contentBase64"] = "@base64(body('File'))"
            definition_path.write_text(json.dumps(payload), encoding="utf-8")
            accepted = subprocess.run(
                [sys.executable, str(SCRIPT), str(definition_path)], capture_output=True, text=True, check=False
            )
            self.assertEqual(accepted.returncode, 0)
            self.assertIn("OK: flow definition validation passed", accepted.stdout)


if __name__ == "__main__":
    unittest.main()