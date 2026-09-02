"""configuration（bots の JSON 文字列カラム）を PATCH する前の恒久チェック。

configuration を丸ごと上書きすると model / instructions / memory / greeting などが
まとめて消える。set_*.py はすべて GET → deep-merge → PATCH で更新するが、
マージ漏れを見逃さないよう **送信直前に** 更新前後を突き合わせる。

set_instructions.py / set_model.py / set_prompts.py から呼ばれ、正常系でも毎回動作する。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_STD = Path(__file__).resolve().parents[2] / "standard" / "scripts"


def load_auth_helper() -> tuple[str, object]:
    module_path = _STD / "auth_helper.py"
    spec = importlib.util.spec_from_file_location("auth_helper", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"auth_helper.py を読み込めません: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    dataverse_url = getattr(module, "DATAVERSE_URL")
    get_session = getattr(module, "get_session")
    return dataverse_url, get_session


DATAVERSE_URL, get_session = load_auth_helper()

# 更新対象として明示されない限り保持されるべきキー（agentSettings 配下）
GUARDED_SETTINGS = ("model", "instructions", "enableMemory", "greetingText", "conversationStarters")
# BotConfiguration の直下で保持されるべきキー
GUARDED_ROOT = ("$kind", "recognizer", "channels")


def assert_intact(before: dict, after: dict, *, changing: str) -> None:
    """更新対象 `changing` 以外の設定が欠落していないことを検証する。

    changing: 今回意図的に書き換えるキー（"instructions" / "model" / "prompts"）。
    """
    changed = {"prompts": ("greetingText", "conversationStarters")}.get(changing, (changing,))
    lost = [k for k in GUARDED_ROOT if k in before and k not in after]
    lost += [
        f"agentSettings.{k}"
        for k in GUARDED_SETTINGS
        if k not in changed
        and k in before.get("agentSettings", {})
        and k not in after.get("agentSettings", {})
    ]
    if lost:
        raise SystemExit(
            "❌ configuration のマージに失敗しています（PATCH 中止）。消えるキー: "
            + ", ".join(lost)
            + "\n   丸ごと上書きせず GET → deep-merge → PATCH になっているか確認してください。"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="cliagent の BotConfiguration 構造と必須キーを検証する"
    )
    parser.add_argument(
        "--bot-id",
        help="対象 Bot の ID。未指定時は AGENT_BOTID または agent_botid.txt を使用",
    )
    return parser.parse_args()


def resolve_bot_id(bot_id_arg: str | None) -> str:
    if bot_id_arg:
        return bot_id_arg.strip()
    if os.getenv("AGENT_BOTID"):
        return os.getenv("AGENT_BOTID", "").strip()
    if Path("agent_botid.txt").exists():
        return Path("agent_botid.txt").read_text(encoding="utf-8").strip()
    return ""


def load_configuration(bot_id: str) -> tuple[str, dict]:
    sess = get_session()
    url = f"{DATAVERSE_URL}/api/data/v9.2/bots({bot_id})?$select=name,configuration"
    res = sess.get(url)
    res.raise_for_status()
    payload = res.json()
    config_raw = payload.get("configuration") or "{}"
    config = json.loads(config_raw) if isinstance(config_raw, str) else config_raw
    return str(payload.get("name") or bot_id), config


def validate_configuration(config: dict) -> list[str]:
    issues: list[str] = []
    if config.get("$kind") != "BotConfiguration":
        issues.append("$kind が BotConfiguration ではありません")
    if "recognizer" not in config:
        issues.append("recognizer がありません")
    agent_settings = config.get("agentSettings")
    if not isinstance(agent_settings, dict):
        issues.append("agentSettings がありません")
        return issues
    for key in ("model", "instructions", "enableMemory"):
        if key not in agent_settings:
            issues.append(f"agentSettings.{key} がありません")
    return issues


def main() -> int:
    args = parse_args()
    bot_id = resolve_bot_id(args.bot_id)
    if not bot_id:
        print("AGENT_BOTID 未設定。agent_botid.txt も無し。", file=sys.stderr)
        return 1

    bot_name, config = load_configuration(bot_id)
    issues = validate_configuration(config)

    print(f"Bot: {bot_name}")
    print(f"$kind: {config.get('$kind')}")
    print(f"recognizer: {config.get('recognizer', {}).get('$kind', '-')}")
    agent_settings = config.get("agentSettings") or {}
    print(f"model: {agent_settings.get('model', {}).get('series', '-')}")
    print(f"enableMemory: {agent_settings.get('enableMemory', '-')}")
    print(
        "instructions: "
        + ("present" if agent_settings.get("instructions") else "missing")
    )

    if issues:
        print("\n❌ 検証 NG")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("\n✅ 検証 OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
