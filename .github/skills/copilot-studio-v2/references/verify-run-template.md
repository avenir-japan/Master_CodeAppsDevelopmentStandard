# verify スクリプト実行テンプレート

Copilot Studio v2 の設定変更後に、公開前チェックとして実行する最小テンプレート。

## 1. 事前準備

- `.env` に Dataverse 接続情報を設定済みであること
- 対象 Bot の ID を確認済みであること

## 2. Bot ID を指定する

PowerShell 例:

```powershell
$env:AGENT_BOTID = "00000000-0000-0000-0000-000000000000"
```

または、リポジトリルートに `agent_botid.txt` を作成して Bot ID を1行で記載する。

単発で実行するだけなら、各コマンドに `--bot-id` を付けてもよい。

## 3. 設定整合を検証する

```powershell
py -3 .github/skills/copilot-studio-v2/scripts/verify_config.py
```

```powershell
py -3 .github/skills/copilot-studio-v2/scripts/verify_config.py --bot-id "00000000-0000-0000-0000-000000000000"
```

確認観点:

- BotConfiguration の主要キー
- model / instructions / memory などの必須設定

## 4. エージェント全体を検証する

```powershell
py -3 .github/skills/copilot-studio-v2/scripts/verify_agent.py
```

```powershell
py -3 .github/skills/copilot-studio-v2/scripts/verify_agent.py --bot-id "00000000-0000-0000-0000-000000000000"
```

確認観点:

- botcomponents の一覧と type=14 filedata の読み取り可否（実行・公開状態や接続の健全性までは判定しない）

## 5. 採用経路の実行確認（対象環境での承認後）

設計で選んだ Teams / Microsoft 365 Copilot チャネルから代表入力を送り、期待する応答と必要なツール・エージェントフローの入出力、接続・実行主体を確認する。公開後の利用権、容量、Credits の適用条件は [共通のライセンス確認ルール](../../standard/references/license-requirements.md)に沿って確認する。これらを実施できない場合は「設定の読み取り確認のみ、実行未確認」と記録し、公開後の動作を保証しない。

## 6. 失敗時の切り分け

- `AGENT_BOTID 未設定`:
  - 環境変数 `AGENT_BOTID` か `agent_botid.txt` を設定する
- `401/403`:
  - 認証・権限・対象環境を再確認する
- `filedata が読めない`:
  - スキル同梱ファイルの登録状態を確認する
