"""既存案件へ標準のエージェント・スキルを非破壊で配置する。"""

import argparse
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[4]
DIRECTORIES = (Path(".github/agents"), Path(".github/skills"))
FILES = (Path(".github/copilot-instructions.md"), Path(".env.example"), Path(".vscode/mcp.json"))
GITIGNORE_TEMPLATE = Path(".github/skills/standard/references/gitignore-template")


def install(source: Path, target: Path, apply: bool = False) -> tuple[list[Path], list[Path]]:
    """新しいファイルだけ配置し、競合は変更せず返す。"""
    source = source.resolve()
    target = target.resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError("配置元と配置先は別の独立したディレクトリを指定してください")
    if not source.is_dir() or not target.is_dir():
        raise ValueError("配置元と配置先のディレクトリが必要です")

    added: list[Path] = []
    conflicts: list[Path] = []
    candidates = list(FILES)
    for directory in DIRECTORIES:
        candidates.extend(
            path.relative_to(source)
            for path in (source / directory).rglob("*")
            if path.is_file()
            and not path.is_symlink()
            and not any(part in {"__pycache__", ".venv", "node_modules"} for part in path.relative_to(source).parts)
            and path.suffix != ".pyc"
            and path.name != ".env"
        )

    for relative in candidates:
        origin = source / relative
        destination = target / relative
        if origin.is_symlink() or any(part.is_symlink() for part in destination.parents if part != target and target in part.parents):
            conflicts.append(relative)
        elif destination.exists() or destination.is_symlink():
            if not destination.is_file() or destination.read_bytes() != origin.read_bytes():
                conflicts.append(relative)
        else:
            added.append(relative)
            if apply:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(origin.read_bytes())

    gitignore = target / ".gitignore"
    if gitignore.is_symlink():
        conflicts.append(Path(".gitignore"))
    else:
        original = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
        entries = (source / GITIGNORE_TEMPLATE).read_text(encoding="utf-8").splitlines()
        missing = [entry for entry in entries if entry and entry not in original.splitlines()]
        if missing:
            added.append(Path(".gitignore"))
            if apply:
                gitignore.write_text(
                    original + ("\n" if original and not original.endswith("\n") else "") + "\n".join(missing) + "\n",
                    encoding="utf-8",
                )
    return added, conflicts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="既存案件のルートディレクトリ")
    parser.add_argument("--apply", action="store_true", help="競合のないファイルと .gitignore の不足行を追加")
    args = parser.parse_args()
    try:
        added, conflicts = install(SOURCE_ROOT, args.target, args.apply)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print("適用結果" if args.apply else "dry-run（変更なし）")
    for path in added:
        print(f"追加: {path}")
    for path in conflicts:
        print(f"競合（変更なし）: {path}")
    return 1 if conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main())