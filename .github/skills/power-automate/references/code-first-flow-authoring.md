# Power Automate コードファースト実装ガイド

## 目的

Power Automate フローを pac / clone / export した定義で保守する場合、
コネクタの動的パラメータ、UI の解釈、公開時バリデーションの差で、
JSON が正しく見えてもデザイナーや publish で崩れることがある。

この文書は、コードファーストで Modern Flow を扱うときの実装順序と、
切り分けの優先順位をまとめる。

## 1. 最小雛形を UI で成立させてから clone する

コードベース実装の基本は、UI で保存可能な最小フローを先に成立させ、
その定義を clone して拡張すること。

### 原則

- まず Power Automate UI で最小フローを保存可能な状態まで作る
- その後に pac / clone / export で定義を取得する
- 取得した action 名、operationId、parameter shape、connectionReferences を正本として保持する
- 拡張時は既存 action を作り直すより、既存定義の近傍へ追加する

### 向いている場面

- Modern Flow をソリューション配下でコード管理する場合
- コネクタの動的パラメータ形が UI 依存で揺れやすい場合
- 既存フローの action 名や接続参照を壊さず拡張したい場合

### 避けること

- UI で一度も成立していないコネクタアクションを、JSON だけでゼロから合成する
- clone 済み定義の shape を無視して action を作り直す

## 2. import / save / publish は別ゲートとして診断する

Power Automate の実装では、次の 3 つを別の検証ゲートとして扱う。

1. import / pack が通るか
2. デザイナーで save できるか
3. publish できるか

### import / pack が通るか

- ソリューション構造
- JSON 構文
- connectionReferences の整合性
- XML / solution metadata の整合性

### save できるか

- action の配置制約
- 動的パラメータ shape
- UI が action をどう解釈しているか
- Scope / variable / runAfter の組み合わせ

### publish できるか

- コネクタの operationSchema
- 接続解決
- 公開時バリデーション
- save 済み定義と公開時に許可される定義の差

### 典型例

- import は成功、save は成功、publish だけ失敗
  - JSON 構文よりコネクタ定義や operationSchema を疑う
- import は成功、デザイナーで赤エラー
  - UI が期待する parameter shape と clone 定義の差を疑う

pack / import 成功だけをもって「フローは正しい」と判断しないこと。

### 呼び出し元への応答は実行経路ごとに確認する

エージェントやアプリなど、呼び出し元が同期的な結果を必要とするフローでは、
save / publish に加え、成功・条件不一致・処理失敗の各経路を実際に通して応答を確認する。
応答を返さない設計のフローには適用しない。

- 条件分岐の `else` が空のまま、呼び出し元への応答を欠いていないか確認する
- 先行アクションが失敗またはスキップされたとき、失敗応答まで到達できる `runAfter` か確認する
- 各経路で呼び出し元が期待する結果を受け取れることを、実行履歴と呼び出し元の表示で照合する

通知などの経路を廃止するときは、アクションの削除と合わせて後続応答の `runAfter` と本文を更新し、残った参照式と未使用の connectionReferences を確認する。成功・失敗それぞれの応答経路を再検証する。

### URL で指定された実行履歴を読み取り専用で調べる

Power Automate の実行 URL をブラウザーで開けない場合も、直ちに調査不能とせず、既存認証で対象環境への参照権限を確認する。実行履歴の調査は、フロー編集・再実行とは別の読み取り作業とする。

1. URL のホストとパスを確認し、環境 ID・フロー ID・実行 ID を取り出す。`pac org who --json` の環境 ID・組織 URL・接続先アカウントと照合し、一致しなければ停止する。
2. 対象環境が一致し、既存の認証が使用できる場合に限り、共通の `auth_helper.py` の `flow_api_call("GET", path)` で Flow API にアクセスする。`path` は `/providers/Microsoft.ProcessSimple/environments/{environmentId}/flows/{flowId}` を起点に、フロー情報、`/runs/{runId}`、その `/actions` を順に指定し、返る ID・状態を照合する。多数の履歴は必要な件数に絞って確認する。Flow API のフロー ID を Dataverse の workflow ID と同一視しない。
3. 実行全体の `Succeeded` だけで成果物成功とせず、条件分岐と保存・リンク作成・成功応答それぞれの `Succeeded` / `Skipped` / `Failed` を確認する。トークン、署名付き URL、回答本文、アクションの入出力全体を表示・保存しない。認証・権限・API のエラーは実際の状態とともに報告し、別アカウントでの回避や書き込みには進まない。

この経路は案件での読取実績に基づく調査手順であり、すべての環境での API 権限やアクション履歴の取得を保証しない。

## 3. docs と UI がずれたら code view と clone 定義を正本にする

Learn、swagger、過去の実装例と、Power Automate デザイナーの実際の code view が
食い違うことがある。

### 正本順位

1. 現在の環境で UI 保存済みの code view
2. その環境から pac / clone / export した定義
3. 公式 docs / swagger

### 判断基準

- docs は操作の存在確認と意味確認に使う
- 実際に送る parameter key や body 階層は、UI 保存済み定義に合わせる
- 同じ operationId でも、コードビューの階層が違えば UI 側に合わせる

### 避けること

- docs の記載だけを根拠に、UI が別 shape を期待している action を上書きする
- 別環境の code view を、そのまま現在環境の最終正本とみなす

## 4. pac solution sync の結果が怪しいときは fresh clone で切る

pac solution sync の直後に同じファイルを並列で読むと、ローカル更新途中の内容を拾い、
stale に見えることがある。

### 切り分け手順

1. sync と同時に対象 JSON を読まない
2. 取得結果が不自然なら、別ディレクトリへ fresh clone を取る
3. fresh clone と作業フォルダで結果が一致するか比較する

### 使いどころ

- 画面では保存済みなのに、ローカル clone では古い action 数に見える
- sync 後の JSON が途中状態に見える
- export の問題か、ローカル読み取り競合かを切り分けたい

### 避けること

- 1 回の sync 結果だけで「環境側が古い」と断定する
- stale に見えた時点で、すぐにフロー本体の修正に進む

## Microsoft 365 Copilot Chat のリンク応答

成功応答にクリック可能な URL を表示するときは `message` に `[表示名](URL)` の Markdown リンクを使う（検証したケースではプレーン URL では不可）。表示用 `message` と機械可読な URL 出力は分け、既存の URL 出力契約を Markdown に置き換えない。成功表示だけを変更し、失敗応答と共有リンク作成後に応答する順序は保持して回帰確認する。

## 接続の実行主体を選ぶ（`invoker` / `embedded`）

実行者ごとに参照できるデータを分ける必要があるか、共通のデータを管理された接続で処理するかを先に決める。フローの `connectionReferences[*].runtimeSource` はコネクタごとに確認し、表示名やフロー ID の変更とは独立した設定として扱う。

| 条件 | 選択候補 | 運用上の確認 |
|---|---|---|
| 利用者本人のアクセス権で読み書きし、個人ごとのデータ制限を守る | `invoker`（実行者が接続を提供） | 各利用者の接続、同意、対象リソースへの権限、利用チャネルでの認証導線 |
| 複数利用者が同じ共有データ・保存先を扱い、組織がその権限を一元管理する | `embedded`（フローに設定した接続を使用） | 最小権限の接続所有者、接続参照の割当、所有者変更・失効時の運用、共有先と閲覧権限 |

`embedded` を使うだけで利用者のデータ権限が維持されるわけではない。フローから取得した内容を誰に返すか、生成したファイルを誰が閲覧できるかを別に設計する。Copilot Studio から呼ぶ場合は、フロー内の `runtimeSource` とエージェントの**ツール認証設定**を別々に確認する。ツール設定の値からフロー内の接続実行主体を推定しない。

既存フローの名前変更・デザイナー保存・ソリューション移送後には、前後の `runtimeSource` と接続参照先を再取得して比較する。差異があれば意図した実行主体を再判断し、予定利用者で取得・保存・応答・成果物の閲覧を試験する。顧客環境では実接続を再割当てし、開発環境の成功を流用しない。

出典: [Power Automate のフロー共有と実行者接続](https://learn.microsoft.com/en-us/power-automate/create-team-flows#can-another-user-use-a-connection-provided-by-the-run-only-user)、[Copilot Studio のツール認証](https://learn.microsoft.com/en-us/microsoft-copilot-studio/configure-enduser-authentication)。

## 5. 関連する基本原則

- 既定アクション優先、Graph HTTP は未サポート処理だけに限定する
- トリガー・アクション名は作成直後に固定する
- 接続参照はソリューション内で管理し、環境側の解決状態まで確認する

エージェント連携が想定されるフローでは、コード上で期待するトリガー定義、環境で確認したフローの種別、実際の呼び出し元を別々に記録する。どれか一つだけから他を断定せず、未確認ならそのまま記載する。一般的なクラウドフローとも、特定のエージェント専用フローとも、証拠なしに呼び分けない。

帳票など既存の様式へ出力する際は、差し込み対象外の固定欄を入力契約に勝手に追加せず、入力から確かめられない値を別の日時・属性から推測しない。確認済みの書式や凡例はデータ連携の修正に伴って自動で変更しない。案件ごとに差し込み対象と変更可能な範囲を確認する。

入力・出力契約を変更したら、実装とテストだけでなく、関連する仕様書のサンプルや0件時・例外時の記述も変更後の契約と照合する。テストが通っても、説明中の旧キーや旧形式が残っていないか確認する。

**AI 出力を文書へ差し込む MVP**

- 既存の解析アクションを保存処理より前に置く。
- 解析失敗時に保存へ進まないことを代表ケースで確認する。
- 解析エラーを成功応答へ変換しない。
- 個別の失敗分岐・補正は、具体的な副作用がある場合だけ追加する。
- 固定 JSON の単体成功と、AI 出力を使った成功を区別する。

**Word テンプレート**

- 最新版からタグ名・種類・繰り返しセクションを取得する。
- 理由欄や手動写真枠を含め、差し込み表との差分を確認してから固定入力を試す。
- 見出しと本文など役割の異なるタグは値の出どころを別々に定義する。後処理で対象を選び直す経路や値が欠ける経路も含め、両欄に同じ原文全文を代入する等、意図しない重複が生成文書にないか確認する。
- テンプレート更新時は差分確認をやり直す。タグ数・IDを固定しない。
- ローカル DOCX、Word Online 実行、生成 DOCX、画面表示は別々に確認する。
- 固定入力の後に、AI 出力を接続して確認する。

**エージェントからフローを使う場合**

1. 下書き／公開版、トリガー／応答、同期設定を確認する。
2. 接続参照とエージェントへのツール登録を確認する。
3. 会話から実行し、単体 run と区別して記録する。

[公式要件](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-flow-create)を採用構成・ハーネスと照合する。API と画面表示が食い違う場合は、バージョン・対象 ID・反映時刻を確認し、推測で上書きしない。

**既存定義の変更**

- 対象環境・フロー ID・現行定義・接続参照を照合する。
- 変更前定義を復旧可能な場所へ退避する。
- UI 雛形から別フローの ID や接続を流用しない。
- 差分を絞って反映し、再取得して変更箇所以外が保たれたことを確認する。
- 保存・公開・単体 run・エージェント実行を別々に判定する。
- 退避定義・実行出力の認証情報や接続情報を共有しない。

複数工程にまたがる依頼の報告では、仕様・変換処理・フロー定義への接続・関連文書などを、依頼された範囲に応じて「完了」「未着手」「要確認」に分ける。一部の成果物ができても全工程の完了とは表現せず、未接続の処理を稼働中のフローとして扱わない。

## 認証・環境解決と接続参照

既存のデプロイスクリプトは Dataverse Web API の `workflows` への作成・更新を主経路とし、Flow API は環境解決・起動、および Teams 1:1 投稿など一部デプロイ経路に使用する。対象フロー・接続参照・接続の状態を確認して経路を選び、有効化と実行結果をそれぞれ検証する。

- API の認証スコープを混用しない: Flow API `https://service.flow.microsoft.com/.default`（環境 ID 解決・`/start`）、PowerApps API `https://service.powerapps.com/.default`（接続検索）、Graph API `https://graph.microsoft.com/.default`（ユーザー情報）、Dataverse API `https://{org}.crm7.dynamics.com/.default`（`workflows`・`connectionreferences`）。
- 接続は `https://make.powerautomate.com/connections` で対象環境に事前作成する。API から接続を自動作成せず、PowerApps API で環境内の `Connected` 接続 ID を毎回検索する。古い ID のハードコードは `ConnectionNotFound` / `AppLeaseMissing` の原因となる。実行時に接続が `Error` / `Disconnected` なら UI で再認証する。
- Flow API の `GET https://api.flow.microsoft.com/providers/Microsoft.ProcessSimple/environments?api-version=2016-11-01`（timeout 60 秒）で `properties.linkedEnvironmentMetadata.instanceUrl` と `DATAVERSE_URL` の末尾 `/` を除いて比較し、一致する環境の `name` を環境 ID とする（`properties.displayName` ではない）。該当環境が見つからないときはエラーで止め、環境 ID を `.env` に固定しない。
- PowerApps API `GET https://api.powerapps.com/providers/Microsoft.PowerApps/apis/{connector}/connections`（`api-version=2016-11-01`、`$filter=environment eq '{env_id}'`）で接続を検索する。504 / Timeout の場合、`timeout=120`、最大 3 回、待機 `15 → 30 → 45` 秒で再試行する。成功時は `statuses` に `Connected` を含む接続を選ぶ。見つからなければ接続の事前作成・再認証を案内して止める。
- 2026-05 に確認した `AzureResourceManagerRequestFailed` には、接続 ID の直接埋め込みによる `authenticatedUserObjectId` 不足の事例がある。ソリューション対応フローでは接続参照を使う。
  1. 定義に `runtimeSource: "embedded"`、`connection.connectionReferenceLogicalName`、`api.name` を設定する。`host.connectionName` と `connectionReferences` のキーを一致させる。AI Builder 等で同一コネクタに別キー（例: `shared_commondataserviceforapps_1`）を使う場合は、そのキーも登録する。
  2. `connectionreferences?$filter=connectionreferencelogicalname eq '{logical_name}'&$select=connectionreferenceid,connectionid` で検索する。論理名だけでは不十分で、環境内に存在し、`connectionid` が空でなく、期待する `connectorid` と一致することを検査する。
  3. 既存参照の接続 ID が異なれば `connectionreferences({connectionreferenceid})` を PATCH する。参照が無ければ `connectionreferencelogicalname`、`connectionreferencedisplayname`、`connectorid: "/providers/Microsoft.PowerApps/apis/{connector}"`、`connectionid` を同一ソリューション内に POST する。
  4. 新規 POST の既存実装例では `retry_metadata(...)` でメタデータ反映を再試行し、論理名 `{PUBLISHER_PREFIX}_sharedcommondataserviceforapps` / `{PUBLISHER_PREFIX}_sharedoffice365` で Dataverse / Office 365 Outlook の接続をそれぞれ登録する。
- `connectionReferences` の接続 ID 直接指定（`connectionName` / `source: "Embedded"`）は単一環境の簡易方式だが、移行時の書き換えが必要で UI に接続参照の警告が出る場合がある。ソリューション ALM では論理名経由を優先する。Teams 1:1 の Flow API 固有の接続形式は [トリガー・アクションパターン](trigger-action-patterns.md#teams-11-チャット投稿--chat-with-flow-botpostmessagetoconversation) を参照。

## 定義作成・有効化の詳細

1. UI で最小フローを保存し、clone / export の定義を拡張する。Logic Apps スキーマ `https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#`、`contentVersion: "1.0.0.0"`、`$authentication`（`SecureObject`）と `$connections`（`Object`）のパラメータ、`triggers`、`actions` を保持し、`clientdata.properties.definition` と `clientdata.properties.connectionReferences`、`schemaVersion: "1.0.0.0"` に配置する。
2. Dataverse `workflows` へ `MSCRM.SolutionUniqueName` を付けて Draft 作成する際は `name`、`description`、`type: 1`、`category: 5`（Cloud Flow）、`statecode: 0`、`statuscode: 1`、`primaryentity: "none"`、`json.dumps(clientdata, ensure_ascii=False)` の JSON 文字列を使用する。作成直後は 3 秒程度待ち、`statecode: 1`、`statuscode: 2` で有効化する。接続参照と定義を確認してから実行結果を検証する。
3. Dataverse `SubscribeWebhookTrigger`（Create/Update 等）は有効化だけで Webhook 登録が終わらないため、有効化後 3 秒程度待ち Flow API スコープで `POST https://api.flow.microsoft.com/providers/Microsoft.ProcessSimple/environments/{env-id}/flows/{workflow-id}/start?api-version=2016-11-01`（timeout 60 秒）を呼ぶ。SharePoint `OnNewFile`（Notification 型）は非推奨の履歴例のみで新規採用しない。SharePoint `GetOnNewFileItems`（Polling）、`Recurrence`、`PowerAppV2` では `/start` 不要。登録失敗時は有効化済みと区別し、UI の Turn On による登録も確認する。
4. 有効化失敗時は `flow_definition_debug.json` に `{"workflow_body": workflow_body, "error": str(e)}` を UTF-8 / `ensure_ascii=False` / `indent=2` の JSON で保存し、UI での確認先 `https://make.powerautomate.com/environments/{env-id}/flows/{workflow-id}` を示して失敗終了する。UI での手動有効化を案内する。定義に顧客データや秘密情報が含まれ得るため、診断ファイルを共有・コミットしない。import / save / publish / 実行の各ゲートを別々に確認する。

## アクション組み立て・復旧時の注意

- PoC / MVP は目的に必要なアクションと検証に絞り、本番向けの拡張は自動追加しない。削減で正しさや必要な検証を損なわず、追加の作り込みが必要なら理由を明示して案件ごとに判断する。一覧取得・通常 CRUD・通知投稿は既定アクションを第一候補にする。Graph HTTP は既定アクションが無い、スキーマが不安定、または必要な操作を表現できない場合のみ設計時に理由を示して使う。Teams / Groups 等は対象リソースに近い既定コネクタを優先し、`/groups` を Teams Graph HTTP に無理に寄せない。
- Python の f-string に `@{...}` を埋め込むとブレースのエスケープが複雑になる。通常の文字列テンプレート `"@{triggerOutputs()?['body/{prefix}_name']}".replace('{prefix}', PREFIX)` を使うか、1 箇所なら f-string の二重ブレース `@{{...}}` を使う。複数箇所では後者を避ける。
- `InitializeVariable` は Scope 内に置かず、トップレベル `actions` に配置する。Scope 内は初期化済み変数への `SetVariable` / `AppendToArrayVariable` 等を使う。`SetVariable` で同じ変数を式に参照する（例: `union(variables('varItems'), createArray(...))` を `varItems` に代入）と `Self reference is not supported` になる。収集中は `AppendToArrayVariable` を使い、収集後に `Compose` で `union(variables('varItems'), variables('varItems'))` を実行して重複排除する。
- Modern Flow が `ActiveUnpublished` 相当の行状態で `pac solution import` を繰り返しても失敗する場合は、接続参照と定義を確認し、publish all 後も同一行で失敗するかを切り分ける。単一または少数の対象フローに限り、既存ソリューション／フローを退避し、参照先・ID 依存と明示承認を確認したうえで Dataverse `workflows` の削除・再作成を復旧候補とする。import の一般代替ではなく、削除後の途中失敗は自動回復しない（[デプロイ前チェック](pre-deploy-checks.md#破壊的なサンプルデプロイ)）。
- コネクタ削除時はフロー JSON の action と `connectionReferences`、ローカル Solution の `Customizations.xml` 等の connection reference、環境側の参照を照合する。環境側 `connectionreference` は workflow / solution の参照残りを確認してから削除する。片側だけ消すと次回のデプロイ／有効化に残骸が影響する。

基本原則の正本は [../SKILL.md](../SKILL.md) を参照。
