# AI Builder プロンプト 構築リファレンス

## ★ デプロイフロー概要

```
新規作成:
  Model POST → AIModelPublish → Done! (わずか2 APIコール)

更新:
  Model 検索 → Run Config PATCH → Done! (わずか2 APIコール)

削除＋再作成:
  Draft Configs DELETE → Model DELETE → 新規作成フロー
  ※ Published Training Config (state=2) は DELETE 不可 (405) → 無害
```

従来の旧パターンは Model 作成 → Training Config 作成（state=2, status=6）→ Run Config 作成（state=2, status=7）→ `_msdyn_activerunconfigurationid_value` と `statecode=1` の Model PATCH。環境によって `statecode` / `statuscode` 指定や `_value` PATCH が拒否されるため、新規作成では以下の 2 API コールを使う。

## 構築手順

### Step 1: AI Model 作成

```python
import json
import os
import requests
import time
from auth_helper import api_get, api_post, api_patch, api_delete, get_token, DATAVERSE_URL

SOLUTION_NAME = os.environ["SOLUTION_NAME"]
GPT_TEMPLATE_ID = "edfdb190-3791-45d8-9a6c-8f90a37c278a"

# ★ msdyn_TemplateId@odata.bind 形式を使用
#    _msdyn_templateid_value 形式は一部環境で拒否される
model_body = {
    "msdyn_name": PROMPT_NAME,
    "msdyn_TemplateId@odata.bind": f"/msdyn_aitemplates({GPT_TEMPLATE_ID})",
    "msdyn_sharewithorganizationoncreate": False,
}
model_id = api_post("msdyn_aimodels", model_body, solution=SOLUTION_NAME)
print(f"AI Model created: {model_id}")
time.sleep(3)  # メタデータ伝播待ち
```

### Step 2: AIModelPublish で1ステップ完全アクティブ化

```python
custom_config_str = json.dumps(CUSTOM_CONFIG, ensure_ascii=False)
token = get_token()
headers = {
    "Authorization": f"Bearer {token}",
    "OData-MaxVersion": "4.0",
    "OData-Version": "4.0",
    "Content-Type": "application/json; charset=utf-8",
}

# ★ AIModelPublish — msdyn_ プレフィックスなし!
# ★ RunConfigurationId に model_id を渡す → Run Config がその ID で作成される
r = requests.post(
    f"{DATAVERSE_URL}/api/data/v9.2/AIModelPublish",
    headers=headers,
    json={
        "TemplateId": GPT_TEMPLATE_ID,
        "ModelId": model_id,
        "RunConfigurationId": model_id,   # ← model_id を渡すのがポイント
        "ModelName": PROMPT_NAME,
        "CustomConfiguration": custom_config_str,
        "RunConfiguration": custom_config_str,
    },
)
if r.status_code >= 400:
    raise RuntimeError(f"AIModelPublish failed: {r.status_code} - {r.text[:300]}")
time.sleep(5)  # アクティベーション完了待ち

# 検証
model_state = api_get(
    f"msdyn_aimodels({model_id})?$select=statecode,_msdyn_activerunconfigurationid_value"
)
assert model_state["statecode"] == 1, "Model is not Active!"
print(f"Model Active! activeRun={model_state['_msdyn_activerunconfigurationid_value']}")
```

### Step 3: botcomponent 作成（Copilot Studio エージェント利用時のみ）

```python
# Bot の schemaname を取得して component schemaname を構築
bot_data = api_get(f"bots({bot_id})?$select=schemaname")
bot_schema = bot_data.get("schemaname", "")
action_name = PROMPT_NAME.replace(" ", "")
comp_schemaname = f"{bot_schema}.action.{action_name}"

# 既存コンポーネントを検索（べき等）
existing_comp = api_get(
    f"botcomponents?$filter=schemaname eq '{comp_schemaname}'"
    "&$select=botcomponentid"
)

# inputs YAML を構築（PVA ダブル改行フォーマット）
inputs_yaml_lines = []
for inp in INPUT_DEFINITIONS:
    inputs_yaml_lines.append("  - kind: AutomaticTaskInput")
    inputs_yaml_lines.append(f"    propertyName: {inp['id']}")
    inputs_yaml_lines.append(f"    name: {inp['id']}")
    inputs_yaml_lines.append("    shouldPromptUser: true")
    inputs_yaml_lines.append("")
inputs_yaml = "\n".join(inputs_yaml_lines)

# ★ yaml.dump() は使わない — PVA パーサーと非互換
comp_data = (
    "kind: TaskDialog\n\n"
    f"inputs:\n{inputs_yaml}\n\n"
    f"modelDisplayName: {PROMPT_NAME}\n\n"
    f"modelDescription: {PROMPT_DESCRIPTION}\n\n"
    "action:\n"
    "  kind: InvokeAIBuilderModelTaskAction\n"
    f"  aIModelId: {model_id}\n\n"
    "outputMode: All\n\n"
)

if existing_comp.get("value"):
    comp_id = existing_comp["value"][0]["botcomponentid"]
    api_patch(f"botcomponents({comp_id})", {"data": comp_data})
else:
    comp_body = {
        "name": PROMPT_NAME,
        "schemaname": comp_schemaname,
        "componenttype": 9,
        "_parentbotid_value": bot_id,
        "data": comp_data,
        "description": PROMPT_DESCRIPTION,
    }
    comp_id = api_post("botcomponents", comp_body, solution=SOLUTION_NAME)

# エージェント再公開
api_post(f"bots({bot_id})/Microsoft.Dynamics.CRM.PvaPublish", {})
```

## 既存 AI プロンプトの更新パターン

```python
# ★ プロンプト内容の更新は Run Config の PATCH だけで完了
existing = api_get(
    f"msdyn_aimodels?$filter=msdyn_name eq '{PROMPT_NAME}'"
    "&$select=msdyn_aimodelid,_msdyn_activerunconfigurationid_value,statecode"
)
if existing.get("value"):
    model = existing["value"][0]
    model_id = model["msdyn_aimodelid"]
    run_config_id = model["_msdyn_activerunconfigurationid_value"]

    if model["statecode"] == 1 and run_config_id:
        # Active Model → Run Config を PATCH するだけ
        api_patch(f"msdyn_aiconfigurations({run_config_id})", {
            "msdyn_customconfiguration": json.dumps(updated_config, ensure_ascii=False),
        })
        print("Prompt updated successfully")
    else:
        # Draft Model → 削除して再作成が確実
        _delete_model_and_configs(model_id)
        # → 新規作成フローに進む
```

## べき等デプロイ（推奨パターン）

```python
def deploy_ai_prompt():
    """AI Model をべき等でデプロイする。"""
    # 既存検索
    existing = api_get(
        f"msdyn_aimodels?$filter=msdyn_name eq '{PROMPT_NAME}'"
        "&$select=msdyn_aimodelid,statecode,_msdyn_activerunconfigurationid_value"
    )

    if existing.get("value"):
        model = existing["value"][0]
        model_id = model["msdyn_aimodelid"]

        if model["statecode"] == 1 and model.get("_msdyn_activerunconfigurationid_value"):
            # ケース 1: 既に Active → プロンプト更新のみ
            run_config_id = model["_msdyn_activerunconfigurationid_value"]
            api_patch(f"msdyn_aiconfigurations({run_config_id})", {
                "msdyn_customconfiguration": json.dumps(CUSTOM_CONFIG, ensure_ascii=False),
            })
            return model_id
        else:
            # ケース 2: Draft → 削除して再作成
            _delete_model_and_configs(model_id)

    # ケース 3: 存在しない → 新規作成
    return _create_and_activate()


def _create_and_activate():
    """Model 作成 → AIModelPublish → Active"""
    model_body = {
        "msdyn_name": PROMPT_NAME,
        "msdyn_TemplateId@odata.bind": f"/msdyn_aitemplates({GPT_TEMPLATE_ID})",
        "msdyn_sharewithorganizationoncreate": False,
    }
    model_id = api_post("msdyn_aimodels", model_body, solution=SOLUTION_NAME)
    time.sleep(3)

    custom_config_str = json.dumps(CUSTOM_CONFIG, ensure_ascii=False)
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Content-Type": "application/json; charset=utf-8",
    }
    r = requests.post(
        f"{DATAVERSE_URL}/api/data/v9.2/AIModelPublish",
        headers=headers,
        json={
            "TemplateId": GPT_TEMPLATE_ID,
            "ModelId": model_id,
            "RunConfigurationId": model_id,
            "ModelName": PROMPT_NAME,
            "CustomConfiguration": custom_config_str,
            "RunConfiguration": custom_config_str,
        },
    )
    if r.status_code >= 400:
        raise RuntimeError(f"AIModelPublish failed: {r.status_code} - {r.text[:300]}")
    time.sleep(5)
    return model_id


def _delete_model_and_configs(model_id):
    """Model と関連 Config を削除（Published Training は 405 で無視）"""
    configs = api_get(
        f"msdyn_aiconfigurations?$filter=_msdyn_aimodelid_value eq '{model_id}'"
        "&$select=msdyn_aiconfigurationid,statecode"
    )
    for c in configs.get("value", []):
        try:
            api_delete(f"msdyn_aiconfigurations({c['msdyn_aiconfigurationid']})")
        except Exception:
            pass  # Published Training (state=2) は 405 → 無視
    time.sleep(2)
    try:
        api_delete(f"msdyn_aimodels({model_id})")
    except Exception:
        pass
    time.sleep(3)
```

## Dataverse データ構造

プロンプト本体と公開後の設定は `msdyn_aimodel` と `msdyn_aiconfiguration` に保存する。Model 作成時は既存の `msdyn_aitemplate`（GPT Dynamic Prompt）を参照し、Copilot Studio にツールとして追加する場合のみ `botcomponent` も使用する。いずれも Dataverse テーブルであり、下図ではテンプレート参照と作成・更新するレコードを分けて示す。

```
既存の msdyn_aitemplate (msdyn_aitemplates)
  └─ GPT Dynamic Prompt のテンプレート ID を Model 作成時に参照

┌─────────────────────────┐
│  msdyn_aimodel          │  ← AI プロンプト本体
│  (msdyn_aimodels)       │
│                         │
│  msdyn_name             │  プロンプト名
│  _msdyn_templateid_value│  GPT Prompt テンプレート ID
│  _msdyn_activerunconfigurationid_value │  → Run Config
│  statecode=1 (Active)   │
└──────────┬──────────────┘
           │ 1:N
           ▼
┌─────────────────────────┐
│  msdyn_aiconfiguration  │  ← 設定（AIModelPublish で自動生成）
│  (msdyn_aiconfigurations│
│                         │
│  Training (type=190690000, state=2, status=6) │  Published Training
│  Run     (type=190690001, state=2, status=7)  │  Active Run Config
│    msdyn_customconfiguration = JSON            │  ← プロンプト定義本体
└─────────────────────────┘

┌─────────────────────────┐
│  botcomponent           │  ← エージェントとの紐付け（Copilot Studio 利用時のみ）
│  (botcomponents)        │
│                         │
│  componenttype=9        │  トピックと同じ型
│  kind: TaskDialog       │  AI プロンプトアクション
│  action.aIModelId       │  → msdyn_aimodel の GUID
│  _parentbotid_value     │  → エージェント (bots)
└─────────────────────────┘
```

### テンプレート ID（固定値）

| テンプレート名     | ID                                     |
| ------------------ | -------------------------------------- |
| GPT Dynamic Prompt | `edfdb190-3791-45d8-9a6c-8f90a37c278a` |

Model 作成時はこのテンプレート ID を `msdyn_TemplateId@odata.bind` に指定し、ソリューションヘッダー付きで POST する。`AIModelPublish` 後に自動生成される Config も対象ソリューションに含まれることを確認し、不足時は `AddSolutionComponent`（componenttype=401）で補完する。デフォルトソリューションだけに残さず、環境間移行を確認する。

### msdyn_customconfiguration の JSON 構造

```json
{
  "version": "GptDynamicPrompt-2",
  "prompt": [
    { "type": "literal", "text": "以下の情報を分析してください: " },
    { "type": "inputVariable", "id": "input_text" },
    { "type": "literal", "text": " を基にレポートを作成。" }
  ],
  "definitions": {
    "inputs": [
      {
        "id": "input_text",
        "text": "input_text",
        "type": "text",
        "quickTestValue": "テスト用のサンプルテキスト"
      }
    ],
    "formulas": [],
    "data": [],
    "output": {
      "formats": ["json"],
      "jsonSchema": {
        "type": "object",
        "properties": {
          "summary": { "type": "string" },
          "key_points": { "type": "array", "items": { "type": "string" } }
        }
      },
      "jsonExamples": [
        { "summary": "出力例", "key_points": ["ポイント1", "ポイント2"] }
      ]
    }
  },
  "modelParameters": {
    "modelType": "gpt-41-mini",
    "gptParameters": { "temperature": 0 }
  },
  "settings": {
    "recordRetrievalLimit": 30,
    "shouldPreserveRecordLinks": null,
    "runtime": null
  },
  "code": "",
  "signature": ""
}
```

#### prompt 配列の要素型

| type            | 説明             | 必須フィールド |
| --------------- | ---------------- | -------------- |
| `literal`       | 固定テキスト     | `text`         |
| `inputVariable` | 入力変数への参照 | `id`           |

`prompt` 配列は `literal` と `inputVariable` を交互に配置し、`inputVariable.id` を `definitions.inputs[].id` と一致させる。

#### definitions.inputs の型

| type       | 説明             | 備考                        |
| ---------- | ---------------- | --------------------------- |
| `text`     | テキスト入力     | `quickTestValue` でテスト値 |
| `document` | ドキュメント入力 | ファイルアップロード        |
| `image`    | 画像入力         | 画像ファイル                |

#### definitions.output の形式

| formats    | 説明         | 追加フィールド                     |
| ---------- | ------------ | ---------------------------------- |
| `["text"]` | テキスト出力 | なし                               |
| `["json"]` | JSON 出力    | `jsonSchema` + `jsonExamples` 必須 |

#### modelParameters.modelType の値

| 値            | モデル       |
| ------------- | ------------ |
| `gpt-41-mini` | GPT-4.1 mini |
| `gpt-41`      | GPT-4.1      |
| `o3-mini`     | o3-mini      |

`modelType` は上記の有効な値を使い、`temperature` は 0〜1 の float 値とする。

### botcomponent の YAML 構造（kind: TaskDialog）

`componenttype=9` を指定し、`schemaname` を `{botSchema}.action.{PromptNameNoSpaces}` 形式にする。YAML は `kind: TaskDialog`、`action.kind: InvokeAIBuilderModelTaskAction` とし、`action.aIModelId` に `msdyn_aimodel` の GUID（ハイフン付き小文字）を指定する。`inputs.propertyName` は `customconfiguration` の `definitions.inputs[].id` と一致させる。`shouldPromptUser: true` にするとエージェントがユーザーに入力を求める。

```yaml
kind: TaskDialog

inputs:
  - kind: AutomaticTaskInput
    propertyName: text
    name: text
    shouldPromptUser: true

modelDisplayName: AI Prompt Sample

modelDescription: AI Prompt Sample

action:
  kind: InvokeAIBuilderModelTaskAction
  aIModelId: ${AI_MODEL_ID}

outputMode: All
```

## ファイル入力（Image or Document Input）の制限事項

公式ドキュメント: https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-inputs-prompt#limitations

### 対応ファイル形式

| 条件                          | 対応形式                                                                  |
| ----------------------------- | ------------------------------------------------------------------------- |
| 標準（Code Interpreter オフ） | **PNG, JPG, JPEG, PDF** のみ                                              |
| Code Interpreter オン         | 上記 + **Word (.doc/.docx), Excel (.xls/.xlsx), PowerPoint (.ppt/.pptx)** |

### サイズ・ページ数・時間制限

| 制限項目           | 値                              |
| ------------------ | ------------------------------- |
| ファイルサイズ合計 | **25 MB 未満**（全ファイル合計）|
| ページ数           | **50 ページ未満**               |
| 処理タイムアウト   | **100 秒**（超過するとタイムアウトエラー） |

### その他の制限

- **エージェントへ直接追加したプロンプトツール**では画像・文書入力は未対応（[Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-inputs-prompt#limitations)、2026-10-30 確認）。テキストのプロンプト利用全般にフローは不要
- ファイル処理にはエージェントフロー／クラウドフロー経由等を比較し、経路ごとの入力・出力、認証・容量・課金とエージェント間のファイル受け渡しを実際に検証する。トピック内のプロンプトも直接ツールと同じ制限だとは推定しない
- 非対応ファイル形式は OneDrive for Business `ConvertFile` で PDF 変換する案等を検証する

## トラブルシューティング

### AIModelPublish 関連

| エラー | 原因 | 対策 |
|--------|------|------|
| 404 Not Found | `msdyn_AIModelPublish` を使っている | `AIModelPublish`（プレフィックスなし）を使う |
| `AnotherRunConfigAlreadyPublished` | 既に Active Run Config がある | 更新パターンを使う（Run Config PATCH）|
| 400 Bad Request | TemplateId or ModelId が不正 | GUID 形式を確認 |

### Model 作成関連

| エラー | 原因 | 対策 |
|--------|------|------|
| `CRM do not support direct update of Entity Reference` | `_msdyn_templateid_value` を使っている | `msdyn_TemplateId@odata.bind` を使う |
| `Unexpected parameter(s) statuscode` | Config 作成時に statecode/statuscode 指定 | 指定しない（AIModelPublish が設定する）|
| `undeclared property` | 存在しない nav property を使っている | `msdyn_AIModelId@odata.bind` を使う |
| 403 Forbidden | AI Builder が環境で無効 | Power Platform 管理センターで有効化 |

### botcomponent 関連

| エラー | 原因 | 対策 |
|--------|------|------|
| Duplicate schemaname | 同じ schemaname が存在 | 既存を検索して PATCH で更新 |
| YAML parse error | yaml.dump() を使った | 手動でダブル改行フォーマット構築 |
| エージェントに表示されない | componenttype が 9 でない | componenttype=9 を確認 |
| エージェントに表示されない | PvaPublish していない | 再公開する |

### フロー有効化関連

| エラー | 原因 | 対策 |
|--------|------|------|
| `GetPredictionSchema failed with BadRequest` | Model が Draft 状態 | 先に AIModelPublish で Active 化 |
| `does not contain a definition for parameter` | f-string 未使用のキー | dict キーに `f"..."` を使う |
| `InvalidOpenApiFlow` (0x80060467) | フロー定義の操作パラメータが不正 | 操作スキーマを確認 |

### 環境差異に関する既知の問題

```
以下の操作は環境によって動作が異なる:

1. _msdyn_xxx_value 形式の PATCH
   - 一部環境: 成功
   - 一部環境: "CRM do not support direct update of Entity Reference properties"
   → 解決: @odata.bind 形式を常に使う

2. Config 作成時の statecode/statuscode 指定
   - 一部環境: 成功
   - 一部環境: "Unexpected parameter(s) statuscode"
   → 解決: AIModelPublish に任せる（指定しない）

3. msdyn_ プレフィックス付きアクション (msdyn_Publish, msdyn_AIModelPublish 等)
   - 全環境: 404 Not Found
   → 解決: AIModelPublish（プレフィックスなし）を使う

4. SetState アクション
   - 全環境: 404 Not Found
   → 解決: AIModelPublish に任せる

5. PublishAIConfiguration (bound action on Run Config)
   - 新規 Model + AIModelPublish 済み: AnotherRunConfigAlreadyPublished
   - 既存 Draft Model に手動 Run Config を作った場合: 成功
   → 解決: 新規は AIModelPublish のみ。PublishAIConfiguration は不要
```

## 完全なアンチパターン集

```
❌ msdyn_AIModelPublish (msdyn_ プレフィックス付き) → 常に 404
❌ msdyn_Publish → 常に 404
❌ SetState → 常に 404
❌ PerformBoundAction → 作成自体が失敗
❌ _msdyn_templateid_value を Model POST に含める → 一部環境で拒否
❌ statecode/statuscode を Config POST に含める → 一部環境で拒否
❌ msdyn_modelrundataspecification を Config POST に含める → 400
❌ _msdyn_activerunconfigurationid_value を直接 PATCH → 一部環境で拒否
❌ msdyn_TrainingConfigurationId@odata.bind → undeclared property
❌ AIModelPublish 後に PublishAIConfiguration → AnotherRunConfigAlreadyPublished
❌ yaml.dump() で botcomponent YAML を生成 → PVA パーサーで失敗
❌ Draft Model を参照するフローを有効化 → GetPredictionSchema failed
```
