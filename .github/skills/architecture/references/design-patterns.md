# アーキテクチャ設計 リファレンス

> **既定提案**: 検証導入パッケージでは、まず Teams / Microsoft 365 Copilot を入口にした対話型パターンを第一候補にする。
> 画面 UI が本当に必要な場合は Canvas App を基本案とし、利用するデータ・コネクタのライセンスを確認する。Canvas App では仕様・技術要件を満たすのが難しい場合、Code Apps / Model-Driven Apps も代替候補として提案し、実現性・ライセンス・費用を確認してユーザー承認後に採用を決める。

## 7. 統合アーキテクチャパターン集

### パターン A: 必要時の業務アプリ（Canvas App + 通知）

```
[採用済みデータソース] ←→ [Canvas App]  ← ユーザーがデータ操作
      ↓ レコード変更
[Power Automate] → メール/Teams 通知
```

**使うスキル**: `canvas-app` → `power-automate`（データソース・コネクタのライセンスを確認）

### パターン A2: 追加ライセンス承認時の例外案（Model-Driven + 通知）

```
[Dataverse] ←→ [Model-Driven Apps]  ← テーブル定義から自動生成 UI
      ↓ レコード変更
[Power Automate] → メール/Teams 通知
```

**使うスキル**: `model-driven-app` → `power-automate`

> **パターン A vs A2 の判断**: A を基本案とする。Canvas App では要件を満たすのが難しい場合に A2 も代替候補として提示し、Dataverse のライセンス条件・実現性・費用を確認してユーザー承認後に採用を決める。

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

### パターン E: 追加条件を要する拡張業務システム

```
[Dataverse]
    ↑↓
[Canvas App] ←→ ユーザー操作（画面が必要な場合）
    ↓ レコード変更
[Power Automate] → 通知 / 承認 / 外部連携
    ↓
[Copilot Studio] ← Teams から対話
    ↓
[AI Builder] ← エージェントのツールとして分析
```

**使うスキル**: 全フェーズスキルを順番に適用

> **位置づけ**: パターン E は拡張パターンとして扱う。Canvas App では仕様・技術要件を満たしにくい場合の代替候補として、Dataverse 等のライセンスと利用条件を確認して提案し、明示承認後に採用する。

---

## 8. 設計アウトプットテンプレート

このスキルで判断した結果は、以下のテンプレートでユーザーに提示する:

```markdown
## アーキテクチャ設計書

### 0. Phase 0 実現可能性判定

採用する重要経路ごとに、[開発着手前の実現可能性ゲート](../../standard/references/power-platform-development-standard.md)の判定表を記入するか、判定表の保存先を示す。公式根拠 URL・確認日、想定最大規模との照合、利用者・実行主体のライセンス、Copilot Credits、必要な実機検証結果と代替案を記録する。

- 判定表または参照先: {記入 / 要確認}
- 未確認・不適合の重要経路と対応: {内容 / なし / 要確認}
- 採用構成・例外案の承認者と承認結果: {記入 / 要確認}

未確認・不適合の重要経路が残る場合は本実装に進まず、代替案または最小限の実機検証を先に扱う。

### 1. 要件サマリー

- 開発段階: {PoC / MVP / 本番 / その他 / 要確認}
- 検証目的・仮説（PoC / MVP の場合）: {何を確かめるか}
- 対象範囲 / 対象外・後続判断事項: {今回実施することと、今回扱わないこと}
- 管理対象: {何を管理するか}
- 主なユーザー: {誰が使うか}
- 主要操作: {何をするか}

PoC / MVP の場合は、この段階で確かめる内容と本番化時に改めて判断する事項を分ける。フローを含む構成は、目的達成と必要な検証に必要な処理に絞り、検証結果を本番運用の保証として扱わない。

### 2. アーキテクチャパターン

**パターン {A/B/C/D/E}**: {パターン名}

### 3. コンポーネント構成

| コンポーネント             | 用途                                     | 必要性  |
| -------------------------- | ---------------------------------------- | ------- |
| Teams / M365 Copilot       | {入口 / チャネルの概要}                  | ✅ / ❌ |
| Dataverse カスタムテーブル | {採用する場合のテーブル構成}             | ✅ / ❌ |
| Canvas App                 | {必要時の画面・利用データの概要}         | ✅ / ❌ |
| Code Apps（代替案）        | {Canvas App では難しい要件・画面の概要}  | ✅ / ❌ |
| Model-Driven（代替案）     | {必要な場合のアプリ概要・ライセンス条件} | ✅ / ❌ |
| Power Automate             | {フローの概要}                           | ✅ / ❌ |
| Copilot Studio             | {エージェントの概要}                     | ✅ / ❌ |
| AI Builder                 | {プロンプトの概要}                       | ✅ / ❌ |

### 4. 判断根拠

- {なぜこのコンポーネントを選んだか}
- {Canvas App では満たしにくい要件、代替案の実現性・ライセンス・費用・承認状況、または代替案を選ばなかった理由}

### 5. 構築フェーズ

1. Phase 1: Dataverse カスタムテーブル — {テーブル数}テーブル（※ 採用時のみ）
2. Phase 2: Copilot Studio / Teams / M365 Copilot — {対話 UI の概要}（※ 不要なら省略）
3. Phase 2: Canvas App — {画面数}画面（※ 画面 UI が必要な場合のみ）
4. Phase 2: Code Apps — {画面数}画面（※ Canvas App では難しい場合のみ。実現性・ライセンス・費用を確認し、明示承認後に採用）
5. Phase 2: Model-Driven Apps — テーブルから自動生成（※ Canvas App では難しい場合に代替提案し、ライセンス確認・明示承認後）
6. Phase 2.5: Power Automate — {フロー数}フロー（※ 不要なら省略）
7. Phase 3: Copilot Studio — {エージェント数}エージェント（※ 不要なら省略）
8. Phase 4: AI Builder — {プロンプト数}プロンプト（※ 不要なら省略）

この設計で進めてよいですか？
```

---

## 9. よくある判断ミスと対策

| ミス                                                             | 正しい判断                                                                                          |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 通知だけなのに Copilot Studio を使う                             | Power Automate 単体で十分。LLM が不要なら使わない                                                   |
| 確定的な処理に Copilot Studio を使う                             | 条件分岐が固定なら Power Automate。LLM のハルシネーションリスクを避ける                             |
| Power Automate で自然言語処理を頑張る                            | Copilot Studio に任せる。フローの条件分岐で自然言語を扱うのは脆い                                   |
| AI Builder で対話機能を作ろうとする                              | Copilot Studio を使う。AI Builder は単発の入力→出力処理向き                                         |
| Canvas Apps で複雑な UI を作る                                   | Code Apps / Model-Driven Apps も代替候補として比較し、実現性・ライセンス・費用を確認する            |
| 標準 CRUD なら無条件に Model-Driven Apps を使う                  | まず Canvas App を基本案として検討し、難しい場合に Model-Driven Apps も提案。ライセンスと承認を確認 |
| 全要件に Copilot Studio を使う                                   | 対話が不要な部分は Power Automate / 必要時の Canvas App で扱う                                      |
| Power Automate フロー内に AI Builder アクションを API でデプロイ | API では `InvalidOpenApiFlow` エラー。AI Builder ステップは UI で手動追加                           |

---
