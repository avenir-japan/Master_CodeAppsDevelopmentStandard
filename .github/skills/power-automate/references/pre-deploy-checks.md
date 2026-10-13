# クラウドフローのデプロイ前チェック

## 対象と実行

Power Automate UI で保存できた最小フローから取得した定義を拡張した後、**送信する最終定義**を JSON に書き出す。
`properties.definition` を含むエクスポート形式、または定義オブジェクト単体を指定できる。

```powershell
python .github/skills/power-automate/scripts/validate_flow_definition.py path/to/flow-definition.json
```

終了コード 0 のときだけ次に進む。現時点で検査するのは、`contentBase64` が空値でないことと、
実行時式を渡す場合に `@base64(...)` で始まることのみ。Dataverse の行パラメータや
テーブル・列・Lookup は**検査対象外**であり、Dataverse を採用した案件でだけ別途確認する。
静的検査は式の実行結果や、文字列リテラルが正しい Base64 かまでは判定しない。

## 次の確認ゲート

1. 対象環境で接続参照が解決し、意図したソリューションに含まれるか確認する。
2. デザイナーで保存し、公開または有効化できるか確認する。
3. テスト実行の run を特定して、トリガー・アクション・業務出力を照合する。

定義検査、保存、公開、実行の成功を混同しない。エラー時は
[コードファースト実装ガイド](code-first-flow-authoring.md)のゲートごとに原因を切り分ける。
Canvas App を使う案件では `sync_canvas` / `compile_canvas` の検証後に Designer で Save / Publish し、
Copilot Studio を使う案件では公開前の設定検証と利用者視点の動作確認を別に実施する。
