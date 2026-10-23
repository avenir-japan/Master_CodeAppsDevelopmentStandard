import json
import unittest
from argparse import Namespace
from pathlib import Path
from subprocess import CompletedProcess
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import auth_helper
import initialize_workspace
import setup_environment
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import AuthenticationRequiredError


class AuthSetupTests(unittest.TestCase):
    def test_matching_legacy_browser_record_is_migrated(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".auth_record_browser.json").write_text('{"tenant_id": "internal"}', encoding="utf-8")
            new_path = root / "cache" / "auth_record_internal_browser.json"
            with (
                patch.object(auth_helper, "TENANT_ID", "internal"),
                patch.object(auth_helper, "_PROJECT_ROOT", root),
                patch.object(auth_helper, "_BROWSER_AUTH_RECORD_PATH", new_path),
                patch.object(auth_helper.AuthenticationRecord, "deserialize", side_effect=lambda text: SimpleNamespace(tenant_id=json.loads(text)["tenant_id"], serialize=lambda: text)),
                patch.object(auth_helper, "InteractiveBrowserCredential") as credential,
                patch.object(auth_helper, "_browser_credentials", {}),
            ):
                auth_helper._ensure_browser_credential()
            self.assertEqual(new_path.read_text(encoding="utf-8"), '{"tenant_id": "internal"}')
            self.assertEqual(credential.call_args.kwargs["authentication_record"].tenant_id, "internal")

    def test_mismatched_legacy_record_is_not_migrated(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".auth_record_browser.json").write_text('{"tenant_id": "other"}', encoding="utf-8")
            new_path = root / "cache" / "auth_record_internal_browser.json"
            with (
                patch.object(auth_helper, "TENANT_ID", "internal"),
                patch.object(auth_helper, "_PROJECT_ROOT", root),
                patch.object(auth_helper, "_BROWSER_AUTH_RECORD_PATH", new_path),
                patch.object(auth_helper.AuthenticationRecord, "deserialize", side_effect=lambda text: SimpleNamespace(tenant_id=json.loads(text)["tenant_id"], serialize=lambda: text)),
                patch.object(auth_helper, "InteractiveBrowserCredential") as credential,
                patch.object(auth_helper, "_browser_credentials", {}),
            ):
                auth_helper._ensure_browser_credential()
            self.assertFalse(new_path.exists())
            self.assertNotIn("authentication_record", credential.call_args.kwargs)

    def test_wrong_tenant_record_requires_new_browser_authentication(self):
        with TemporaryDirectory() as directory:
            record_path = Path(directory) / "auth_record_internal_browser.json"
            client_record_path = record_path.with_name("auth_record_internal_browser_client-one.json")
            client_record_path.write_text('{"tenant_id": "other"}', encoding="utf-8")
            new_record = SimpleNamespace(tenant_id="internal", serialize=lambda: '{"tenant_id": "internal"}')
            credential = MagicMock()
            credential.authenticate.return_value = new_record
            credential.get_token.return_value = SimpleNamespace(token="token", expires_on=9999999999)
            with (
                patch.object(auth_helper, "TENANT_ID", "internal"),
                patch.object(auth_helper, "_BROWSER_AUTH_RECORD_PATH", record_path),
                patch.object(auth_helper.AuthenticationRecord, "deserialize", side_effect=lambda text: SimpleNamespace(tenant_id=json.loads(text)["tenant_id"], serialize=lambda: text)),
                patch.object(auth_helper, "InteractiveBrowserCredential", return_value=credential) as build_credential,
                patch.object(auth_helper, "_browser_credentials", {}),
                patch.object(auth_helper, "_inmemory_tokens", {}),
            ):
                self.assertEqual(auth_helper.get_token("test.scope", client_id="client-one"), "token")
                self.assertEqual(auth_helper.get_token("test.scope", client_id="client-one"), "token")
                self.assertNotIn("authentication_record", build_credential.call_args.kwargs)
                self.assertEqual(client_record_path.read_text(encoding="utf-8"), '{"tenant_id": "internal"}')
            credential.authenticate.assert_called_once_with(scopes=["test.scope"])

    def test_matching_browser_record_reuses_cached_sign_in(self):
        with TemporaryDirectory() as directory:
            record_path = Path(directory) / "auth_record_internal_browser.json"
            record_path.write_text('{"tenant_id": "internal"}', encoding="utf-8")
            credential = MagicMock()
            credential.get_token.return_value = SimpleNamespace(token="cached", expires_on=9999999999)
            with (
                patch.object(auth_helper, "TENANT_ID", "internal"),
                patch.object(auth_helper, "PREFER_BROWSER_AUTH", True),
                patch.object(auth_helper, "_BROWSER_AUTH_RECORD_PATH", record_path),
                patch.object(auth_helper.AuthenticationRecord, "deserialize", side_effect=lambda text: SimpleNamespace(tenant_id=json.loads(text)["tenant_id"])),
                patch.object(auth_helper, "InteractiveBrowserCredential", return_value=credential) as build_credential,
                patch.object(auth_helper, "_browser_credentials", {}),
                patch.object(auth_helper, "_inmemory_tokens", {}),
            ):
                self.assertEqual(auth_helper.get_token("test.scope"), "cached")
                self.assertEqual(auth_helper.get_token("test.scope"), "cached")
            self.assertEqual(build_credential.call_args.kwargs["authentication_record"].tenant_id, "internal")
            credential.authenticate.assert_not_called()
            credential.get_token.assert_called_once_with("test.scope")

    def test_browser_cache_failure_preserves_record_and_requires_explicit_reauth(self):
        with TemporaryDirectory() as directory:
            record_path = Path(directory) / "auth_record_internal_browser.json"
            record_path.write_text('{"tenant_id": "internal"}', encoding="utf-8")
            credential = MagicMock()
            credential.get_token.side_effect = ClientAuthenticationError(message="permission denied")
            with (
                patch.object(auth_helper, "TENANT_ID", "internal"),
                patch.object(auth_helper, "PREFER_BROWSER_AUTH", True),
                patch.object(auth_helper, "_BROWSER_AUTH_RECORD_PATH", record_path),
                patch.object(auth_helper.AuthenticationRecord, "deserialize", side_effect=lambda text: SimpleNamespace(tenant_id=json.loads(text)["tenant_id"])),
                patch.object(auth_helper, "InteractiveBrowserCredential", return_value=credential) as build_credential,
                patch.object(auth_helper, "_browser_credentials", {}),
                patch.object(auth_helper, "_inmemory_tokens", {}),
            ):
                with self.assertRaises(ClientAuthenticationError):
                    auth_helper.get_token("test.scope")
                self.assertTrue(record_path.exists())
                self.assertTrue(build_credential.call_args.kwargs["disable_automatic_authentication"])
            credential.authenticate.assert_not_called()

    def test_browser_interaction_required_preserves_record(self):
        with TemporaryDirectory() as directory:
            record_path = Path(directory) / "auth_record_internal_browser.json"
            record_path.write_text('{"tenant_id": "internal"}', encoding="utf-8")
            credential = MagicMock()
            credential.get_token.side_effect = AuthenticationRequiredError(message="sign in required", scopes=["test.scope"])
            with (
                patch.object(auth_helper, "TENANT_ID", "internal"),
                patch.object(auth_helper, "PREFER_BROWSER_AUTH", True),
                patch.object(auth_helper, "_BROWSER_AUTH_RECORD_PATH", record_path),
                patch.object(auth_helper.AuthenticationRecord, "deserialize", side_effect=lambda text: SimpleNamespace(tenant_id=json.loads(text)["tenant_id"])),
                patch.object(auth_helper, "InteractiveBrowserCredential", return_value=credential),
                patch.object(auth_helper, "_browser_credentials", {}),
                patch.object(auth_helper, "_inmemory_tokens", {}),
            ):
                with self.assertRaises(AuthenticationRequiredError):
                    auth_helper.get_token("test.scope")
                self.assertTrue(record_path.exists())
            credential.authenticate.assert_not_called()

    def test_persistent_caches_do_not_allow_plaintext_fallback(self):
        with patch.dict("os.environ", {"PP_NO_PERSISTENT_CACHE": ""}):
            browser_options = auth_helper._interactive_browser_credential_kwargs()["cache_persistence_options"]
            with patch.object(auth_helper, "DeviceCodeCredential") as device_credential:
                auth_helper._build_credential()
            device_options = device_credential.call_args.kwargs["cache_persistence_options"]
        self.assertFalse(browser_options.allow_unencrypted_storage)
        self.assertFalse(device_options.allow_unencrypted_storage)

    def test_client_ids_use_separate_records_and_memory_tokens(self):
        with TemporaryDirectory() as directory:
            record_path = Path(directory) / "auth_record_internal_browser.json"
            credentials = []

            def create_credential(**kwargs):
                credential = MagicMock()
                client_id = kwargs["client_id"]
                credential.authenticate.return_value = SimpleNamespace(
                    tenant_id="internal", serialize=lambda: '{"tenant_id": "internal"}'
                )
                credential.get_token.return_value = SimpleNamespace(token=client_id, expires_on=9999999999)
                credentials.append(credential)
                return credential

            with (
                patch.object(auth_helper, "TENANT_ID", "internal"),
                patch.object(auth_helper, "_BROWSER_AUTH_RECORD_PATH", record_path),
                patch.object(auth_helper, "InteractiveBrowserCredential", side_effect=create_credential),
                patch.object(auth_helper, "_browser_credentials", {}),
                patch.object(auth_helper, "_inmemory_tokens", {}),
            ):
                self.assertEqual(auth_helper.get_token("test.scope", client_id="one"), "one")
                self.assertEqual(auth_helper.get_token("test.scope", client_id="two"), "two")
                self.assertEqual(auth_helper.get_token("test.scope", client_id="one"), "one")
                self.assertTrue(auth_helper._browser_record_path("one").is_file())
                self.assertTrue(auth_helper._browser_record_path("two").is_file())
            self.assertEqual(len(credentials), 2)

    def test_list_restores_original_active_profile(self):
        profiles = [
            {"index": "1", "active": "*", "name": "original", "user": "user@example.com"},
            {"index": "2", "active": "", "name": "other", "user": "user@example.com"},
        ]
        with (
            patch.object(setup_environment, "list_profiles", return_value=profiles),
            patch.object(setup_environment, "org_who", side_effect=[None, {"url": "https://example.test", "env_id": "env", "friendly": "Dev"}]),
            patch.object(setup_environment, "run_command", return_value=CompletedProcess([], 0)) as run_command,
        ):
            self.assertEqual(setup_environment.command_list(), 0)
        run_command.assert_called_once_with(["pac", "auth", "select", "--name", "original"])

    def test_list_reports_failed_profile_restoration(self):
        profiles = [{"index": "1", "active": "*", "name": "original", "user": "user@example.com"}]
        with (
            patch.object(setup_environment, "list_profiles", return_value=profiles),
            patch.object(setup_environment, "org_who", return_value=None),
            patch.object(setup_environment, "run_command", return_value=CompletedProcess([], 1)),
        ):
            self.assertEqual(setup_environment.command_list(), 1)

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

    def test_profile_does_not_change_env_when_tenant_resolution_fails(self):
        args = Namespace(profile="other", solution=None, display=None, prefix=None, no_auth=False)
        with TemporaryDirectory() as directory:
            repo_root = Path(directory)
            env_path = repo_root / ".env"
            original = "DATAVERSE_URL=https://old.example.test/\nTENANT_ID=old-tenant\n"
            env_path.write_text(original, encoding="utf-8")
            with (
                patch.object(setup_environment, "org_who", return_value={"url": "https://new.example.test/", "env_id": "new-env", "user": "admin@example.com"}),
                patch.object(setup_environment, "resolve_tenant", return_value=""),
                patch.object(setup_environment, "trigger_auth") as trigger_auth,
            ):
                self.assertEqual(setup_environment.command_profile(args, repo_root), 1)
            self.assertEqual(env_path.read_text(encoding="utf-8"), original)
            trigger_auth.assert_not_called()

    def test_auth_only_explicitly_renews_when_interaction_required(self):
        with (
            patch.object(auth_helper, "api_get", side_effect=[AuthenticationRequiredError(message="sign in required", scopes=["test.scope"]), {"UserId": "user"}]) as whoami,
            patch.object(auth_helper, "authenticate") as authenticate,
            patch.dict("os.environ", {}, clear=False),
        ):
            self.assertEqual(setup_environment.trigger_auth({"DATAVERSE_URL": "https://example.test"}), 0)
        authenticate.assert_called_once_with()
        self.assertEqual(whoami.call_count, 2)

    def test_auth_only_does_not_retry_unrelated_authentication_failure(self):
        with (
            patch.object(auth_helper, "api_get", side_effect=ClientAuthenticationError(message="permission denied")),
            patch.object(auth_helper, "authenticate") as authenticate,
        ):
            with self.assertRaises(ClientAuthenticationError):
                setup_environment.trigger_auth({})
        authenticate.assert_not_called()


class WorkspaceInstallTests(unittest.TestCase):
    def test_dry_run_and_apply_preserve_existing_files(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            target = Path(directory) / "target"
            (source / ".github/agents").mkdir(parents=True)
            (source / ".github/skills/standard/references").mkdir(parents=True)
            (target / ".github/agents").mkdir(parents=True)
            (source / ".github/agents/new.md").write_text("standard", encoding="utf-8")
            (source / ".github/agents/__pycache__").mkdir()
            (source / ".github/agents/__pycache__/generated.pyc").write_bytes(b"generated")
            (target / ".github/agents/new.md").write_text("project", encoding="utf-8")
            (source / ".github/skills/standard/references/gitignore-template").write_text(".env\nnode_modules/\n", encoding="utf-8")
            (source / ".github/copilot-instructions.md").write_text("standard", encoding="utf-8")
            (source / ".env.example").write_text("EXAMPLE=1", encoding="utf-8")
            (target / ".gitignore").write_text("# project\n.env\n", encoding="utf-8")

            added, conflicts = initialize_workspace.install(source, target)
            self.assertIn(Path(".github/agents/new.md"), conflicts)
            self.assertIn(Path(".gitignore"), added)
            self.assertFalse((target / ".github/copilot-instructions.md").exists())
            self.assertNotIn(Path(".github/agents/__pycache__/generated.pyc"), added)
            self.assertEqual((target / ".gitignore").read_text(encoding="utf-8"), "# project\n.env\n")

            initialize_workspace.install(source, target, apply=True)
            self.assertEqual((target / ".github/agents/new.md").read_text(encoding="utf-8"), "project")
            self.assertEqual((target / ".github/copilot-instructions.md").read_text(encoding="utf-8"), "standard")
            self.assertEqual((target / ".gitignore").read_text(encoding="utf-8"), "# project\n.env\nnode_modules/\n")
            added, conflicts = initialize_workspace.install(source, target, apply=True)
            self.assertEqual(added, [])
            self.assertEqual(conflicts, [Path(".github/agents/new.md")])


if __name__ == "__main__":
    unittest.main()