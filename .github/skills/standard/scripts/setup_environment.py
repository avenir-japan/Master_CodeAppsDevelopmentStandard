"""PAC プロファイルから環境を取得して .env を構成し、デバイスコード認証して auth_helper に保存する。

標準プロセス（プロジェクト開始時の環境セットアップ）:
  1. ``--list``  : ``pac auth list`` のプロファイルを ``pac org who`` で解決し、環境候補を一覧表示
                   （エージェントはこの一覧を AskUserQuestion でユーザーに選ばせる）。
  2. ``--profile <名前>`` : 選択プロファイルの環境値（URL / 環境 ID / テナント）で ``.env`` を upsert。
  3. 既定でデバイスコード認証をトリガーし、auth_helper が AuthenticationRecord を保存する。
     これ以降の Python スクリプトは 2 層キャッシュによりデバイスコード入力なしで認証される。

補足:
  - この PAC CLI バージョンには ``pac auth token`` が無いため、Python の Dataverse 認証は
    PAC プロファイルではなく **デバイスコード認証（auth_helper）** を正式な経路とする。
  - PAC プロファイルは「環境メタデータ（URL / 環境 ID）」の取得元として利用する。
  - テナント GUID は選択プロファイルのユーザーのドメインから OIDC ディスカバリで解決する。

依存: requests（テナント解決）, azure-identity / python-dotenv（auth_helper 経由）。

使い方:
  python setup_environment.py --list
  python setup_environment.py --profile "<ProfileName>" \
      --solution "<SolutionName>" --prefix "<prefix>" --display "<表示名>"
  python setup_environment.py --auth-only      # 既存 .env でデバイスコード認証のみ実行
  python setup_environment.py --profile "<ProfileName>" --no-auth  # .env 構成のみ（認証しない）

終了コード: 成功 0 / 前提不足・失敗 1。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
ROW_RE = re.compile(r"^\[(\d+)\]\s*(\*?)\s+\S+\s+(\S+)\s+(\S+@\S+)", re.MULTILINE)


def run_command(args: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", check=check)


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate

    for candidate in (start, *start.parents):
        if (candidate / ".github" / "skills" / "standard" / "SKILL.md").exists():
            return candidate

    return Path.cwd()


def list_profiles() -> list[dict[str, str]]:
    result = run_command(["pac", "auth", "list"])
    if result.returncode != 0:
        raise RuntimeError(f"pac auth list に失敗しました:\n{result.stderr.strip() or result.stdout.strip()}")

    profiles: list[dict[str, str]] = []
    for match in ROW_RE.finditer(result.stdout):
        index, active, name, user = match.group(1), match.group(2), match.group(3), match.group(4)
        profiles.append({"index": index, "active": "*" if active else "", "name": name, "user": user})
    return profiles


def org_who(profile_name: str) -> dict[str, str] | None:
    selected = run_command(["pac", "auth", "select", "--name", profile_name])
    if selected.returncode != 0:
        return None

    result = run_command(["pac", "org", "who", "--json"])
    if result.returncode != 0:
        return None

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

    url = (data.get("OrgUrl") or "").strip()
    env_id = (data.get("EnvironmentId") or "").strip()
    user = (data.get("UserEmail") or "").strip()
    if not url:
        return None

    return {
        "url": url,
        "env_id": env_id,
        "user": user,
        "friendly": (data.get("FriendlyName") or "").strip(),
    }


def resolve_tenant(user_email: str) -> str:
    domain = user_email.split("@", 1)[1] if "@" in user_email else user_email
    try:
        import requests

        url = f"https://login.microsoftonline.com/{domain}/v2.0/.well-known/openid-configuration"
        endpoint = requests.get(url, timeout=15).json().get("token_endpoint", "")
        match = re.search(r"/([0-9a-fA-F-]{36})/", endpoint)
        return match.group(1) if match else ""
    except Exception as exc:
        print(f"[setup_environment] テナント解決に失敗（手動設定が必要）: {exc}", file=sys.stderr)
        return ""


def upsert_env(repo_root: Path, mapping: dict[str, str]) -> Path:
    env_path = repo_root / ".env"
    lines = env_path.read_text(encoding="utf-8").splitlines() if env_path.is_file() else []
    remaining = dict(mapping)
    output: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
            if key in remaining:
                output.append(f"{key}={remaining.pop(key)}")
                continue
        output.append(line)

    if remaining:
        if output and output[-1].strip():
            output.append("")
        for key, value in remaining.items():
            output.append(f"{key}={value}")

    env_path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    return env_path


def trigger_device_code(values: dict[str, str]) -> int:
    if values.get("DATAVERSE_URL"):
        os.environ["DATAVERSE_URL"] = values["DATAVERSE_URL"]
    if values.get("TENANT_ID"):
        os.environ["TENANT_ID"] = values["TENANT_ID"]

    sys.path.insert(0, str(HERE))
    try:
        from auth_helper import api_get  # type: ignore
    except Exception as exc:
        print(f"[setup_environment] auth_helper の読み込みに失敗: {exc}", file=sys.stderr)
        return 1

    whoami = api_get("WhoAmI")
    print("[setup_environment] 認証成功（WhoAmI）:", whoami.get("UserId", ""))
    print("[setup_environment] 認証レコードを保存しました。以降はデバイスコード不要です。")
    return 0


def command_list() -> int:
    try:
        profiles = list_profiles()
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1

    rows = []
    for profile in profiles:
        info = org_who(profile["name"])
        if info is None:
            continue
        rows.append({**profile, **info})

    if not rows:
        print("環境を持つ PAC プロファイルが見つかりません。pac auth create で作成してください。")
        return 1

    print("番号 | プロファイル | 環境名 | 環境 ID | URL")
    for index, row in enumerate(rows, 1):
        active = " (active)" if row["active"] else ""
        print(f"{index} | {row['name']}{active} | {row['friendly']} | {row['env_id']} | {row['url']}")
    print("\nJSON:", json.dumps(rows, ensure_ascii=False))
    print("\n-> この一覧を AskUserQuestion で提示し、選択後に --profile <名前> を実行してください。")
    return 0


def command_profile(args: argparse.Namespace, repo_root: Path) -> int:
    info = org_who(args.profile)
    if info is None:
        print(f"プロファイル '{args.profile}' から環境を取得できませんでした。", file=sys.stderr)
        return 1

    tenant = resolve_tenant(info["user"]) if info["user"] else ""
    mapping = {
        "DATAVERSE_URL": info["url"] if info["url"].endswith("/") else info["url"] + "/",
        "TENANT_ID": tenant,
        "ENV_ID": info["env_id"],
        "PAC_AUTH_PROFILE": args.profile,
    }
    if args.solution:
        mapping["SOLUTION_NAME"] = args.solution
    if args.display:
        mapping["SOLUTION_DISPLAY_NAME"] = args.display
    if args.prefix:
        mapping["PUBLISHER_PREFIX"] = args.prefix
        mapping["VITE_PUBLISHER_PREFIX"] = args.prefix

    env_path = upsert_env(repo_root, mapping)
    print(f"[setup_environment] .env を更新しました: {env_path}")
    for key in ("DATAVERSE_URL", "TENANT_ID", "ENV_ID", "PAC_AUTH_PROFILE"):
        print(f"   {key}={mapping.get(key, '')}")

    if not tenant:
        print("[setup_environment] 警告: TENANT_ID を解決できませんでした。.env を手動設定してください。", file=sys.stderr)
    if args.no_auth:
        return 0
    return trigger_device_code(mapping)


def command_auth_only(repo_root: Path) -> int:
    env_path = repo_root / ".env"
    values: dict[str, str] = {}
    if env_path.is_file():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
    return trigger_device_code(values)


def main() -> int:
    parser = argparse.ArgumentParser(description="PAC プロファイルから .env 構成とデバイスコード認証を行う")
    parser.add_argument("--list", action="store_true", help="環境候補を一覧表示する")
    parser.add_argument("--profile", help="利用する PAC プロファイル名")
    parser.add_argument("--solution", help="SOLUTION_NAME を設定する")
    parser.add_argument("--display", help="SOLUTION_DISPLAY_NAME を設定する")
    parser.add_argument("--prefix", help="PUBLISHER_PREFIX を設定する")
    parser.add_argument("--no-auth", action="store_true", help=".env 構成のみ行い、認証しない")
    parser.add_argument("--auth-only", action="store_true", help="既存 .env を使って認証のみ実行する")
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())

    if args.list:
        return command_list()
    if args.auth_only:
        return command_auth_only(repo_root)
    if args.profile:
        return command_profile(args, repo_root)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())