---
name: standard
description: "Power Platform 包括開発標準。共通認証（auth_helper.py）・.env パラメータ・ソリューション管理・アイコン生成・HTML メールテンプレートなど全スキル共通の基盤。"
category: architecture
triggers:
  - "Power Platform 開発"
  - "Code Apps"
  - "Power Automate"
  - "フロー作成"
  - "Copilot Studio"
  - "エージェント開発"
  - "ソリューション"
  - "デプロイ"
  - "トラブルシューティング"
  - "生成オーケストレーション"
  - "アイコン作成"
  - "アイコン生成"
  - "icon"
  - "PNG"
  - "SVG"
  - "Pillow"
  - "iconbase64"
  - "WebResource"
  - "テーブルアイコン"
  - "エージェントアイコン"
  - "アプリアイコン"
  - "HTML メール"
  - "メールテンプレート"
  - "HTMLメールデザイン"
  - "リッチメール"
  - "メール通知"
  - "ニュースレター"
  - "レポートメール"
  - "メールフォーマット"
---

# Power Platform 包括開発標準スキル

全スキル共通の基盤。共通認証・ソリューション管理・アイコン生成・HTML メールテンプレートを提供する。

## この標準の既定スコープ

このマスターリポジトリでは、検証導入パッケージの既定提案を **ベースライセンス（Microsoft 365 + Copilot）の範囲内** に置く。

- 既定の UI / チャネルは **Teams / Microsoft 365 Copilot** を優先する
- **Canvas App（標準コネクタ）** は既定スコープに含むが、工数を踏まえて必要時のみ採用候補とする
- Code Apps、Dataverse カスタムテーブル、AI Builder、プレミアム / カスタムコネクタ、クレジット消費が大きい Copilot Studio パターンは、既定提案ではなく **案件ごとの追加ライセンス評価項目** として扱う
- 個別スキルは技術手順の正本として残し、採用優先順位とスコープ判断は本スキル、`architecture`、`references/license-requirements.md` を正本とする

## Copilot 向け優先判断基準

- GitHub Copilot の既定モデルは GPT-5.4 とし、軽作業は軽量モデル、コード量が多い実装はコード特化モデルも候補にしつつ、アーキテクチャ設計、原因不明の障害調査、横断リファクタリング、納品前の高リスクレビューでは、まず GPT 系の上位 reasoning model を候補にし、比較検討や別観点レビューが必要な場合は Opus 系も候補にする
- 納品、ALM、環境移送の相談では、まず `Copilot で自動整理`、`スクリプトで半自動`、`顧客管理者または案件責任者が実施` に分類する
- 環境変数だけで終わらせず、マネージド / アンマネージド選定、マネージドプロパティ、接続参照、顧客初期設定作業まで確認する
- 顧客テナント固有の URL、実 ID、シークレット、接続資格情報、承認要否は Copilot が仮決めしない
- ライセンス、認証、チャネル設定は固定値を断定せず、最新の公式情報確認と顧客承認を前提に案内する
- マネージド案件では、顧客のアンマネージド層編集を既定にせず、再提供運用を優先して案内する

## サブリファレンス（必要に応じて参照）

| リファレンス                                                                 | 内容                                                         |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [Power Platform 開発標準](references/power-platform-development-standard.md) | 設計原則・Phase 別手順・チェックリストをまとめた全体ガイド   |
| [マスターリポジトリへの知見還元](references/master-repo-feedback-loop.md)    | 案件リポジトリから汎用知見をマスターへ戻すフィードバック運用 |
| [ソリューション運用と納品](references/managed-solution-delivery.md)          | マネージド / アンマネージド選定、納品、初期設定の考え方      |
| [環境変数ガイド](references/environment-variables.md)                        | 環境変数の型、使い方、納品時の差し替えパターン               |
| [ライセンス確認ルール](references/license-requirements.md)                   | 固定値を断定せず、最新 docs を確認するための確認観点         |
| [認証リファレンス](references/auth-patterns.md)                              | auth_helper.py の詳細実装・認証パターン                      |
| [アイコン作成](references/icon-creation.md)                                  | Pillow による PNG/SVG アイコン生成・API 登録パターン         |
| [HTML メールテンプレート](references/html-email-template.md)                 | HTML メールのデザインシステム・カラーパレット・基本原則      |
| [テンプレートコンポーネント](references/template-components.md)              | HTML メールの各コンポーネント詳細                            |

## 大前提: 一つのソリューション内に開発

Dataverse テーブル・Code Apps・Power Automate フロー・Copilot Studio エージェントは **すべて同一のソリューション内** に含める。
`.env` の `SOLUTION_NAME` と `PUBLISHER_PREFIX` を全フェーズで統一して使用する。

## 共通基盤: .env と認証

すべてのデプロイスクリプトは以下の **共通パラメータ** と **共通認証** を使用する。
各スキルから個別に認証を設定する必要はない。

### .env 共通パラメータ

環境情報は **Power Apps ポータル > 設定（右上の⚙）> セッション詳細** から取得する。

```env
# === 必須（全フェーズ共通）===
DATAVERSE_URL=https://{org}.crm7.dynamics.com/   # セッション詳細: Instance URL
TENANT_ID={your-tenant-id}                       # セッション詳細: Tenant ID
SOLUTION_NAME={YourSolutionName}
PUBLISHER_PREFIX={prefix}

# === オプション ===
PAC_AUTH_PROFILE={YourProfileName}         # PAC CLI 認証プロファイル名
ADMIN_EMAIL=admin@example.com              # Power Automate 通知先
BOT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  # Copilot Studio Bot ID（URL でも可）
```

> **セッション詳細の Environment ID** は `pac auth create --environment {env-id}` でも使用する。

| パラメータ         | 用途                           | 使用フェーズ               |
| ------------------ | ------------------------------ | -------------------------- |
| `DATAVERSE_URL`    | Dataverse Web API のベース URL | 全フェーズ                 |
| `TENANT_ID`        | Azure AD テナント ID           | 全フェーズ                 |
| `SOLUTION_NAME`    | ソリューション一意名           | 全フェーズ                 |
| `PUBLISHER_PREFIX` | テーブル・列のプレフィックス   | 全フェーズ                 |
| `PAC_AUTH_PROFILE` | PAC CLI の認証プロファイル名   | Phase 2 (Code Apps)        |
| `ADMIN_EMAIL`      | フロー通知先メール             | Phase 2.5 (Power Automate) |
| `BOT_ID`           | Copilot Studio Bot ID or URL   | Phase 3 (Copilot Studio)   |

### 共通認証: auth_helper.py

共通実装は `.github/skills/standard/scripts/auth_helper.py` にあり、案件スクリプトでは必要に応じてプロジェクト直下へコピーして利用する。
**ユーザーに何度もデバイスコード認証を求めない** 2 層キャッシュ構成。

```
層1: AuthenticationRecord (.auth_record.json)
  - アカウント情報（テナント・ユーザー ID）を保存
  - `auth_helper.py` と同じディレクトリに .auth_record.json として永続化

層2: TokenCachePersistenceOptions (MSAL OS 資格情報ストア)
  - リフレッシュトークン・アクセストークンを永続化
  - サイレントリフレッシュでデバイスコード不要

初回: DeviceCodeCredential → ブラウザで認証 → キャッシュ保存
2回目以降: キャッシュから自動取得（認証プロンプトなし）
```

#### 認証既定: 弊社標準テナントではブラウザ対話認証を使う

弊社の標準開発テナントでは Device Code 認証が条件付きアクセスや利用制限で一律失敗する前提で扱う。
そのため、Power Platform 開発ではブラウザ対話認証を既定とする。

```powershell
$env:PP_USE_INTERACTIVE_BROWSER = "1"
```

```text
使いどころ:
  - 弊社標準開発テナントで Power Platform 系スクリプトを実行する
  - Device Code で「アクセス権がありません」「この方法は許可されていません」系の失敗になる
  - CLI や SDK の Device Code 認証は通らないが、同一アカウントでブラウザサインインは可能

原則:
  - 弊社標準開発テナントでは、最初から PP_USE_INTERACTIVE_BROWSER=1 を前提にする
  - 他テナントへ持ち出す場合のみ、Device Code 可否を個別確認する
  - 顧客テナント固有の認証制限は Copilot が迂回方法を仮決めせず、ブラウザサインイン可否を前提に案内する
```

#### 公開 API

認証パターンの詳細実装は [認証リファレンス](references/auth-patterns.md) を参照。

## 参照ドキュメント

- [開発標準](references/power-platform-development-standard.md): 設計原則・Phase 別手順・トラブルシューティング
- [Dataverse ガイド](../dataverse/references/dataverse-guide.md): CRUD・Lookup・Choice・エラーハンドリング

## Copilot の振る舞いルール

納品、ALM、環境移送、顧客運用に関する相談を受けた場合、Copilot は次の順で整理する。

1. まず対象を `Copilot で自動整理できるもの`、`スクリプトで半自動化できるもの`、`顧客管理者または案件責任者が実施すべきもの` に分類する
2. 環境変数だけで終わらせず、最低でも `マネージド / アンマネージドの選定`、`マネージドプロパティ方針`、`接続参照`、`顧客環境で必要な初期設定作業`、`ライセンス・認証・DLP の確認要否` を確認する
3. マネージド案件では、顧客がアンマネージド層で編集してよい範囲を表で提案する
4. 顧客テナントでしか実施できない作業や秘密情報の入力は、Copilot が完了したように見せず `顧客管理者が実施` と明示する
5. ライセンス、認証、チャネル設定は固定値を断定せず、最新の公式ドキュメント確認と顧客承認を前提に案内する

マネージドプロパティの初期提案は次を既定とする。

| コンポーネント                             | 既定方針           |
| ------------------------------------------ | ------------------ |
| Power Automate フロー                      | 顧客編集不可       |
| Code App / Canvas App / モデル駆動型アプリ | 顧客編集不可       |
| Copilot Studio エージェント本体            | 顧客編集不可       |
| 環境変数                                   | 値変更可           |
| 接続参照                                   | 差し替え可         |
| Dataverse テーブル、列                     | 要件次第で個別判断 |

## 関連スキル

> **採用優先順位の扱い**: 下表は利用可能な実装スキルの一覧であり、既定提案の優先順位そのものではない。
> 優先順位は「Teams / Microsoft 365 Copilot を先頭、Canvas App は必要時のみ、その他は案件判断」を正本とする。

| フェーズ                  | スキル             | 内容                                             |
| ------------------------- | ------------------ | ------------------------------------------------ |
| Phase 1: Dataverse 構築   | `dataverse`        | テーブル設計・作成・ローカライズ・デモデータ     |
| Phase 1.5: Security Role  | `dataverse`        | カスタムセキュリティロール作成・権限設定         |
| Phase 2: Copilot Studio   | `copilot-studio`   | Teams / M365 Copilot をチャネルとする対話体験    |
| Phase 2: Code Apps        | `code-apps`        | 初期化・デプロイ・Dataverse 接続                 |
| Phase 2: Code Apps UI     | `code-apps`        | CodeAppsStarter デザインシステム・コンポーネント |
| Phase 2: Canvas App       | `canvas-app`       | 添付・SharePoint staging・msapp import 運用      |
| Phase 2: Model-Driven App | `model-driven-app` | モデル駆動型アプリ作成・SiteMap・公開            |
| Phase 2.5: Power Automate | `power-automate`   | クラウドフロー作成・接続参照                     |
| Phase 3: Copilot Studio   | `copilot-studio`   | エージェント構築・生成オーケストレーション       |

## クイックリファレンス: 絶対遵守ルール

> **Dataverse テーブル構築ルール**（スキーマ設計・Lookup・ローカライズ・デモデータ等）は [`dataverse`](../dataverse/SKILL.md) スキルに移管済み。

| ルール                                                                                 | 理由                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 先にデプロイしてから開発                                                               | Dataverse 接続確立が必要                                                                                                                                                                                                                    |
| 生成オーケストレーションモード一択                                                     | トピックベース開発は非推奨                                                                                                                                                                                                                  |
| Flow API は専用スコープで認証                                                          | Dataverse トークンの使い回し不可                                                                                                                                                                                                            |
| 接続は環境内に事前作成                                                                 | API での接続自動作成は不可                                                                                                                                                                                                                  |
| フローはべき等パターンでデプロイ                                                       | displayName で検索 → 更新 or 新規作成                                                                                                                                                                                                       |
| Bot 作成は Copilot Studio UI                                                           | API（bots INSERT）ではプロビジョニングされない                                                                                                                                                                                              |
| Bot 作成後はプロビジョニング完了を待つ                                                 | UI でロード完了前にスクリプト実行→トピック削除 0 件になる                                                                                                                                                                                   |
| configuration はディープマージで PATCH                                                 | 丸ごと上書き→基盤モデル・gPTSettings が消える                                                                                                                                                                                               |
| optInUseLatestModels は明示的に False                                                  | True だと基盤モデルが GPT に強制変更。既存 True も上書き                                                                                                                                                                                    |
| 推奨プロンプトは conversationStarters で登録                                           | GPT コンポーネント (type=15) YAML の title/text                                                                                                                                                                                             |
| 挨拶メッセージはエージェントに合わせて設定                                             | ConversationStart トピック (type=9) の SendActivity.text                                                                                                                                                                                    |
| クイック返信は ConversationStart で登録                                                | ConversationStart トピック (type=9) の quickReplies                                                                                                                                                                                         |
| トピック削除時はシステムトピックを保護                                                 | schemaname パターンで ConversationStart, Escalate 等を保護                                                                                                                                                                                  |
| チャネル公開は applicationmanifestinformation                                          | teams オブジェクトに shortDescription/longDescription 等                                                                                                                                                                                    |
| M365 Copilot は copilotChat.isEnabled                                                  | applicationmanifestinformation 内で true に設定                                                                                                                                                                                             |
| 説明は publish 後に設定                                                                | data PATCH の非同期処理で上書きされる                                                                                                                                                                                                       |
| appId は環境固有                                                                       | 別環境の appId → AppLeaseMissing (409)                                                                                                                                                                                                      |
| Code Apps を環境で有効化                                                               | 未許可 → CodeAppOperationNotAllowedInEnvironment (403)                                                                                                                                                                                      |
| dataSourcesInfo.ts は SDK コマンドで生成                                               | `npx power-apps add-data-source` で自動生成。手動作成禁止                                                                                                                                                                                   |
| **init スキャフォールドファイルは手動作成禁止**                                        | `npx power-apps init` が `power.config.json`, `plugins/plugin-power-apps.ts`, `vite.config.ts` 等を自動生成。コピー禁止                                                                                                                     |
| PAC CLI 認証プロファイルを作成                                                         | 新環境では pac auth create が必須                                                                                                                                                                                                           |
| get_token() は scope のみ指定                                                          | auth_helper は .env から自動読み込み                                                                                                                                                                                                        |
| **全コンポーネントをソリューションに含める**                                           | AddSolutionComponent で検証・補完。ヘッダーだけに依存しない                                                                                                                                                                                 |
| **設計フェーズでユーザー承認必須**                                                     | テーブル設計を提示し承認を得てから構築に進む                                                                                                                                                                                                |
| **nameUtils パッチは Node.js スクリプトで**                                            | PowerShell の $ エスケープで適用失敗する。`node patch-nameutils.cjs` を使う                                                                                                                                                                 |
| **SDK Lookup 名は未ポピュレート（初回から対応必須）**                                  | `createdbyname` 等は返らない。**初回デプロイから** `_xxx_value` + `useMemo` クライアントサイド名前解決を実装                                                                                                                                |
| **フロー接続 ID はハードコードしない**                                                 | 環境が変わると接続 ID も変わる。毎回 PowerApps API で自動検索                                                                                                                                                                               |
| **PowerApps API 接続検索はタイムアウトする**                                           | 504 GatewayTimeout 頻発。3回リトライ＋フォールバック接続 ID パターンで対策                                                                                                                                                                  |
| **AI Builder アクションは API でフロー定義に含めない**                                 | PerformBoundAction → InvalidOpenApiFlow で有効化失敗。Power Automate UI で手動追加                                                                                                                                                          |
| **api_get() は dict を返す**                                                           | `.json()` を呼ぶとエラー。戻り値の dict をそのまま使う                                                                                                                                                                                      |
| **api_get() はパス文字列のみ受付**                                                     | `api_get("url", {"$filter": ...})` は不可。クエリパラメータは URL に直接埋め込む: `api_get("url?$filter=...")`                                                                                                                              |
| **PowerShell インラインで `$select` 等を使わない**                                     | PowerShell が `$select` を変数展開しパラメータ名が消失（`?=3&=...` になる）。Python スクリプトファイルで実行すること                                                                                                                        |
| **Dataverse API 429 レート制限にはリトライ＋再実行**                                   | `PublishAllXml` や `EntityDefinitions` PUT で 429 が頻発。時間を置いてスクリプト再実行で回復。べき等設計が必須                                                                                                                              |
| **ConversationStart/GPT YAML は手動構築**                                              | `yaml.dump()` は PVA パーサーと非互換。会話の開始・クイック返信・推奨プロンプトが消える                                                                                                                                                     |
| **bots PATCH には name フィールド必須**                                                | 省略すると `Empty or null bot name` エラー (0x80040265)。既存名を GET して再送                                                                                                                                                              |
| **アイコンは [アイコン作成リファレンス](references/icon-creation.md) に従い API 登録** | エージェント=PNG 3サイズ、テーブル=SVG WebResource。詳細は `references/icon-creation.md`                                                                                                                                                    |
| **基盤モデルは API で設定できない**                                                    | `aISettings` PATCH で `optInUseLatestModels: False` にしても基盤モデルが GPT に戻るケースあり。UI で手動選択                                                                                                                                |
| **`npx power-apps push` テナント不一致問題**                                           | 環境 ID からテナント解決に失敗し `ServiceToServiceEnvironmentNotFound` (404) を返す場合がある。**`pac code push -env {ENVIRONMENT_ID} -s {SOLUTION_NAME}` を使う**                                                                          |
| **`npx power-apps add-data-source` テナント不一致**                                    | 同様にテナント不一致で org-url プロンプトが出る。**`--org-url {DATAVERSE_URL}` を明示指定**するか、対話プロンプトで入力する                                                                                                                 |
| **メール返信は Work IQ Mail MCP を使う**                                               | 「メールに返信する (V3)」コネクタは Attachments 属性でスタックする。Work IQ Mail MCP（`mcp_MailTools`）を使うこと                                                                                                                           |
| **メールトリガー時は質問禁止**                                                         | メールから起動時にユーザーに質問するとチャット返信できずスタック。Instructions に判定ロジックと即処理ルールが必須                                                                                                                           |
| **ExecuteCopilot プロンプトは構造化**                                                  | `triggerBody()` の丸投げは不十分。メッセージID・差出人・件名・本文を個別に渡し、ツール名を明示する                                                                                                                                          |
| **セキュリティロールは Basic User コピーから開始**                                     | ゼロから作成すると約480の標準権限が欠落しアプリが動かない。RetrieveRolePrivilegesRole で取得して土台にする                                                                                                                                  |
| **マスタテーブルの読み取り専用ロールにも AppendTo**                                    | Lookup 先テーブルに AppendTo がないとレコード作成時にエラー。Read + AppendTo: Global が最低限必要                                                                                                                                           |
| **ライセンス回答は固定値を断定しない**                                                 | 本パッケージの既定提案はベースライセンス範囲内だが、Code Apps、Dataverse カスタムテーブル、AI Builder、プレミアム / カスタムコネクタ、クレジット消費が大きい Copilot Studio パターンは都度最新の Microsoft Learn または公式ガイドを確認する |
