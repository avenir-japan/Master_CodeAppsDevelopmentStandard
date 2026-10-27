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

このマスターリポジトリでは、検証導入パッケージの**技術選定時の条件付き初期提案**を **ベースライセンス（Microsoft 365 + Copilot）の範囲内** に置く。提案前に顧客の契約・利用者／実行主体の利用権、利用可能なチャネル、既存資産（アプリ・データソース・コネクタ等）と案件要件を確認する。未確認なら採用を確定せず、案件の確定要件をこの初期提案で上書きしない。

- 既定の UI / チャネル候補は **Teams / Microsoft 365 Copilot** とし、利用可能性と要件適合を確認する
- **Canvas App（標準コネクタ）** は画面 UI が必要な場合の初期候補とし、既存資産、データソース・コネクタのライセンス条件と工数を確認する
- Code Apps、Dataverse カスタムテーブル、AI Builder、プレミアム / カスタムコネクタ、Credits 消費が見込まれる Copilot Studio パターンは、消費量の大小にかかわらず既定提案から外し、案件ごとにライセンスと Credits を評価する
- Power Automate クラウドフローからエージェントを呼び出す自律型の構成・実装は、Credits 非消費の条件を満たす場合でも標準スコープに含めず、必要時のみ例外的な代替案として検討する（[条件と根拠](references/license-requirements.md#1-基本方針)）
- Copilot Studio のハーネス選定と Credits の適用条件は [ライセンス確認ルール §1](references/license-requirements.md#1-基本方針) を参照する。
- Canvas App で要件を満たせない場合の Code Apps / モデル駆動型アプリ等は、実現性・ライセンス・費用を示した代替案としてユーザー承認後に採否を決める
- 個別スキルは技術手順の正本として残し、採用優先順位とスコープ判断は本スキル、`architecture`、`references/license-requirements.md` を正本とする

**技術選定と実装標準は別**: 上記の優先順位は方式を選ぶまでの初期提案であり、Code Apps を承認済みの方式として採用した案件では `code-apps` スキルと [開発標準の Code Apps 手順](references/power-platform-development-standard.md#4-ui-開発) を実装標準として適用する。Code Apps の実装手順が存在することを理由に、技術選定で Code Apps を既定採用しない。

開発段階の既定提案は PoC / MVP とし、本番品質・本番運用の保証を前提にしない。案件の確定要件を優先し、機能・検証範囲は目的に必要な範囲に絞る。
採用する重要経路は PoC / MVP でも [Phase 0 の実現可能性ゲート](references/power-platform-development-standard.md#開発着手前の実現可能性ゲート全案件必須)で技術・利用者／実行主体のライセンス・Copilot Credits を別々に判定する。未確認・不適合の経路は通常案として本実装に進めず、代替案を検討する。実機検証に Credits 消費や追加費用が生じ得る場合と、例外案を採用する場合は、条件・費用影響を示してユーザーの明示承認を得る。

## Copilot 向け優先判断基準

- GitHub Copilot のモデルには利用上限がある。社内の費用比較に基づき、開発では原則 Azure 上に用意した指定モデルを使う（社内方針）。具体名は固定せず社内の案内に従い、高難度の作業や比較レビューも指定モデルの中から選ぶ
- 納品、ALM、環境移送の相談では、まず `Copilot で自動整理`、`スクリプトで半自動`、`顧客管理者または案件責任者が実施` に分類する
- リポジトリを GitHub へ反映する場合、コミット後の変更点説明、更新箇所の要約、ユーザー向け報告は日本語で行う
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
| [ブラウザ自動化方針](references/browser-automation.md)                       | VS Code 統合ブラウザを使った検証手順の標準化                 |
| [対話型セットアップ](references/interactive-setup.md)                        | 初期確認を AskUserQuestion で整理する導入導線                |
| [VS Code・Copilot 環境構築](references/vscode-copilot-setup.md)              | 開発者端末の初回セットアップ                                 |
| sdk-update-check.md                                                          | npm SDK と upstream skills の追従確認手順                    |
| [アイコン作成](references/icon-creation.md)                                  | Pillow による PNG/SVG アイコン生成・API 登録パターン         |
| [HTML メールテンプレート](references/html-email-template.md)                 | HTML メールのデザインシステム・カラーパレット・基本原則      |
| [テンプレートコンポーネント](references/template-components.md)              | HTML メールの各コンポーネント詳細                            |

## 大前提: 一つのソリューション内に開発

採用した Dataverse テーブル・Canvas App・Code Apps・モデル駆動型アプリ・Power Automate フロー・Copilot Studio エージェントは **原則として同一のソリューション内** に含める。
`.env` の `SOLUTION_NAME` と `PUBLISHER_PREFIX` を全フェーズで統一して使用する。

初期化では、採用した構成に必要な Publisher・Solution と、必要に応じて環境変数・接続参照を準備する。
Dataverse カスタムテーブルの作成は初期化の必須工程ではない。要件で採用した場合のみ
[`dataverse`](../dataverse/SKILL.md) のテーブル構築工程へ進み、採用しない場合もソリューション管理は継続する。
ライセンスの適用条件は構成ごとに最新の公式情報で確認する。

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
**同じ実行環境・同じユーザープロファイルで再利用する** 2 層キャッシュ構成。別の OS / WSL / SSH / コンテナー / 実行ユーザーへレコードだけを移しても認証は引き継げない。

```text
層1: AuthenticationRecord (実行ユーザーの ~/.power-platform-cli/auth_record_{TENANT_ID}_browser.json)
  - アカウント情報（テナント・ユーザー ID）を保存。トークンは保存しない
  - Device Code は auth_record_{TENANT_ID}_device.json
  - 明示した client_id はブラウザのファイル名末尾を分離し、読み込み時は TENANT_ID の一致を確認

層2: TokenCachePersistenceOptions (OS のユーザーデータ保護 API で暗号化される永続キャッシュ)
  - 認証シークレットを保持。実ファイルや保存先は OS・実行環境の実装に依存する
  - 利用可能な場合にサイレント取得を試みる。再認証が不要とは保証しない

初回（社内開発）: InteractiveBrowserCredential → ブラウザで認証 → レコードとキャッシュ保存
2回目以降: 同一実行環境でキャッシュから取得を試み、必要なら再認証
```

`PP_NO_PERSISTENT_CACHE=1` は層2の永続化**のみ**無効化し、層1の読み込み・書き込みは継続する。既存の永続キャッシュを削除する設定ではない。レコード・トークンキャッシュは実行ユーザーの認証情報として扱い、共有・納品・コミットしない。対象別の安全な整理手順は [認証リファレンス](references/auth-patterns.md#実行環境とキャッシュの管理) を参照。

#### 認証既定: 弊社標準テナントではブラウザ対話認証を使う

弊社の標準開発テナントでは Device Code 認証が条件付きアクセスや利用制限で一律失敗する前提で扱う。
そのため、Power Platform 開発ではブラウザ対話認証を既定とする。

```powershell
$env:PP_USE_INTERACTIVE_BROWSER = "1"
```

案件の `.env` では `PP_USE_INTERACTIVE_BROWSER=true` を設定する。顧客テナントへの納品時に社内の `.env` や認証キャッシュを含めず、顧客環境の認証設定は個別に確認する。

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

### 事前検証: MCP ツールの利用可能性

MCP ツールを使う作業では、必要な範囲で次を順に確認する。

1. 適用される VS Code のワークスペース・ユーザー設定に対象サーバーが登録されているか。
2. 現在の VS Code セッションで対象ツールが利用可能として表示されるか。
3. 対象機能の小さな実呼び出しが成功するか。

設定の存在だけで接続成功と判断せず、登録を追加する前に既存設定も確認する。
各段階の結果を区別し、未実施の確認を成功扱いしない。

### 事前検証: Dataverse 側の MCP クライアント状態チェック

Dataverse 側で MCP クライアントの許可が必要な作業では、`.github/skills/standard/scripts/check_mcp_client.py` で
対象クライアントの有効状態を確認する。この検査は VS Code 側の登録・ツール表示・実呼び出しの確認とは別に行う。

### 定期点検: SDK / upstream skills 更新チェック

依存更新や upstream 公式 skills の追従要否を確認するときは、
`.github/scripts/check-sdk-updates.mjs` を dry-run で実行して差分を確認する。
運用手順は `standard/references/sdk-update-check.md` を正本とする。

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
> 契約・チャネル・既存資産・案件要件を確認したうえでの初期候補は「Teams / Microsoft 365 Copilot を先頭、Canvas App は画面 UI が必要な場合、その他は案件判断」とする。選定後は採用方式のスキルを実装標準とする。

| フェーズ                  | スキル             | 内容                                                                        |
| ------------------------- | ------------------ | --------------------------------------------------------------------------- |
| Phase 1: Dataverse 構築   | `dataverse`        | テーブル設計・作成・ローカライズ・デモデータ                                |
| Phase 1.5: Security Role  | `dataverse`        | カスタムセキュリティロール作成・権限設定                                    |
| Phase 2: Copilot Studio   | `copilot-studio`   | Teams / M365 Copilot をチャネルとする対話体験                               |
| Phase 2: Code Apps        | `code-apps`        | 初期化・デプロイ・Dataverse 接続                                            |
| Phase 2: Code Apps UI     | `code-apps`        | CodeAppsStarter デザインシステム・コンポーネント                            |
| Phase 2: Canvas App       | `canvas-app`       | MCP + coauthoring、Git Integration、限定移送、添付・SharePoint staging 運用 |
| Phase 2: Model-Driven App | `model-driven-app` | モデル駆動型アプリ作成・SiteMap・公開                                       |
| Phase 2.5: Power Automate | `power-automate`   | クラウドフロー作成・接続参照                                                |
| Phase 3: Copilot Studio   | `copilot-studio`   | エージェント構築・生成オーケストレーション                                  |

## クイックリファレンス: 絶対遵守ルール

> **Dataverse テーブル構築ルール**（スキーマ設計・Lookup・ローカライズ・デモデータ等）は [`dataverse`](../dataverse/SKILL.md) スキルに移管済み。

| ルール                                                                                 | 理由                                                                                                                                                                                                                                                                             |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 先にデプロイしてから開発                                                               | Dataverse 接続確立が必要                                                                                                                                                                                                                                                         |
| 生成オーケストレーションモード一択                                                     | トピックベース開発は非推奨                                                                                                                                                                                                                                                       |
| Flow API は専用スコープで認証                                                          | Dataverse トークンの使い回し不可                                                                                                                                                                                                                                                 |
| 接続は環境内に事前作成                                                                 | API での接続自動作成は不可                                                                                                                                                                                                                                                       |
| フローはべき等パターンでデプロイ                                                       | displayName で検索 → 更新 or 新規作成                                                                                                                                                                                                                                            |
| Bot 作成は Copilot Studio UI                                                           | API（bots INSERT）ではプロビジョニングされない                                                                                                                                                                                                                                   |
| Bot 作成後はプロビジョニング完了を待つ                                                 | UI でロード完了前にスクリプト実行→トピック削除 0 件になる                                                                                                                                                                                                                        |
| configuration はディープマージで PATCH                                                 | 丸ごと上書き→基盤モデル・gPTSettings が消える                                                                                                                                                                                                                                    |
| optInUseLatestModels は明示的に False                                                  | True だと基盤モデルが GPT に強制変更。既存 True も上書き                                                                                                                                                                                                                         |
| 推奨プロンプトは conversationStarters で登録                                           | GPT コンポーネント (type=15) YAML の title/text                                                                                                                                                                                                                                  |
| 挨拶メッセージはエージェントに合わせて設定                                             | ConversationStart トピック (type=9) の SendActivity.text                                                                                                                                                                                                                         |
| クイック返信は ConversationStart で登録                                                | ConversationStart トピック (type=9) の quickReplies                                                                                                                                                                                                                              |
| トピック削除時はシステムトピックを保護                                                 | schemaname パターンで ConversationStart, Escalate 等を保護                                                                                                                                                                                                                       |
| チャネル公開は applicationmanifestinformation                                          | teams オブジェクトに shortDescription/longDescription 等                                                                                                                                                                                                                         |
| M365 Copilot は copilotChat.isEnabled                                                  | applicationmanifestinformation 内で true に設定                                                                                                                                                                                                                                  |
| 説明は publish 後に設定                                                                | data PATCH の非同期処理で上書きされる                                                                                                                                                                                                                                            |
| appId は環境固有                                                                       | 別環境の appId → AppLeaseMissing (409)                                                                                                                                                                                                                                           |
| Code Apps を環境で有効化                                                               | 未許可 → CodeAppOperationNotAllowedInEnvironment (403)                                                                                                                                                                                                                           |
| dataSourcesInfo.ts は SDK コマンドで生成                                               | `npx power-apps add-data-source` で自動生成。手動作成禁止                                                                                                                                                                                                                        |
| **init スキャフォールドファイルは手動作成禁止**                                        | `npx power-apps init` が `power.config.json`, `plugins/plugin-power-apps.ts`, `vite.config.ts` 等を自動生成。コピー禁止                                                                                                                                                          |
| PAC CLI 認証プロファイルを作成                                                         | 新環境では pac auth create が必須                                                                                                                                                                                                                                                |
| get_token() は scope のみ指定                                                          | auth_helper は .env から自動読み込み                                                                                                                                                                                                                                             |
| **全コンポーネントをソリューションに含める**                                           | AddSolutionComponent で検証・補完。ヘッダーだけに依存しない                                                                                                                                                                                                                      |
| **設計フェーズでユーザー承認必須**                                                     | テーブル設計を提示し承認を得てから構築に進む                                                                                                                                                                                                                                     |
| **nameUtils パッチは Node.js スクリプトで**                                            | PowerShell の $ エスケープで適用失敗する。`node patch-nameutils.cjs` を使う                                                                                                                                                                                                      |
| **SDK Lookup 名は未ポピュレート（初回から対応必須）**                                  | `createdbyname` 等は返らない。**初回デプロイから** `_xxx_value` + `useMemo` クライアントサイド名前解決を実装                                                                                                                                                                     |
| **フロー接続 ID はハードコードしない**                                                 | 環境が変わると接続 ID も変わる。毎回 PowerApps API で自動検索                                                                                                                                                                                                                    |
| **PowerApps API 接続検索はタイムアウトする**                                           | 504 GatewayTimeout 頻発。3回リトライ＋フォールバック接続 ID パターンで対策                                                                                                                                                                                                       |
| **AI Builder アクションは API でフロー定義に含めない**                                 | PerformBoundAction → InvalidOpenApiFlow で有効化失敗。Power Automate UI で手動追加                                                                                                                                                                                               |
| **api_get() は dict を返す**                                                           | `.json()` を呼ぶとエラー。戻り値の dict をそのまま使う                                                                                                                                                                                                                           |
| **api_get() はパス文字列のみ受付**                                                     | `api_get("url", {"$filter": ...})` は不可。クエリパラメータは URL に直接埋め込む: `api_get("url?$filter=...")`                                                                                                                                                                   |
| **PowerShell インラインで `$select` 等を使わない**                                     | PowerShell が `$select` を変数展開しパラメータ名が消失（`?=3&=...` になる）。Python スクリプトファイルで実行すること                                                                                                                                                             |
| **Dataverse API 429 レート制限にはリトライ＋再実行**                                   | `PublishAllXml` や `EntityDefinitions` PUT で 429 が頻発。時間を置いてスクリプト再実行で回復。べき等設計が必須                                                                                                                                                                   |
| **ConversationStart/GPT YAML は手動構築**                                              | `yaml.dump()` は PVA パーサーと非互換。会話の開始・クイック返信・推奨プロンプトが消える                                                                                                                                                                                          |
| **bots PATCH には name フィールド必須**                                                | 省略すると `Empty or null bot name` エラー (0x80040265)。既存名を GET して再送                                                                                                                                                                                                   |
| **アイコンは [アイコン作成リファレンス](references/icon-creation.md) に従い API 登録** | エージェント=PNG 3サイズ、テーブル=SVG WebResource。詳細は `references/icon-creation.md`                                                                                                                                                                                         |
| **基盤モデルは API で設定できない**                                                    | `aISettings` PATCH で `optInUseLatestModels: False` にしても基盤モデルが GPT に戻るケースあり。UI で手動選択                                                                                                                                                                     |
| **`npx power-apps push` テナント不一致問題**                                           | 環境 ID からテナント解決に失敗し `ServiceToServiceEnvironmentNotFound` (404) を返す場合がある。**`pac code push -env {ENVIRONMENT_ID} -s {SOLUTION_NAME}` を使う**                                                                                                               |
| **`npx power-apps add-data-source` テナント不一致**                                    | 同様にテナント不一致で org-url プロンプトが出る。**`--org-url {DATAVERSE_URL}` を明示指定**するか、対話プロンプトで入力する                                                                                                                                                      |
| **メール返信は Work IQ Mail MCP を使う**                                               | 「メールに返信する (V3)」コネクタは Attachments 属性でスタックする。Work IQ Mail MCP（`mcp_MailTools`）を使うこと                                                                                                                                                                |
| **メールトリガー時は質問禁止**                                                         | メールから起動時にユーザーに質問するとチャット返信できずスタック。Instructions に判定ロジックと即処理ルールが必須                                                                                                                                                                |
| **ExecuteCopilot プロンプトは構造化**                                                  | `triggerBody()` の丸投げは不十分。メッセージID・差出人・件名・本文を個別に渡し、ツール名を明示する                                                                                                                                                                               |
| **セキュリティロールは Basic User コピーから開始**                                     | ゼロから作成すると約480の標準権限が欠落しアプリが動かない。RetrieveRolePrivilegesRole で取得して土台にする                                                                                                                                                                       |
| **マスタテーブルの読み取り専用ロールにも AppendTo**                                    | Lookup 先テーブルに AppendTo がないとレコード作成時にエラー。Read + AppendTo: Global が最低限必要                                                                                                                                                                                |
| **ライセンス回答は固定値を断定しない**                                                 | 既定提案は利用者・実行主体のベースライセンス内かつ Credits 非消費とし、Code Apps、Dataverse カスタムテーブル、AI Builder、プレミアム / カスタムコネクタ、Credits 消費が見込まれる Copilot Studio パターンは、消費量によらず都度最新の Microsoft Learn または公式ガイドで判定する |
