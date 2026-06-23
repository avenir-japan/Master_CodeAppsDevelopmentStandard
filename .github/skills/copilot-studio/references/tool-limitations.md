# Copilot Studio ツール制限とワークアラウンド

## バイナリドキュメントのツール間受け渡し制限（重要）

### 制限事項

Copilot Studio の生成オーケストレーション（Generative Orchestration）モードでは、
**バイナリデータ（PDF、画像など）をツール間で直接受け渡すことができない**。

#### 動作しないパターン

```
ユーザー → [Tool A: ファイル受信] → (バイナリ) → [Tool B: AI 分析]
                                       ↑
                                このバイナリ受け渡しが不可
```

例: ファイルアップロードツールで受け取った PDF を AI Builder プロンプトに渡す

#### 症状

- Tool A の出力（バイナリ）を Tool B で参照できない
- エージェントがバイナリを「テキスト」として扱おうとする
- AI Builder でドキュメント分析できない

### 解決策: Power Automate フローで処理を統合

バイナリを受け取り → AI 分析 → テキスト結果を返す、を単一フローで完結させる。

```
ユーザー → [単一フロー: ファイル受信 + AI 分析] → テキスト結果 → エージェント
```

#### 推奨アーキテクチャ

```python
# 1 つのフローで完結
{
    "triggers": {
        "PowerApps_V2_トリガー": {
            # ファイルとメタデータを同時に受け取る
            "inputs": {
                "schema": {
                    "file_name": "string",
                    "file_content": "string",  # base64
                }
            }
        }
    },
    "actions": {
        "AI_Builder_プロンプト実行": {
            # 同一フロー内でバイナリを AI Builder に渡す
        },
        "PowerApp応答": {
            # テキスト結果のみ返す（バイナリは返さない）
        }
    }
}
```

### 対比: テキストデータは問題なし

テキストベースのデータは複数ツール間で正常に受け渡しできる。

```
✅ ユーザー → [Tool A: テキスト取得] → (string) → [Tool B: 分析]
```

## ツール呼び出し順序の制御

### 制限事項

Generative Orchestration モードでは、エージェントがツール呼び出し順序を自律的に決定する。
開発者が明示的に「Tool A → Tool B」の順序を強制することは難しい。

### ワークアラウンド

1. **単一ツールに統合**: 依存関係のある処理は 1 つのフロー/ツールにまとめる
2. **Instructions で誘導**: 「まず〇〇を確認してから△△を実行してください」と記述
3. **Conditional Routing** は未サポート（Classic モード機能）

## ツール出力の型制限

### サポートされる出力型

| 型 | サポート | 備考 |
|---|---|---|
| string | ✅ | 最も信頼性が高い |
| number | ✅ | |
| boolean | ✅ | |
| object (JSON) | ⚠️ | エージェントが正しく解釈しない場合あり |
| array | ⚠️ | 同上 |
| binary | ❌ | バイナリはテキストに変換して返す |

### 推奨: JSON 文字列で返す

複雑なデータはツール側で JSON 文字列化し、エージェントに解釈させる。

```python
"PowerApp応答": {
    "inputs": {
        "body": {
            "result": "@{string(outputs('AI_Result'))}"  # JSON 文字列
        }
    }
}
```

エージェント Instructions で解釈方法を指示:

```yaml
instructions: |
  ReceiptUpload ツールの result は JSON 文字列です。
  以下のフィールドを抽出して報告してください:
  - store_name: 店舗名
  - total_amount: 合計金額
  - date: 日付
```

## 関連リファレンス

- [Power Automate 連携パターン](../../power-automate/references/trigger-action-patterns.md)
- [AI Builder 統合](../../ai-builder/references/power-automate-integration.md)
