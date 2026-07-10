# アーキテクチャ設計 リファレンス

> **既定提案**: 検証導入パッケージでは、まず Teams / Microsoft 365 Copilot を入口にした対話型パターンを第一候補にする。
> 画面 UI が必要な場合のみ Canvas App を優先的に検討し、Code Apps やその他の拡張パターンは案件要件と追加ライセンス評価に応じて採用する。

## 7. 統合アーキテクチャパターン集

### パターン A: 必要時の業務アプリ（Canvas App / Code Apps + 通知）

```
[Dataverse] ←→ [Canvas App / Code Apps]  ← ユーザーがデータ操作
      ↓ レコード変更
[Power Automate] → メール/Teams 通知
```

**使うスキル**: `code-apps` / `canvas-app` → `power-automate`

### パターン A2: 業務アプリ（Model-Driven + 通知）

```
[Dataverse] ←→ [Model-Driven Apps]  ← テーブル定義から自動生成 UI
      ↓ レコード変更
[Power Automate] → メール/Teams 通知
```

**使うスキル**: `model-driven-app` → `power-automate`

> **パターン A vs A2 の判断**: カスタム UI が不要で標準ビュー/フォームで十分なら A2（最速）。
> 画面 UI が必要で、まずベースライセンス範囲内を優先するなら A の Canvas App、カンバン・ダッシュボード・カスタムビジュアルが必要なら A の Code Apps を比較する。

### パターン B: 標準対話 UI（Teams / M365 Copilot + ナレッジ）

```
[Teams / Web] → [Copilot Studio]
                    ↓
              [Dataverse ナレッジ] + [SharePoint ナレッジ]
```

**使うスキル**: `copilot-studio`

### パターン C: イベント駆動 AI 処理（トリガー + エージェント）

```
[メール受信 / スケジュール]
      ↓
[Power Automate] → ExecuteCopilot
      ↓
[Copilot Studio] → ツール呼び出し（MCP / コネクタ）
      ↓
応答処理（メール返信 / Teams 投稿）
```

**使うスキル**: `copilot-studio`（[trigger.md](../../copilot-studio/references/trigger.md) を参照）

### パターン D: 定期レポート配信

```
[Power Automate: Recurrence トリガー]
      ↓
[Copilot Studio] → RSS/Web 検索 → レポート生成 → メール送信
```

**使うスキル**: `copilot-studio`（[market-research-report.md](../../copilot-studio/references/market-research-report.md) を参照）

### パターン E: 拡張フルスタック業務システム

```
[Dataverse]
    ↑↓
[Code Apps] ←→ ユーザー操作
    ↓ レコード変更
[Power Automate] → 通知 / 承認 / 外部連携
    ↓
[Copilot Studio] ← Teams から対話
    ↓
[AI Builder] ← エージェントのツールとして分析
```

**使うスキル**: 全フェーズスキルを順番に適用

> **位置づけ**: パターン E は拡張パターンとして扱う。検証導入パッケージの既定提案ではなく、要件と追加ライセンス評価に応じて採用する。

---

## 8. 設計アウトプットテンプレート

このスキルで判断した結果は、以下のテンプレートでユーザーに提示する:

```markdown
## アーキテクチャ設計書

### 1. 要件サマリー

- 管理対象: {何を管理するか}
- 主なユーザー: {誰が使うか}
- 主要操作: {何をするか}

### 2. アーキテクチャパターン

**パターン {A/B/C/D/E}**: {パターン名}

### 3. コンポーネント構成

| コンポーネント | 用途                 | 必要性  |
| -------------- | -------------------- | ------- |
| Teams / M365 Copilot | {入口 / チャネルの概要} | ✅ / ❌ |
| Dataverse      | {テーブル構成の概要} | ✅ 必須 |
| Code Apps      | {画面の概要}         | ✅ / ❌ |
| Canvas App     | {画面の概要}         | ✅ / ❌ |
| Model-Driven   | {アプリの概要}       | ✅ / ❌ |
| Power Automate | {フローの概要}       | ✅ / ❌ |
| Copilot Studio | {エージェントの概要} | ✅ / ❌ |
| AI Builder     | {プロンプトの概要}   | ✅ / ❌ |

### 4. 判断根拠

- {なぜこのコンポーネントを選んだか}
- {なぜ代替案を選ばなかったか}

### 5. 構築フェーズ

1. Phase 1: Dataverse — {テーブル数}テーブル
2. Phase 2: Copilot Studio / Teams / M365 Copilot — {対話 UI の概要}（※ 不要なら省略）
3. Phase 2: Canvas App — {画面数}画面（※ 不要なら省略）
4. Phase 2: Code Apps — {画面数}画面（※ 不要なら省略）
5. Phase 2: Model-Driven Apps — テーブルから自動生成（※ Canvas App / Code Apps と排他）
6. Phase 2.5: Power Automate — {フロー数}フロー（※ 不要なら省略）
7. Phase 3: Copilot Studio — {エージェント数}エージェント（※ 不要なら省略）
8. Phase 4: AI Builder — {プロンプト数}プロンプト（※ 不要なら省略）

この設計で進めてよいですか？
```

---

## 9. よくある判断ミスと対策

| ミス                                                             | 正しい判断                                                                 |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------- |
| 通知だけなのに Copilot Studio を使う                             | Power Automate 単体で十分。LLM が不要なら使わない                          |
| 確定的な処理に Copilot Studio を使う                             | 条件分岐が固定なら Power Automate。LLM のハルシネーションリスクを避ける    |
| Power Automate で自然言語処理を頑張る                            | Copilot Studio に任せる。フローの条件分岐で自然言語を扱うのは脆い          |
| AI Builder で対話機能を作ろうとする                              | Copilot Studio を使う。AI Builder は単発の入力→出力処理向き                |
| Canvas Apps で複雑な UI を作る                                   | Code Apps に切り替える。ドラッグ&ドロップのカンバンは Canvas Apps では困難 |
| 標準 CRUD だけなのに Code Apps でフルスクラッチ                  | Model-Driven Apps なら自動生成で最速。カスタム UI 不要なら MDA を検討      |
| 全要件に Copilot Studio を使う                                   | 対話が不要な部分は Power Automate / Code Apps で。適材適所                 |
| Power Automate フロー内に AI Builder アクションを API でデプロイ | API では `InvalidOpenApiFlow` エラー。AI Builder ステップは UI で手動追加  |

---
