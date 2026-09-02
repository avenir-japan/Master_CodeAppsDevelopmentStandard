# SDK 更新検知

Power Platform 関連 SDK と upstream 公式 skills の更新は、`.github/scripts/check-sdk-updates.mjs` で定期点検する。
このチェックは、依存更新そのものを自動適用するものではなく、**採用判断の材料を機械的に集める**ための標準手順。

## 対象

- npm パッケージの最新バージョン差分
- upstream skills リポジトリの更新差分
- 既存 Issue との重複回避マーカー

## 使い方

### help

```powershell
node .github/scripts/check-sdk-updates.mjs --help
```

### dry-run

```powershell
$env:ISSUE_REPOSITORY = "owner/repo"
$env:DRY_RUN = "true"
node .github/scripts/check-sdk-updates.mjs
```

### test

```powershell
node .github/scripts/check-sdk-updates.test.mjs
```

### Issue 作成モード

```powershell
$env:ISSUE_REPOSITORY = "owner/repo"
$env:GH_TOKEN = "<token>"
node .github/scripts/check-sdk-updates.mjs
```

必要な環境変数の雛形は `.github/scripts/check-sdk-updates.env.example` を参照する。

## 運用ルール

1. まず dry-run で差分内容を確認する。
2. 未追跡の更新があっても、即採用せず破壊的変更・CLI help・テンプレート互換性を確認する。
3. Issue 作成はトークン設定後に行う。トークン未設定での通常実行はしない。
4. 更新候補を標準へ取り込む場合は、`update-skills` の検証手順とあわせて扱う。