# Copilot Studio エージェント構築リファレンス

## 構築手順

構築前にエージェント名・説明、Instructions 全文、推奨プロンプト（conversationStarters のタイトルと本文を 3〜5 個）、ConversationStart の挨拶とクイック返信（3〜5 個）、会話経路、ナレッジ、MCP 接続先、公開情報（短い説明・詳細な説明・背景色・開発者名）を設計提示し、承認を得る。既存エージェントはトピックの用途・依存先と維持／変更／削除案を確認し、削除は ID ごとに承認を得る（[既存エージェント改善パターン](#既存エージェント改善パターン)）。

設計承認後・Bot 作成前に [アイコン作成リファレンス](../../standard/references/icon-creation.md) に従い 3〜4 案を提案して選択を受け、PNG 240 / 192 / 32 の 3 サイズを生成する。`bots.iconbase64` と Teams マニフェストへ登録する。

#### Bot の作成経路（v1）

```
❌ Dataverse bots テーブルへの直接 INSERT
   → PVA Bot Management Service にプロビジョニングされない
   → Copilot Studio UI で「エージェントの作成中に問題が発生しました」エラー
   → botroutinginfo が 404 になる

✅ Copilot Studio UI で手動作成 → API で設定変更のみ
```

### Step 0: Copilot Studio UI での Bot 作成（ユーザー手動）

ユーザーに依頼する際は、ソリューションの **スキーマ名（`SOLUTION_NAME`）** と **表示名** の両方を伝える。
Copilot Studio UI のドロップダウンには表示名が表示されるため、スキーマ名だけではユーザーが特定できない。

**⚠️ プロビジョニング完了を待つこと（重要）**

Bot を「作成」した直後は Dataverse に `bots` レコードが即座に作成されるが、
**デフォルトトピック・GPT コンポーネント等は PVA Bot Management Service が非同期でプロビジョニング**する。
プロビジョニングが未完了なら変更を開始しない。既定トピックは自動削除せず保持する。`scripts/deploy_agent.py` は案件固有の旧例であり、通常手順から実行しない。実行には対象 GUID・公開・削除 ID の明示承認が必要。

ユーザーには以下を案内する:

```
1. Copilot Studio UI でエージェントを作成
2. ★ 作成後、Copilot Studio UI でエージェントが完全にロードされるまで待つ
   （トピック一覧・概要ページが表示されるまで）
3. UI で対象 Bot と既存トピック・GPT コンポーネントを確認
4. 案件に必要な変更を個別に設計・承認し、通常は UI で設定する
```

```
1. https://copilotstudio.microsoft.com/ にアクセス
2. 「+ 作成」をクリック
3. エージェント名を入力
4. ★「エージェント設定 (オプション)」を展開:
   - 言語: 日本語 (日本)
   - ソリューション: 「{SOLUTION_DISPLAY_NAME}」を選択
     （スキーマ名: {SOLUTION_NAME}、表示名: {SOLUTION_DISPLAY_NAME}）
   - スキーマ名: {prefix}_agent_name
5. 「作成」をクリック
6. ★ エージェントが完全にロードされるまで待つ（トピック一覧が表示されるまで）
7. UI で Bot ID と既存構成を照合する（旧デプロイスクリプトへの入力には URL でなく正確な GUID が必要）
```

> **教訓**: UI のドロップダウンにはソリューションの「表示名」が表示される。スキーマ名だけ伝えるとユーザーがどれを選ぶか迷う。必ず「表示名: ○○○（スキーマ名: △△△）」の形式で伝える。

### Step 1: Bot 検索

- UI で確認した正確な Bot GUID と現行設定を照合する。案件固有の旧スクリプトは GUID を要求し、名前検索や URL からの自動選択で承認を代替しない

### Step 1.5: プロビジョニング完了待ち（スクリプト内で自動）

Bot の Dataverse レコードは即座に作成されるが、デフォルトトピック・GPT コンポーネントは
PVA Bot Management Service が**非同期でプロビジョニング**する。
スクリプトは自動的にポーリングして完了を待つ。

```python
def wait_for_provisioning(bot_id: str, timeout: int = 120) -> bool:
    """トピックまたは GPT コンポーネントが出現するまでポーリング"""
    elapsed = 0
    while elapsed < timeout:
        # componenttype=1 (トピック) をチェック
        topics = api_get("botcomponents", {
            "$filter": f"_parentbotid_value eq '{bot_id}' and componenttype eq 1",
            "$select": "botcomponentid"})
        if topics.get("value"):
            return True
        # componenttype=15 (GPT コンポーネント) もチェック
        gpt = api_get("botcomponents", {
            "$filter": f"_parentbotid_value eq '{bot_id}' and componenttype eq 15",
            "$select": "botcomponentid"})
        if gpt.get("value"):
            return True
        print(f"  待機中... ({elapsed}/{timeout}秒)")
        time.sleep(10)
        elapsed += 10
    print(f"  ⚠️ {timeout}秒タイムアウト")
    return False
```

```
✅ 10 秒間隔でポーリング、最大 120 秒タイムアウト
✅ componenttype=1 (トピック) と componenttype=15 (GPT) の両方をチェック
✅ タイムアウト時は変更を停止し、UI で状態を確認する
❌ プロビジョニング完了前に変更 → 一部の構成を見落とす
❌ time.sleep() で固定時間待機 → プロビジョニングが遅い環境で不足する
```

### Step 2: 既存トピックの棚卸し（通常は保持）

あいさつ・既定トピックも含め、ID・種類・依存先・維持／変更／削除案を確認する。`system_` や `schemaname` のパターンだけで削除対象を決めない。削除が必要な場合のみ各 ID と影響範囲・復旧方法の承認を受け、実行直前の一覧と照合する。`scripts/deploy_agent.py` の旧削除機能も、対象 GUID と承認済み ID の完全一致なしには実行できない。

### Step 3: 生成オーケストレーション有効化

**⚠️ UI で選択した基盤モデルを変更しないこと（重要）**

```python
# 既存 configuration を読み込み → ディープマージで既存設定を保持
bot_data = api_get(f"bots({bot_id})?$select=configuration")
existing_config = json.loads(bot_data.get("configuration", "{}") or "{}")

# ★ 必要最小限のオーバーライドのみ指定
overrides = {
    "$kind": "BotConfiguration",
    "settings": {"GenerativeActionsEnabled": True},
    "aISettings": {
        "$kind": "AISettings",
        "useModelKnowledge": True,
        "isFileAnalysisEnabled": True,
        "isSemanticSearchEnabled": True,
        "optInUseLatestModels": False,  # ★ 明示的に False — True だと基盤モデルが別モデルへ強制変更される
    },
    "recognizer": {"$kind": "GenerativeAIRecognizer"},
}

# ★ ディープマージ: 既存の gPTSettings・モデル選択・その他 UI 設定を全て保持
merged = _deep_merge(existing_config, overrides)

api_patch(f"bots({bot_id})", {"configuration": json.dumps(merged)})
```

```
❌ optInUseLatestModels: True → UI で選択した基盤モデルが別モデルに強制変更される
❌ aISettings を丸ごと上書き → モデル設定が消える
❌ gPTSettings だけ保持して他の既存キーを落とす → 設定が欠損
✅ ディープマージで既存 configuration を保持し、必要な設定のみ追加・更新
✅ optInUseLatestModels は明示的に False — UI で選択した基盤モデルを維持
✅ 既存 config に True が残っていても False で上書きする
```

### Step 4: 指示（Instructions）設定

```python
# UI コンポーネント特定 → defaultSchemaName で照合
default_schema = saved_config.get("gPTSettings", {}).get("defaultSchemaName", "")

existing = api_get("botcomponents",
    {"$filter": f"_parentbotid_value eq '{bot_id}' and componenttype eq 15",
     "$select": "botcomponentid,name,schemaname,data"})

# defaultSchemaName と一致 → 更新候補。他は保持し、依存関係を個別調査する
# 識別できなければ自動更新せず、UI 側で確認する
# 更新: api_patch("botcomponents(comp_id)", {"data": GPT_YAML})
```

#### GPT コンポーネントの安全な更新

1. **UI が作成したコンポーネントを特定して更新する**
   - `bots(id)?$select=configuration` → `configuration.gPTSettings.defaultSchemaName` で UI コンポーネントの schemaname を取得
   - API で新しい GPT コンポーネントを INSERT すると UI と API で別々のコンポーネントが存在し、UI は自分のコンポーネントしか読まない

2. **configuration を PATCH する際は既存値をディープマージする**
   - `configuration` を丸ごと上書きすると `gPTSettings.defaultSchemaName` やモデル設定が消える
   - 必ず GET → ディープマージ → PATCH
   - `optInUseLatestModels` は明示的に `False` を設定 — `True` だと UI で選択した基盤モデルが別モデルへ強制変更される
   - `aISettings` も丸ごと上書きせずディープマージで既存のモデル選択を保持

3. **GPT コンポーネントを棚卸しし、既存のものは保持する**
   - `componenttype eq 15` で全取得 → `defaultSchemaName` と一致する UI コンポーネントを特定。他のコンポーネントは参照・依存関係を調査し、削除する場合は ID ごとの明示承認と復旧計画を要する。スキーマ名だけで自動削除しない。

#### PVA YAML と Instructions の改行形式

PVA パーサーは標準 YAML のシングル改行 (`\n`) を**構造行**として認識しない。
YAML の**構造行**（kind, displayName, conversationStarters 等）はダブル改行 (`\n\n`) で区切る必要がある。
ただし `instructions: |-` ブロック内のテキストはシングル改行で記述する。

```python
# ✅ 正しい構築方法
def _build_gpt_yaml():
    # instructions ブロック（シングル改行）
    inst_block = "\n".join(f"  {line}" for line in GPT_INSTRUCTIONS.splitlines())

    # conversationStarters（ダブル改行）
    starter_lines = []
    for p in PREFERRED_PROMPTS:
        starter_lines.append(f"  - title: {p['title']}")
        starter_lines.append(f"    text: {p['text']}")
    starters_block = "\n\n".join(starter_lines)

    return (
        "kind: GptComponentMetadata\n\n"
        f"displayName: {BOT_NAME}\n\n"
        f"instructions: |-\n{inst_block}\n\n"
        f"conversationStarters:\n\n{starters_block}\n\n"
    )
```

```
❌ yaml.dump() → PVA パーサーと非互換
❌ 全行シングル改行 → conversationStarters / quickReplies が UI に反映されない
❌ 全行ダブル改行 → instructions テキストが空行だらけになる
❌ conversationStarters の title/text をダブルクォートで囲む → PVA に反映されない
✅ 構造行はダブル改行、instructions ブロック内はシングル改行
✅ conversationStarters の title/text はクォートなし
✅ displayName キーを含める（UI が表示に使用）
✅ instructions 内で単一波括弧 {変数名} を使わない → PVA が Power Fx 式として解釈し IdentifierNotRecognized エラー。自然言語で記述する
```

#### 基盤モデル選択の保持

PVA は GPT コンポーネントの `data` YAML 末尾に基盤モデル情報を格納する:

```yaml
aISettings:
  model:
    modelNameHint: <UI で選択したモデル識別子>
```

GPT コンポーネントの `data` を上書きすると、この `aISettings` セクションが消えて
UI で選択したモデル設定が失われる。

```python
# ✅ 更新前に既存データから aISettings セクションを抽出 → 新 YAML の末尾に付加
existing_data = ui_comp.get("data", "")
ai_idx = existing_data.find("\naISettings:")
if ai_idx < 0:
    ai_idx = existing_data.find("aISettings:")
if ai_idx >= 0:
    ai_settings_section = existing_data[ai_idx:].rstrip()
    final_yaml = new_yaml.rstrip("\n") + "\n\n" + ai_settings_section + "\n\n"
```

```
❌ GPT data を丸ごと上書き → 基盤モデルがデフォルトに戻る
✅ 更新前に aISettings セクションを抽出して保持
✅ 初回デプロイ後にユーザーが UI でモデルを設定 → 2 回目以降のデプロイで保持される
```

### Step 4.5: 会話の開始設定（メッセージ + クイック返信）

**⚠️ yaml.dump() / yaml.safe_load() → yaml.dump() のパイプラインは使用禁止（最重要）**

```
❌ yaml.safe_load() → 値を変更 → yaml.dump() で書き戻す
   → yaml.dump() が PVA パーサーと非互換な YAML を出力する
   → 改行入り文字列が single-quoted multiline になり UI が認識しない
   → quickReplies が消える / 会話の開始メッセージが空になる

✅ ConversationStart YAML は全体を手動で文字列構築する
   → 既存の SendActivity ID のみ正規表現で抽出して再利用
   → YAML テンプレートに変数を埋め込んで生成
```

```python
import re

# ConversationStart トピック（componenttype=9）を検索
result = api_get("botcomponents", {
    "$filter": f"_parentbotid_value eq '{bot_id}' and componenttype eq 9 and contains(schemaname,'ConversationStart')",
    "$select": "botcomponentid,schemaname,data",
})
topic = result["value"][0]
topic_id = topic["botcomponentid"]
existing_data = topic.get("data", "")

# 既存の SendActivity ID を抽出（再利用）
id_match = re.search(r'id:\s+(sendMessage_\w+)', existing_data)
send_id = id_match.group(1) if id_match else "sendMessage_fix01"

# ★ PVA 構造行はダブル改行で組み立てる（yaml.dump() 禁止）
greeting_text = GREETING_MESSAGE.replace("\n", " ")
QUICK_REPLIES = ["クイック返信テキスト1", "クイック返信テキスト2"]
lines = [
    "kind: AdaptiveDialog", "beginDialog:", "  kind: OnConversationStart",
    "  id: main", "  actions:", "    - kind: SendActivity",
    f"      id: {send_id}", "      activity:", "        text:",
    f"          - {greeting_text}", "        speak:",
    f'          - "{greeting_text}"', "        quickReplies:",
]
for qr in QUICK_REPLIES:
    lines.extend(["          - kind: MessageBack", f"            text: {qr}"])
new_data = "\n\n".join(lines) + "\n\n"

api_patch(f"botcomponents({topic_id})", {"data": new_data})
```

> **挨拶メッセージ**: 設計時にエージェントの目的に合ったテキストを提案する。
> 例: 「こんにちは！インシデント管理アシスタントです。インシデントの起票・検索・ステータス更新など、お気軽にお申し付けください。」

#### ConversationStart YAML の改行形式

ConversationStart トピック（componenttype=9）も同じダブル改行フォーマット。

```python
lines = []
lines.append("kind: AdaptiveDialog")
lines.append("beginDialog:")
lines.append("  kind: OnConversationStart")
lines.append("  id: main")
lines.append("  actions:")
lines.append("    - kind: SendActivity")
lines.append(f"      id: {send_id}")
lines.append("      activity:")
lines.append("        text:")
lines.append(f"          - {greeting_text}")  # クォートなし
lines.append("        speak:")
lines.append(f'          - "{greeting_text}"')
lines.append("        quickReplies:")
for qr in QUICK_REPLIES:
    lines.append(f"          - kind: MessageBack")
    lines.append(f"            text: {qr}")
# ダブル改行で結合
new_data = "\n\n".join(lines) + "\n\n"
```

```
❌ シングル改行 → 送信ノードが消え、quickReplies が UI に反映されない
❌ 挨拶テキストに生改行 \n を含める → YAML が壊れる（スペースに置換する）
✅ 全行ダブル改行で結合
✅ actions 配下は 4 スペースインデント
```

### Step 5: エージェント公開

```python
api_post(f"bots({bot_id})/Microsoft.Dynamics.CRM.PvaPublish", {})
```

### Step 6: 説明の設定（publish 後）

```python
# data PATCH の非同期処理が description を上書きするため publish 後に設定
api_patch(f"botcomponents({comp_id})", {"description": description_text})
```

#### 説明（Description）の保存場所

```
❌ YAML 内の description キー → UI が読まない
❌ bot エンティティの description プロパティ → 存在しない
✅ botcomponents テーブルの description カラム

注意: data PATCH の非同期処理が description を上書きする
→ 対策: publish 後に description を別途 PATCH する
```

### Step 7: Teams / Copilot チャネル公開設定

```python
# applicationmanifestinformation.teams を PATCH して Teams マニフェストを設定
bot_data = api_get(f"bots({bot_id})?$select=applicationmanifestinformation,iconbase64")
existing_ami = json.loads(bot_data.get("applicationmanifestinformation", "{}") or "{}")
existing_teams = existing_ami.get("teams", {})

# 設定値の更新（エージェントに合わせた内容を設計時に提案）
existing_teams["shortDescription"] = "簡単な説明（最大80文字）"
existing_teams["longDescription"] = "詳細な説明（最大3400文字）"
existing_teams["accentColor"] = "#0078D4"  # 背景色
existing_teams["developerName"] = "開発者名（最大32文字）"
# アイコンは Bot の iconbase64 を colorIcon/outlineIcon に設定
existing_teams["colorIcon"] = icon_b64
existing_teams["outlineIcon"] = icon_b64

existing_ami["teams"] = existing_teams

# M365 Copilot 可用性を有効化
existing_ami["copilotChat"] = {"isEnabled": True}

api_patch(f"bots({bot_id})", {"applicationmanifestinformation": json.dumps(existing_ami)})
```

```
アイコン画像の要件:
- PNG 形式必須（Teams チャネルが SVG を受け付けない）
- 3 サイズ生成: 240x240（iconbase64）、192x192（colorIcon）、32x32（outlineIcon）
- `data:` prefix なしの生 Base64 PNG で API 登録

設定項目:
| 項目 | 最大文字数 | デフォルト |
|------|-----------|-----------|
| 簡単な説明 | 80 | Microsoft Copilot Studio を使用して構築します。 |
| 詳細な説明 | 3400 | （デフォルトは汎用テキスト） |
| 開発者名 | 32 | 自分の開発者名 |
| 背景色 | - | #FFFFFF（白/透明推奨） |
| Web サイト | - | go.microsoft.com/fwlink/?linkid=2138949 |
| プライバシー | - | go.microsoft.com/fwlink/?linkid=2138950 |
| 使用条件 | - | go.microsoft.com/fwlink/?linkid=2138865 |
| M365 Copilot | - | copilotChat.isEnabled = true |
```

### Step 8: チャネル公開実行

```python
# configuration.channels に msteams / Microsoft365Copilot を追加
config = json.loads(bot_data.get("configuration", "{}") or "{}")
channels = config.get("channels", [])
# 未設定なら追加
channels.append({"channelId": "msteams", ...})
channels.append({"channelId": "Microsoft365Copilot", ...})
config["channels"] = channels
api_patch(f"bots({bot_id})", {"configuration": json.dumps(config)})

# 最終公開
api_post(f"bots({bot_id})/Microsoft.Dynamics.CRM.PvaPublish", {})
```

### Step 9: ナレッジ・ツール・トリガーの手動追加（ユーザーに依頼）

```
★ ナレッジ・ツール・トリガーは API では追加不可 — Copilot Studio UI で手動操作が必要
★ スクリプト完了後に以下の案内をユーザーに提示すること
```

**ユーザーに提示するテンプレート:**

```markdown
### Copilot Studio UI での手動設定

#### ナレッジの追加

1. Copilot Studio → エージェントを開く
2. 左メニュー「ナレッジ」→「+ ナレッジの追加」
3. [ナレッジソースの選定](knowledge-source-selection.md)で方式、ハーネス、利用権、検索品質、権限、容量を確認し、データソースを選択（Dataverse テーブル / SharePoint サイト / ファイル等）。SharePoint サイト URL 参照と「ファイルのアップロード」欄の SharePoint 取り込みは別方式
4. 対象を設定して保存

#### ツールの追加

1. 左メニュー「ツール」→「+ ツールの追加」
2. コネクタまたは MCP Server を検索して選択
   - 例: Dataverse（CRUD 操作）、Work IQ Word MCP（Word 操作）、Work IQ Mail MCP（メール送受信）等
3. 使用するアクションを有効化して保存

> **⚠️ コネクタツール vs MCP ツールの選択基準**
>
> | 操作           | 推奨ツール                             | 理由                                                                                                                           |
> | -------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
> | メール返信     | **Work IQ Mail MCP** (`mcp_MailTools`) | 「メールに返信する (V3)」コネクタは Attachments が AutomaticTaskInput として定義され、エージェントが値を解決できずスタックする |
> | Word 操作      | Work IQ Word MCP (`mcp_WordServer`)    | シンプルな MCP インターフェース                                                                                                |
> | Dataverse CRUD | Dataverse コネクタ                     | 検索・更新・作成に安定                                                                                                         |
>
> **原則: MCP 版がある操作は MCP を優先する。コネクタツールの AutomaticTaskInput が原因でスタックするリスクを回避できる。**

#### トリガーの追加（外部トリガーがある場合）

1. 左メニュー「トリガー」→「+ トリガーの追加」
2. トリガー一覧から使用するトリガーを選択し「次へ」をクリック
3. 作成済みのフローが表示されるので選択
4. 「トリガーの保存」をクリック

##### 選択可能なトリガー一覧（「おすすめ」タブ）

| トリガー名                                 | コネクタ              |
| ------------------------------------------ | --------------------- |
| Recurrence                                 | Schedule              |
| 新しい応答が送信されるとき                 | Microsoft Forms       |
| 項目が作成されたとき                       | SharePoint            |
| アイテムが作成または変更されたとき         | SharePoint            |
| ファイルが作成されたとき                   | OneDrive for Business |
| チャネルに新しいメッセージが追加されたとき | Microsoft Teams       |
| 行が追加、変更、または削除された場合       | Microsoft Dataverse   |
| 新しいメールが届いたとき (V3)              | Office 365 Outlook    |
| タスクが完了したとき                       | Planner               |
| アイテムまたはファイルが修正されたとき     | SharePoint            |
| ファイルが作成されたとき (プロパティのみ)  | SharePoint            |

> 「すべて」タブで全コネクタを検索可能。

#### 公開

1. 上記の設定完了後、右上の「公開」ボタンをクリック

#### 接続マネージャーで接続を作成（公開後・実行前）

エージェントを実行する前に、接続マネージャーで全ツールの接続を作成・認証する必要がある。
```

接続マネージャー URL:
https://copilotstudio.microsoft.com/c2/tenants/{TENANT_ID}/environments/{ENV_ID}/bots/{BOT_SCHEMA}/channels/pva-studio/user-connections

```

- `{TENANT_ID}`: .env の `TENANT_ID`
- `{ENV_ID}`: 環境 ID（`RetrieveCurrentOrganization` API で取得可能）
- `{BOT_SCHEMA}`: エージェントのスキーマ名（例: `geek_newsreporter`）

> **デプロイスクリプトが接続マネージャー URL を自動生成して表示する。**
> 未認証の接続があるとエージェントがツールを呼び出せず、処理が途中で止まる。
```

### 評価と完了判定の補足

- 内容品質と処理成功は別の観点として評価し、基準と結果を分けて記録する。処理が完了したことだけで内容品質を合格としない
- エージェントの目的に合う固定の回帰ケースを用意し、複数回実行してケース別の結果と実行間の変動を記録する
- モデルを比較するときは、入力、Instructions、出力契約、利用するナレッジ・ツール、評価基準などの条件をそろえる。モデル・設定・実行条件と、結果および変動を記録し、特定モデルや一律の合格点を標準として固定しない

## Instructions テンプレート

### Dataverse テーブル論理名は単数形（最重要）

Instructions 内で Dataverse テーブル名を指定するとき、**必ず単数形の論理名**（`LogicalName`）を使うこと。
Power Apps MCP Server・Dataverse MCP Server はテーブルの論理名（単数形）でアクセスする。
複数形（`EntitySetName`）や表示名では正しくアクセスできない。

```
❌ geek_market_insights   ← 複数形（EntitySetName）
❌ 市場インサイト          ← 表示名
✅ geek_market_insight    ← 単数形（LogicalName）
```

> **教訓**: Instructions に複数形テーブル名を記載すると、
> エージェントが MCP Server 経由で Dataverse にアクセスする際にテーブルが見つからずエラーになる。

```
あなたは「{エージェント名}」です。{目的の説明}。

## 利用可能なテーブル

### {prefix}_tablename（日本語名）
- {prefix}_column: 型（説明）
- {prefix}_status: Choice（ステータス）
  - 100000000 = 値A
  - 100000001 = 値B
- {prefix}_lookupid: Lookup → {prefix}_target_table
- createdby: システム列（作成者）

## 行動指針
1. ユーザーの意図を正確に理解し、Dataverse のデータ操作を実行する
2. レコード作成時は必須項目を必ず確認してから実行
3. 検索結果は見やすく整形して表示する（テーブル形式推奨）
4. 日本語で丁寧に応答する
5. Choice 値は整数値で指定する

## 条件分岐ルール
### データの照会 → ナレッジから検索
### 新規レコード作成 → ツール（Dataverse MCP Server）で実行
### レコード更新 → ツールで PATCH 操作
```

### Instructions に Dataverse テーブルスキーマを含める（既存エージェント改善時に特に重要）

エージェントが Dataverse テーブルを操作する場合、Instructions に **テーブル論理名・列論理名・エンティティセット名・Lookup 先** を明記する。
ナレッジとして Dataverse テーブルを追加するだけでは、エージェントがテーブル構造を正しく理解できないケースがある。

```
## 利用可能な Dataverse テーブル

### {prefix}_inquiry（問い合わせ）
- テーブル論理名: {prefix}_inquiry
- エンティティセット名: {prefix}_inquirys
- 主要列:
  - {prefix}_title: 件名
  - {prefix}_description: 詳細（複数行テキスト）
  - {prefix}_customer: Lookup → {prefix}_customer（お客様）
  - {prefix}_product: Lookup → {prefix}_product（製品）
  - {prefix}_status: Choice（100000000=新規, 100000001=対応中, 100000002=解決済み）
  - createdby: 作成者（システム列）
  - createdon: 作成日（システム列）
```

```
❌ テーブル表示名だけを Instructions に記載 → エージェントが MCP で見つけられない
❌ エンティティセット名を省略 → 検索クエリ構築時に推測が必要になる
✅ テーブル論理名 + エンティティセット名 + 列の型と説明を含める
✅ Lookup 先テーブルも論理名で記載
✅ Choice 値は整数値とラベルの両方を記載
```

## 既存エージェント改善パターン

既存エージェントへの Step 2〜8 の一括適用はしない。変更する項目のみ設計・承認し、既存トピックを保持する。
`analyze_bot.py` で現状を分析し、改善点を特定してから設計→承認→実装の流れで進める。

### 改善時の典型的な作業

1. **analyze_bot.py で現状分析**: Instructions の有無、プロンプト、挨拶、クイック返信、トピック一覧、configuration を確認
2. **既存トピックを設計時に確認**: 挨拶・問い合わせ対応等の用途と会話・連携からの依存を確認し、維持／変更／削除案を分ける
3. **改善設計を提示**: 分析結果とトピックごとの変更案を提示し、削除案は個別に承認を得る。構築時に対象を再確認し、承認された不要なカスタムトピックだけを削除する。システムトピックは保護する
4. **configuration ディープマージ**: 既存の基盤モデル設定（aISettings）を保持しつつ改善設定を追加
5. **GPT コンポーネント更新**: 既存の aISettings セクションを抽出・保持しつつ Instructions + conversationStarters を更新
6. **ConversationStart 更新**: 挨拶メッセージ + クイック返信を設定
7. **公開 + 説明設定**: PvaPublish 後に description を PATCH

### 改善時の注意点

```
❌ 既存 Bot の configuration を丸ごと上書い → 基盤モデル・チャネル設定が消える
❌ GPT コンポーネントの data を丸ごと上書い → aISettings のモデル選択が消える
✅ 既存値を GET → ディープマージ → PATCH の3ステップで更新
✅ aISettings セクションは既存 data から抽出して新 YAML 末尾に付加
✅ optInUseLatestModels は既存値に関わらず False に設定
```
