"""Offline fail-closed checks for historical Copilot Studio scripts."""

import ast
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import uuid

SCRIPTS = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("execution_guard", SCRIPTS / "execution_guard.py")
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)
BOT = str(uuid.UUID(int=1))
TOPIC = str(uuid.UUID(int=2))
ARCHIVED = (
    "cleanup_bot.py", "deploy_email_trigger.py", "deploy_market_insight.py",
    "deploy_news_agent.py", "deploy_news_flow.py", "fix_email_msgid.py",
    "fix_email_reply.py", "fix_email_trigger.py", "fix_email_trigger_v2.py",
    "setup_email_trigger.py", "test_desc_timing.py", "test_instructions.py",
)


class ExecutionGuardTests(unittest.TestCase):
    def approve(self, bot=BOT, approved=BOT, *args):
        argv = ["script", "--approve-bot", approved, "--approve-publish",
                "--approve-topic-deletion", "--approved-topic-ids", TOPIC, *args]
        with patch.dict(os.environ, {"BOT_ID": bot}), patch.object(sys, "argv", argv):
            with contextlib.redirect_stderr(io.StringIO()):
                return guard.require_approval(delete_topics=True, publish=True)

    def test_exact_approval(self):
        self.assertEqual(self.approve(), {TOPIC})

    def test_reject_embedded_or_different_bot(self):
        for value in (f"https://host/bots/{BOT}/overview", f"prefix{BOT}", "", TOPIC):
            with self.subTest(value=value), self.assertRaises(SystemExit):
                self.approve(bot=value)
        with self.assertRaises(SystemExit):
            self.approve(approved=TOPIC)

    def test_reject_missing_or_invalid_permissions(self):
        for option in ("--approve-publish", "--approve-topic-deletion", "--approved-topic-ids"):
            args = ["script", "--approve-bot", BOT, "--approve-publish",
                    "--approve-topic-deletion", "--approved-topic-ids", TOPIC]
            index = args.index(option)
            del args[index:index + (2 if option == "--approved-topic-ids" else 1)]
            with self.subTest(option=option), patch.dict(os.environ, {"BOT_ID": BOT}), patch.object(sys, "argv", args):
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    guard.require_approval(delete_topics=True, publish=True)
        with self.assertRaises(SystemExit):
            self.approve(BOT, BOT, "--unrecognized")

    def test_topic_deletion_requires_exact_inventory_before_any_delete(self):
        source = ast.parse((SCRIPTS / "deploy_agent.py").read_text(encoding="utf-8"))
        function = next(node for node in source.body if isinstance(node, ast.FunctionDef)
                        and node.name == "delete_custom_topics")
        module = ast.Module(body=[function], type_ignores=[])
        deleted = []
        topics = [{"botcomponentid": TOPIC, "componenttype": 1, "name": "custom", "schemaname": "custom"}]
        namespace = {"api_get": lambda *_: {"value": topics}, "api_delete": deleted.append,
                     "PROTECTED_TOPIC_PATTERNS": []}
        exec(compile(module, str(SCRIPTS / "deploy_agent.py"), "exec"), namespace)
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(RuntimeError):
                namespace["delete_custom_topics"](BOT, {BOT})
            self.assertEqual(deleted, [])
            namespace["delete_custom_topics"](BOT, {TOPIC})
        self.assertEqual(deleted, [f"botcomponents({TOPIC})"])

    def test_archived_scripts_stop_before_imports(self):
        for script in ARCHIVED + ("deploy_agent.py",):
            with self.subTest(script=script):
                result = subprocess.run([sys.executable, str(SCRIPTS / script)],
                                        capture_output=True, text=True, timeout=10,
                                        env={**os.environ, "BOT_ID": BOT})
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue("execution disabled" in result.stderr or "--approve-bot" in result.stderr,
                                result.stderr)
                self.assertNotIn("ModuleNotFoundError", result.stderr)


if __name__ == "__main__":
    unittest.main()
