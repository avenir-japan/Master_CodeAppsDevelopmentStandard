"""
cliagent エージェントの構造を検証する。
  - 配下の botcomponents（type=9 スキル / type=14 同梱ファイル）を列挙
  - type=14 の filedata を実体ダウンロードしてサイズを確認（読み取り可能か）

.env / 引数:
  AGENT_BOTID   対象 Bot の botid（未指定なら agent_botid.txt を読む）

実行: python verify_agent.py
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
_STD = Path(__file__).resolve().parents[2] / "standard" / "scripts"


def load_auth_helper() -> tuple[object, str]:
    module_path = _STD / "auth_helper.py"
    spec = importlib.util.spec_from_file_location("auth_helper", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"auth_helper.py を読み込めません: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    get_session = getattr(module, "get_session")
    dataverse_url = getattr(module, "DATAVERSE_URL")
    return get_session, dataverse_url


get_session, DATAVERSE_URL = load_auth_helper()

API = f"{DATAVERSE_URL}/api/data/v9.2"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="cliagent の botcomponents と filedata を検証する"
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


def main() -> None:
    args = parse_args()
    bot_id = resolve_bot_id(args.bot_id)
    if not bot_id:
        print("AGENT_BOTID 未設定。agent_botid.txt も無し。", file=sys.stderr)
        sys.exit(1)
    sess = get_session()
    r = sess.get(
        f"{API}/botcomponents?$select=botcomponentid,name,componenttype,schemaname,"
        f"_parentbotcomponentid_value,filedata_name&$filter=_parentbotid_value eq {bot_id}"
    )
    r.raise_for_status()
    comps = r.json().get("value", [])
    print(f"botcomponents: {len(comps)} 件\n")
    for c in comps:
        parent = str(c.get("_parentbotcomponentid_value") or "-")[:8]
        fn = c.get("filedata_name") or ""
        print(f"  type={c['componenttype']:>3}  {c['name']:<30} parent={parent:<8} file={fn}")

    print("\n--- filedata 読み取り検証 ---")
    ok = True
    for c in comps:
        if c["componenttype"] == 14:
            dl = sess.get(f"{API}/botcomponents({c['botcomponentid']})/filedata/$value")
            status = dl.status_code
            size = len(dl.content)
            print(f"  {c['name']:<24} status={status} size={size} bytes")
            if status != 200 or size == 0:
                ok = False
    print("\n" + ("✅ 検証 OK" if ok else "⚠️ 一部 filedata が読めません"))


if __name__ == "__main__":
    main()
