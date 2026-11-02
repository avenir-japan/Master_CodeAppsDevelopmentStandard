"""Offline regression tests for deployment entry points and replacement authorization."""

import importlib.util
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
spec = importlib.util.spec_from_file_location("deployment_safety", SCRIPTS / "deployment_safety.py")
safety = importlib.util.module_from_spec(spec)
spec.loader.exec_module(safety)


class DeploymentSafetyTests(unittest.TestCase):
    def test_default_entry_points_do_not_deploy(self):
        for filename in ("deploy_flow.py", "deploy_flow_create_notify.py", "deploy_flow_sp_teams.py"):
            with self.subTest(filename=filename):
                result = subprocess.run(
                    [sys.executable, str(SCRIPTS / filename)], capture_output=True, text=True, check=False
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Dry-run: no API calls", result.stdout)

    def test_legacy_entry_point_is_disabled(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "deploy_flow_sp_incident_v2.py")],
            capture_output=True, text=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("deployment disabled", result.stderr)

    def test_existing_flow_requires_exact_id(self):
        existing = [{"workflowid": "known-id"}]
        for args in (
            SimpleNamespace(execute=False, replace_workflow_id="known-id"),
            SimpleNamespace(execute=True, replace_workflow_id=None),
            SimpleNamespace(execute=True, replace_workflow_id="different-id"),
        ):
            with self.subTest(args=args), self.assertRaises(RuntimeError):
                safety.check_existing_flows(existing, args)
        safety.check_existing_flows(existing, SimpleNamespace(execute=True, replace_workflow_id="known-id"))

    def test_ambiguous_or_missing_flow_fails_closed(self):
        for existing, requested in (
            ([{"workflowid": "one"}, {"workflowid": "two"}], "one"),
            ([], "one"),
        ):
            with self.subTest(existing=existing), self.assertRaises(RuntimeError):
                safety.check_existing_flows(existing, SimpleNamespace(execute=True, replace_workflow_id=requested))
        safety.check_existing_flows([], SimpleNamespace(execute=True, replace_workflow_id=None))

    def test_id_mismatch_prevents_all_mutations_before_connection_references(self):
        for filename in ("deploy_flow.py", "deploy_flow_create_notify.py", "deploy_flow_sp_teams.py"):
            with self.subTest(filename=filename):
                spec = importlib.util.spec_from_file_location(filename[:-3], SCRIPTS / filename)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                with patch.object(module, "resolve_environment_id", return_value="fake-env"), \
                     patch.object(module, "find_connections") as connections, \
                     patch.object(module, "create_connection_reference", create=True) as create_ref, \
                     patch.object(module, "create_connection_references", create=True) as create_refs:
                    if filename == "deploy_flow.py":
                        with patch.object(module, "api_get", return_value={"value": [{"workflowid": "actual"}]}), \
                             patch.object(module, "api_post") as post, \
                             patch.object(module, "api_patch") as update, \
                             patch.object(module, "api_delete") as delete, \
                             redirect_stdout(StringIO()):
                            with self.assertRaises(RuntimeError):
                                module.main(["--execute", "--replace-workflow-id", "wrong"])
                            for mutation in (post, update, delete):
                                mutation.assert_not_called()
                    else:
                        session = MagicMock()
                        session.get.return_value.json.return_value = {"value": [{"workflowid": "actual"}]}
                        with patch.object(module, "get_session", return_value=session), redirect_stdout(StringIO()):
                            if filename == "deploy_flow_create_notify.py":
                                with patch.object(module, "ADMIN_EMAIL", "test" + "@" + "example.invalid"):
                                    with self.assertRaises(RuntimeError):
                                        module.main(["--execute", "--replace-workflow-id", "wrong"])
                            else:
                                with self.assertRaises(RuntimeError):
                                    module.main(["--execute", "--replace-workflow-id", "wrong"])
                        session.post.assert_not_called()
                        session.patch.assert_not_called()
                        session.delete.assert_not_called()
                    connections.assert_not_called()
                    create_ref.assert_not_called()
                    create_refs.assert_not_called()

    def test_exactly_one_notify_entry_point(self):
        source = (SCRIPTS / "deploy_flow_create_notify.py").read_text(encoding="utf-8")
        self.assertEqual(source.count('if __name__ == "__main__":'), 1)
        self.assertEqual(source.count("def main("), 1)
        self.assertNotIn("def deploy_flow(env_id:", source)


if __name__ == "__main__":
    unittest.main()
