import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import MagicMock, patch

import auth_helper
import setup_environment


class AuthSetupTests(unittest.TestCase):
    def test_explicit_auth_uses_browser_when_enabled(self):
        record = object()
        credential = MagicMock()
        credential.authenticate.return_value = record
        with (
            patch.object(auth_helper, "PREFER_BROWSER_AUTH", True),
            patch.object(auth_helper, "_ensure_browser_credential", return_value=credential),
            patch.object(auth_helper, "_save_browser_auth_record") as save_browser,
            patch.object(auth_helper, "_ensure_credential") as device_credential,
        ):
            self.assertIs(auth_helper.authenticate("test.scope"), record)
        credential.authenticate.assert_called_once_with(scopes=["test.scope"])
        save_browser.assert_called_once_with(record)
        device_credential.assert_not_called()

    def test_profile_writes_browser_setting(self):
        args = Namespace(profile="internal", solution=None, display=None, prefix=None, no_auth=False)
        with (
            patch.object(setup_environment, "org_who", return_value={"url": "https://example.test/", "env_id": "env", "user": "admin@example.com"}),
            patch.object(setup_environment, "resolve_tenant", return_value="tenant"),
            patch.object(setup_environment, "upsert_env", return_value=Path(".env")) as upsert,
            patch.object(setup_environment, "trigger_auth", return_value=0),
        ):
            self.assertEqual(setup_environment.command_profile(args, Path(".")), 0)
        self.assertEqual(upsert.call_args.args[1]["PP_USE_INTERACTIVE_BROWSER"], "true")


if __name__ == "__main__":
    unittest.main()