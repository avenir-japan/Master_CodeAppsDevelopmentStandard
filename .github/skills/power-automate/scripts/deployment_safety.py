"""Fail-closed CLI and existing-flow checks for destructive deployment samples."""

import argparse


def deployment_args(argv=None):
    parser = argparse.ArgumentParser(description="Draft/activation deployment sample (dry-run by default)")
    parser.add_argument("--execute", action="store_true", help="Allow live API calls, including creating a new flow")
    parser.add_argument("--replace-workflow-id", help="Exact workflow ID authorized for replacement, if one exists")
    args = parser.parse_args(argv)
    if args.replace_workflow_id and not args.execute:
        parser.error("--replace-workflow-id requires --execute")
    return args


def check_existing_flows(existing, args):
    """Reject ambiguous matches and require an exact existing ID before deletion."""
    if not args.execute:
        raise RuntimeError("Dry-run: live deployment requires --execute")
    if len(existing) > 1:
        raise RuntimeError("Multiple flows have this name; refusing to replace any")
    if existing:
        actual_id = existing[0]["workflowid"]
        if args.replace_workflow_id != actual_id:
            raise RuntimeError(
                f"Existing flow {actual_id}: back up and review it, then pass "
                "--replace-workflow-id with its exact ID to authorize deletion/recreation"
            )
    elif args.replace_workflow_id:
        raise RuntimeError("Expected workflow was not found; refusing to create a different flow")
