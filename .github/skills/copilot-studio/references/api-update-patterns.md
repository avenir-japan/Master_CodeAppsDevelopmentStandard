# Copilot Studio API 更新パターン

## Agent Instructions の API 更新

### よくある問題

#### 1. Instructions 更新が反映されない

`botcomponents` テーブルを PATCH しただけでは、エージェントに変更が反映されない。

```python
# これだけでは不十分
api_patch(f"botcomponents({component_id})", {"content": new_yaml})
```

#### 解決策: PvaPublish アクションの呼び出し

```python
# 1. Instructions を更新
api_patch(f"botcomponents({component_id})", {"content": new_yaml})

# 2. エージェントを公開（必須）
api_post(f"bots({bot_id})/Microsoft.Dynamics.CRM.PvaPublish", {})
```

`PvaPublish` を呼ばないと、下書き状態のままで実行時に反映されない。

#### 2. aISettings セクションが消える

Instructions の YAML を完全に置き換えると、既存の `aISettings` セクションが失われる。

```yaml
# 元の YAML 構造
kind: TopicV2
aISettings:
  name: TopicName
  persona: ...
  generateKnowledge: true # ← これが消える
  recentActivities: ... # ← これも消える
instructions: |
  古い Instructions...
```

新しい Instructions だけを書くと:

```yaml
# ❌ これを PATCH すると aISettings が消失
kind: TopicV2
instructions: |
  新しい Instructions...
```

#### 解決策: 既存 YAML を保持して Instructions 部分だけ置換

```python
import re

# 1. 既存コンポーネントを取得
component = api_get(f"botcomponents({component_id})")
current_yaml = component["content"]

# 2. instructions セクションだけを置換
new_instructions = "新しい Instructions 内容..."

# 正規表現で instructions ブロックを置換
pattern = r"(instructions:\s*\|[\r\n]+)((?:[ \t]+.*[\r\n]+)*)"
replacement = f"instructions: |\n{textwrap.indent(new_instructions, '  ')}\n"
updated_yaml = re.sub(pattern, replacement, current_yaml)

# 3. PATCH
api_patch(f"botcomponents({component_id})", {"content": updated_yaml})

# 4. 公開
api_post(f"bots({bot_id})/Microsoft.Dynamics.CRM.PvaPublish", {})
```

### 更新確認方法

API 経由で更新後、以下の方法で確認:

1. **Copilot Studio UI**: エージェントを開いて Instructions を確認
2. **API で再取得**: `GET botcomponents({id})` で content を取得
3. **テスト会話**: エージェントに話しかけて新しい Instructions が反映されているか確認

### Bot ID と Component ID の取得

```python
# Bot ID の取得
bots = api_get(f"bots?$filter=name eq '{bot_name}'")
bot_id = bots["value"][0]["botid"]

# System Topic (Instructions コンポーネント) の取得
components = api_get(
    f"botcomponents?"
    f"$filter=_parentbotid_value eq '{bot_id}' "
    f"and componenttype eq 1"  # 1 = Topic
)

for comp in components["value"]:
    content = comp.get("content", "")
    if "kind: SystemTopicV2" in content or "aISettings:" in content:
        system_topic_id = comp["botcomponentid"]
        break
```

### 完全な更新スクリプト例

```python
"""Agent Instructions 更新スクリプト"""
import re
import textwrap
from auth_helper import api_get, api_post, api_patch

BOT_NAME = "MyAgent"

def update_agent_instructions(new_instructions: str):
    # 1. Bot 検索
    bots = api_get(f"bots?$filter=name eq '{BOT_NAME}'")
    if not bots["value"]:
        raise ValueError(f"Bot not found: {BOT_NAME}")
    bot = bots["value"][0]
    bot_id = bot["botid"]

    # 2. System Topic 検索
    components = api_get(
        f"botcomponents?$filter=_parentbotid_value eq '{bot_id}'"
    )

    system_topic = None
    for comp in components["value"]:
        content = comp.get("content", "")
        if "aISettings:" in content:
            system_topic = comp
            break

    if not system_topic:
        raise ValueError("System Topic not found")

    # 3. Instructions 置換
    current_yaml = system_topic["content"]
    pattern = r"(instructions:\s*\|[\r\n]+)((?:[ \t]+.*[\r\n]+)*)"
    indented = textwrap.indent(new_instructions.strip(), "  ")
    replacement = f"instructions: |\n{indented}\n"
    updated_yaml = re.sub(pattern, replacement, current_yaml)

    # 4. PATCH
    api_patch(
        f"botcomponents({system_topic['botcomponentid']})",
        {"content": updated_yaml}
    )
    print("✅ Instructions updated")

    # 5. 公開
    api_post(f"bots({bot_id})/Microsoft.Dynamics.CRM.PvaPublish", {})
    print("✅ Agent published")

if __name__ == "__main__":
    new_instructions = """
あなたは経費精算のサポートエージェントです。
以下のツールを使って業務を支援してください:
- ReceiptUpload: レシート画像の解析
- ExpenseCreate: 経費申請の作成
    """
    update_agent_instructions(new_instructions)
```

## Bot Configuration の更新

### エージェント名の変更

```python
api_patch(f"bots({bot_id})", {"name": "新しいエージェント名"})
api_post(f"bots({bot_id})/Microsoft.Dynamics.CRM.PvaPublish", {})
```

### エージェントの無効化/有効化

```python
# 無効化
api_patch(f"bots({bot_id})", {"statecode": 1})

# 有効化
api_patch(f"bots({bot_id})", {"statecode": 0})
api_post(f"bots({bot_id})/Microsoft.Dynamics.CRM.PvaPublish", {})
```

## 関連リファレンス

- [Copilot Studio トリガーパターン](trigger-patterns.md)
- [Copilot Studio ツール制限](tool-limitations.md)
