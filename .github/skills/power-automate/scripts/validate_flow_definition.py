"""Validate data-source-independent flow definition contracts before deployment."""

import argparse
import json
from pathlib import Path


def validate_content_base64(value: object, path: str = "$", errors: list[str] | None = None) -> list[str]:
    if errors is None:
        errors = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key == "contentBase64":
                if not isinstance(child, str) or not child.strip():
                    errors.append(f"{child_path}: contentBase64 must be a non-empty string")
                elif child.strip().startswith("@") and not child.strip().replace(" ", "").lower().startswith("@base64("):
                    errors.append(f"{child_path}: runtime contentBase64 must use @base64(...)")
            else:
                validate_content_base64(child, child_path, errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_content_base64(child, f"{path}[{index}]", errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Power Automate workflow definition JSON file")
    parser.add_argument("definition", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.definition.read_text(encoding="utf-8"))
    definition = payload.get("properties", {}).get("definition", payload) if isinstance(payload, dict) else None
    if not isinstance(definition, dict):
        parser.error("workflow definition must be a JSON object")
    errors = validate_content_base64(definition)
    if errors:
        parser.exit(1, "Invalid flow binary-content contract:\n" + "\n".join(errors) + "\n")
    print("OK: flow definition validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())