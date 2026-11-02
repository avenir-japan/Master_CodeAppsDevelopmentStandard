"""Offline approval gate for historical Copilot Studio deployment examples."""

import argparse
import os
import re
import uuid


def _bot_id(value):
    if not re.fullmatch(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", value or ""):
        raise ValueError("An exact bot GUID is required; URLs and name lookup are not approved")
    return str(uuid.UUID(value))


def require_approval(*, target_variable="BOT_ID", delete_topics=False, publish=False):
    """Fail before credentials/network access unless explicit target and impact match."""
    parser = argparse.ArgumentParser(description="Historical example; offline unless explicitly approved")
    parser.add_argument("--approve-bot", help="Exact BOT_ID GUID to change")
    if delete_topics:
        parser.add_argument("--approve-topic-deletion", action="store_true")
        parser.add_argument("--approved-topic-ids", help="Comma-separated GUIDs individually approved for deletion")
    if publish:
        parser.add_argument("--approve-publish", action="store_true")
    args = parser.parse_args()
    try:
        expected = _bot_id(os.environ.get(target_variable, ""))
        approved = _bot_id(args.approve_bot)
    except ValueError as exc:
        parser.error(str(exc))
    if approved != expected:
        parser.error(f"--approve-bot must match {target_variable}")
    if publish and not args.approve_publish:
        parser.error("--approve-publish is required")
    if delete_topics:
        if not args.approve_topic_deletion or not args.approved_topic_ids:
            parser.error("--approve-topic-deletion and --approved-topic-ids are required")
        try:
            approved_ids = {_bot_id(item.strip()) for item in args.approved_topic_ids.split(",")}
        except ValueError as exc:
            parser.error(str(exc))
        if not approved_ids:
            parser.error("At least one topic ID must be approved")
        return approved_ids
    return set()
