# Conversation Transcript 分析リファレンス

このリファレンスは、Copilot Studio の会話ログ（ConversationTranscript）を使って、エージェントの動作検証、会話の流れの確認、原因調査を行うための標準手順です。

主目的は、個別会話を探索的に調べて、期待したトピックやツール選択が起きたか、どこで失敗したか、どの分岐に進んだかを確認することです。大量ログの定型集計や可視化は、Copilot Studio 標準分析、CSV、Power BI などの手段と使い分けます。

---

## 1. 目的

- Copilot Studio エージェントの会話ログを用いて、動作検証、会話の流れの確認、問題の原因調査を行う
- 個別会話の探索を主用途とし、必要なレコードだけを少件数で取得する
- 大量集計や可視化は、Copilot Studio 標準分析、CSV、Power BI 等に分けて扱う

---

## 2. 対象範囲

- 対象: Copilot Studio が環境の Dataverse に保存した ConversationTranscript
- 対象外: Dataverse カスタムテーブルを用いた業務 DB の設計・構築
- 対象外: 会話ログの一括更新・削除
- 対象外: 顧客固有データ、実環境 URL、環境 ID、秘密情報をマスターへ保存すること

---

## 3. 前提条件

- Power Platform 環境に Dataverse がある
- ConversationTranscript が保存される環境構成である
- 会話ログ分析は Sandbox 環境を推奨する
- Developer 環境では ConversationTranscript が保存されない場合があるため、事前に保存条件を確認する
- 対象エージェントでテスト会話が実施されている
- 分析担当者に必要な Dataverse 権限と Bot Transcript Viewer ロールがある
- GitHub Copilot 拡張が利用可能
- Power Platform 環境側で Dataverse MCP Server が有効
- Copilot Studio は既定で有効なため、必要に応じて Microsoft GitHub Copilot などの追加クライアントを許可する
- Microsoft GitHub Copilot MCP クライアントが許可されている

---

## 4. Power Platform 環境側の設定

環境側の設定は、次の順で確認する。

1. Power Platform 管理センターで対象環境を開く
2. 製品 -> 機能 で Dataverse MCP Server を有効化する
3. 必要に応じて、詳細設定から許可する MCP クライアントを有効化する
4. 追加クライアントの一覧から Microsoft GitHub Copilot を有効にする
5. 必要な Dataverse 権限と Bot Transcript Viewer ロールを付与する

> この設定は環境側の機能であり、このリポジトリに Dataverse MCP Server 本体や実環境 URL を保存しない。

---

## 5. VS Code の GitHub Copilot への接続

Microsoft 公式の VS Code 手順を前提に、Dataverse MCP Server へ HTTP 接続する。

1. VS Code のコマンドパレットを開く
2. MCP: Add Server を選択する
3. HTTP または Server Sent Events を選択する
4. Dataverse 環境のインスタンス URL に /api/mcp を付けた URL を入力する
5. MCP Server 名を設定する
6. グローバルまたはワークスペースのスコープを選択する
7. GitHub Copilot Chat を Agent モードで使用する
8. 接続後に Dataverse MCP ツールが認識されることを確認する

### グローバルとワークスペースの使い分け

| 観点                 | グローバル                    | ワークスペース                          |
| -------------------- | ----------------------------- | --------------------------------------- |
| 共有範囲             | VS Code 全体                  | このリポジトリのみ                      |
| 誤接続リスク         | 複数案件で混同しやすい        | 案件を分けやすい                        |
| マスター運用との相性 | 実環境 URL を広く保持しやすい | 実環境 URL を案件側へ閉じやすい         |
| 推奨                 | 例外的                        | このマスター / 案件運用ではこちらを優先 |

このマスターでは、顧客固有または案件固有の環境 URL をリポジトリへ固定保存しない方針のため、ワークスペース設定を使う場合でも実 URL はコミットしない。共有が必要なら、.gitignore で除外したローカル設定として扱うか、プレースホルダーのみのサンプルを使う。

MCP 許可リストは /api/mcp エージェントエントリポイントにのみ適用される。通常の Dataverse API や MCP 名のカスタム API は、この設定の影響を受けない。

---

## 6. MCP 構成サンプル

実環境値を含まないサンプルは、次の構造を参考にする。

```json
{
  "servers": {
    "DataverseMcp": {
      "type": "http",
      "url": "<YOUR_DATAVERSE_ORG_URL>/api/mcp"
    }
  }
}
```

このリポジトリでは、実設定ファイルを新設しない。VS Code の UI 手順で登録し、必要に応じてプレースホルダー付きサンプルを参照する。

---

## 7. 外部 dataverse Agent Plugin

- 外部の dataverse Agent Plugin と、リポジトリ内の .github/skills/dataverse/ は別物
- Plugin はこのリポジトリに同梱しない
- Plugin は GitHub Copilot または Copilot CLI 側へ別途導入する
- Plugin には、接続、メタデータ、データ、クエリ、ソリューション、MCP 構成支援などが含まれる
- mcp-configure は Dataverse MCP 接続設定を対話形式で支援する
- Plugin を使っても、Power Platform 環境側の Dataverse MCP 有効化、許可クライアント、権限設定は別途必要
- Plugin がなくても Microsoft 公式の MCP: Add Server 手順で接続できる
- Plugin の導入可否で、リポジトリ内の標準やスキルが置き換わるわけではない
- 公式ドキュメントでは、Microsoft 以外の MCP クライアントを有効にするには環境側の許可設定が必要とされる

---

## 8. ConversationTranscript の探索手順

固定のテーブル名、列名、論理名を推測で断定せず、最初に MCP でメタデータを確認する。

推奨する探索順序:

1. 対象環境、対象エージェント、対象期間、調査目的を確認する
2. search で ConversationTranscript に該当するテーブルやメタデータを探す
3. describe でテーブル、列、論理名、取得可能な項目を確認する
4. 実環境で確認した論理名を使って read_query 用の SELECT を組み立てる
5. まず少件数、読み取り専用で実行する
6. 必要なレコードだけ取得する
7. 取得内容を時系列、会話単位、問題パターンで整理する
8. 分析結果と事実データを区別する

未確認の列名や JSON 構造を完成クエリとして断定しない。必要なら、MCP にクエリ案を作らせて人が確認してから実行する。

---

## 9. 安全なクエリテンプレート

以下はテンプレートであり、実環境依存の論理名は describe の結果に置き換える。

### 9.1 最近のテスト会話を少件数だけ取得

- 目的: 最近のテスト会話を少件数だけ確認する
- 事前確認: transcript テーブル名、作成日時列、対象エージェント列
- プレースホルダー: {transcript_table}, {createdon_column}, {agent_column}
- 件数制限: 小さく保つ。まずは 5 件前後
- 実行条件: 読み取り専用
- 注意: 個人情報や本文の全文出力を避ける

```sql
SELECT TOP 5
  <createdon_column>,
  <agent_column>,
  <session_column>
FROM <transcript_table>
ORDER BY <createdon_column> DESC
```

### 9.2 対象エージェントを絞る

- 目的: 特定エージェントの会話だけを見る
- 事前確認: agent 名、agent reference 列、等価比較できる論理名
- プレースホルダー: {agent_filter_column}, {agent_value}
- 件数制限: 必須。少件数で確認する
- 実行条件: 読み取り専用
- 注意: 先に describe で列の型を確認する

```sql
SELECT TOP 10
  <createdon_column>,
  <agent_filter_column>,
  <session_column>
FROM <transcript_table>
WHERE <agent_filter_column> = <agent_value>
ORDER BY <createdon_column> DESC
```

### 9.3 対象期間を絞る

- 目的: 調査期間を限定する
- 事前確認: 日時列、比較に使う形式
- プレースホルダー: {start_datetime}, {end_datetime}
- 件数制限: 必須。期間は短く区切る
- 実行条件: 読み取り専用
- 注意: SQL 方言は環境で確認する。未確認の関数を完成形にしない

```sql
SELECT TOP 10
  <createdon_column>,
  <session_column>
FROM <transcript_table>
WHERE <createdon_column> >= <start_datetime>
  AND <createdon_column> < <end_datetime>
ORDER BY <createdon_column> ASC
```

### 9.4 特定のセッションまたは会話 ID を調べる

- 目的: 1 つの会話を時系列で追う
- 事前確認: session ID / conversation ID 列
- プレースホルダー: {session_id}, {session_column}
- 件数制限: 1 セッションに限定する
- 実行条件: 読み取り専用
- 注意: 同一会話の複数レコードの粒度を describe で確認する

```sql
SELECT
  <createdon_column>,
  <session_column>,
  <content_column>
FROM <transcript_table>
WHERE <session_column> = <session_id>
ORDER BY <createdon_column> ASC
```

### 9.5 エラー、失敗、エスカレーション候補を探す

- 目的: 問題会話の候補を拾う
- 事前確認: status、error、escalation に相当する列
- プレースホルダー: {status_column}, {error_column}
- 件数制限: 小さく保つ
- 実行条件: 読み取り専用
- 注意: 値の意味は環境のメタデータで確認する

```sql
SELECT TOP 20
  <createdon_column>,
  <status_column>,
  <error_column>,
  <session_column>
FROM <transcript_table>
WHERE <status_column> IS NOT NULL
   OR <error_column> IS NOT NULL
ORDER BY <createdon_column> DESC
```

### 9.6 Content 等の JSON を含むログを時系列で整理する

- 目的: 会話の流れを順番に再現する
- 事前確認: Content 系列の列、JSON 列の実体、必要最小限の項目
- プレースホルダー: {content_column}
- 件数制限: 1 セッションまたは少数件
- 実行条件: 読み取り専用
- 注意: 本文の原文を不要に残さない

```sql
SELECT
  <createdon_column>,
  <session_column>,
  <content_column>
FROM <transcript_table>
WHERE <session_column> = <session_id>
ORDER BY <createdon_column> ASC
```

---

## 10. GitHub Copilot への分析依頼テンプレート

以下は、Copilot への依頼文の雛形である。各テンプレートは、対象環境、対象エージェント、対象期間またはセッション、調査目的、読み取り専用、メタデータ先行、書き込み禁止、列名を推測しない、件数を制限する、事実と解釈を分ける、を満たすように作っている。

### 10.1 接続・メタデータ確認

```text
対象環境: {environment}
対象エージェント: {agent}
対象期間: {period}
目的: ConversationTranscript のメタデータと取得可能な項目を確認したいです。
条件: 読み取り専用で、最初にメタデータを確認してください。書き込み、更新、削除は禁止です。不明な列名は推測せず、describe の結果だけを使ってください。取得件数は最小限にしてください。事実、解釈、次の確認事項を分けて説明してください。
```

### 10.2 最近のテスト会話の一覧化

```text
対象環境: {environment}
対象エージェント: {agent}
対象期間: {period}
目的: 最近のテスト会話を少件数だけ一覧化したいです。
条件: 読み取り専用です。最初にメタデータを確認し、会話ログの論理名を確定してからクエリ案を作ってください。書き込み、更新、削除は禁止です。取得件数を絞り、個人情報や本文の全文出力を避けてください。事実、解釈、改善候補を分けてください。
```

### 10.3 特定セッションの時系列整理

```text
対象環境: {environment}
対象エージェント: {agent}
対象セッション: {session_id}
目的: 1 件の会話を時系列で整理したいです。
条件: 読み取り専用です。最初にメタデータを確認し、不明な列名は推測しないでください。書き込み、更新、削除は禁止です。取得件数を 1 セッションに限定し、事実と解釈を分けてください。
```

### 10.4 期待したトピック／ツールが選択されなかった原因の調査

```text
対象環境: {environment}
対象エージェント: {agent}
対象期間またはセッション: {period_or_session}
目的: 期待したトピックやツールが選択されなかった原因を調べたいです。
条件: 読み取り専用です。最初にメタデータを確認し、関係しそうな列だけを少件数で取得してください。書き込み、更新、削除は禁止です。事実、原因候補、次の確認事項を分けてください。
```

### 10.5 エラーまたは失敗会話の共通点整理

```text
対象環境: {environment}
対象エージェント: {agent}
対象期間: {period}
目的: エラーや失敗が出た会話の共通点を整理したいです。
条件: 読み取り専用です。最初にメタデータを確認し、対象列を確定してください。書き込み、更新、削除は禁止です。取得件数は最小限にし、個人情報の出力は必要最小限にしてください。事実、共通点、原因候補を分けてください。
```

### 10.6 修正前後の会話ログ比較

```text
対象環境: {environment}
対象エージェント: {agent}
対象期間: 修正前 {before_period} / 修正後 {after_period}
目的: 修正前後で会話ログの違いを比較したいです。
条件: 読み取り専用です。最初にメタデータを確認し、比較に使う列名を確定してください。書き込み、更新、削除は禁止です。件数を絞り、事実、差分、改善案を分けてください。
```

### 10.7 テスト結果を受入基準と照合

```text
対象環境: {environment}
対象エージェント: {agent}
対象期間またはセッション: {period_or_session}
目的: 会話ログが受入基準を満たしているか確認したいです。
条件: 読み取り専用です。最初にメタデータを確認し、必要な最小項目だけを取得してください。書き込み、更新、削除は禁止です。事実、受入基準との一致、不一致、未確認事項を分けてください。
```

### 10.8 取得した JSON / Content の構造説明

```text
対象環境: {environment}
対象エージェント: {agent}
対象セッション: {session_id}
目的: 取得した JSON または Content の構造を説明したいです。
条件: 読み取り専用です。最初にメタデータを確認し、Content の実体と列名を確定してください。書き込み、更新、削除は禁止です。個人情報を伏せ、事実、構造、解釈を分けてください。
```

### 10.9 個人情報を伏せた分析レポート作成

```text
対象環境: {environment}
対象エージェント: {agent}
対象期間またはセッション: {period_or_session}
目的: 個人情報を伏せた分析レポートを作成したいです。
条件: 読み取り専用です。最初にメタデータを確認し、取得件数を制限してください。書き込み、更新、削除は禁止です。事実、解釈、改善案を分け、顧客名、個人名、メールアドレス、テナント URL、環境 ID は出力しないでください。
```

---

## 11. 分析結果の出力形式

分析結果は、次の区分で出力する。

- 対象・条件
- 確認した会話ログ
- 観測された事実
- 原因候補
- 未確認事項
- 修正案
- 再テスト項目

原因を断定できない場合は、原因候補として扱い、ログ上の根拠を示す。

---

## 12. ガードレール

- 原則として search、search_data、describe、read_query のみ使用する
- create_record、update_record、delete_record、create_table、update_table、delete_table などの変更系ツールは、この会話ログ分析手順では使用しない
- 書き込み要求が出た場合は実行せず、目的、対象、承認を確認する
- 大量取得を避ける
- 対象エージェントと対象環境を実行前に確認する
- 実行するクエリを利用者へ提示し、確認後に実行する
- 会話ログの原文を不要にリポジトリへ保存しない
- 顧客名、個人名、メールアドレス、テナント URL、環境 ID 等をサンプルへ残さない
- 分析結果をコミットする場合は、匿名化、要約、汎用化した内容だけにする

---

## 13. トラブルシューティング

### 13.1 MCP ツールが表示されない

- 確認対象: VS Code の MCP サーバー設定、Agent モード、Copilot 拡張の有効状態
- 次に見る公式リンク: Dataverse MCP Server の概要、VS Code での MCP 接続方法

### 13.2 認証を求められる

- 確認対象: GitHub Copilot のサインイン、環境側の許可クライアント、権限
- 次に見る公式リンク: Dataverse MCP Server の環境構成、VS Code 接続手順

### 13.3 対象テーブルが見つからない

- 確認対象: search の結果、describe の対象、環境の選択
- 次に見る公式リンク: Dataverse MCP Server の概要、Conversation Transcript の理解とエクスポート

### 13.4 ConversationTranscript にログがない

- 確認対象: 環境種類、Developer 環境の制約、テスト会話の有無
- 次に見る公式リンク: Conversation Transcript の理解とエクスポート、Copilot Studio の分析方針

### 13.5 権限不足

- 確認対象: Dataverse 権限、Bot Transcript Viewer、環境ロール
- 次に見る公式リンク: Conversation Transcript の理解とエクスポート、Dataverse MCP Server の環境構成

### 13.6 MCP クライアントが許可されていない

- 確認対象: 許可済み MCP クライアント、microsoftgithubcopilot の有効化
- 次に見る公式リンク: Dataverse MCP Server の環境構成

### 13.7 Developer 環境を使用している

- 確認対象: 環境種類、ConversationTranscript の保存条件
- 次に見る公式リンク: Conversation Transcript の理解とエクスポート

### 13.8 VS Code と Copilot CLI の構成ファイルを混同している

- 確認対象: VS Code の MCP 設定と Copilot CLI 用設定の分離
- 次に見る公式リンク: VS Code での MCP 接続方法、Dataverse MCP Server の概要

### 13.9 旧 MCP ツール名を使っている

- 確認対象: search_data、search、read_query、describe への読み替え
- 次に見る公式リンク: Dataverse MCP Server の概要

---

## 14. 公式リンク

- [モデル コンテキスト プロトコルで Dataverse に接続する (MCP)](https://learn.microsoft.com/ja-jp/power-apps/maker/data-platform/data-platform-mcp)
- [Dataverse モデル コンテキスト プロトコル (MCP) サーバーを構成する](https://learn.microsoft.com/ja-jp/power-apps/maker/data-platform/data-platform-mcp-disable)

必要に応じて、上記の Microsoft Learn 内で示される関連ページも参照する。
