# Power Platform 認証パターンリファレンス

## 条件付きアクセスでデバイスコード認証がブロックされる問題（重要）

### 症状

デバイスコード認証時に以下のエラーが発生:

```
AADSTS50076: Due to a configuration change made by your administrator,
or because you moved to a new location, you must use multi-factor authentication to access
```

または、デバイスコード表示後にブラウザーで認証すると:

```
申し訳ございませんが、サインイン中に問題が発生しました。
AADSTS7000218: 要求本文には、パラメーター 'client_assertion' または 'client_secret' を含める必要があります。
```

### 原因

テナントの **条件付きアクセスポリシー** がデバイスコードフロー（パブリッククライアント）をブロックしている。
これは企業テナントでよくあるセキュリティ設定。

### 解決策: ブラウザー対話認証への切り替え

`.env` に以下を追加:

```env
PP_USE_INTERACTIVE_BROWSER=true
```

これにより `auth_helper.py` は `DeviceCodeCredential` の代わりに `InteractiveBrowserCredential` を使用する。

### 動作

1. 初回: ブラウザーが開き Azure AD ログイン → MFA 完了 → トークン取得
2. `AuthenticationRecord` をファイル (`.auth_record_browser.json`) に保存
3. 2回目以降: ファイルからレコードをロード → サイレントリフレッシュ（ブラウザー不要）
4. キャッシュ期限切れ時: 自動的にブラウザーで再認証

### 注意点

- WSL や SSH リモート環境では `localhost` リダイレクトが機能しない場合がある
- その場合は Windows ローカルで認証を完了させてからレコードファイルをコピー

---

## 基本的な使い方

```python
from auth_helper import get_token, get_session, api_get, api_post, api_patch, api_delete, retry_metadata

# Dataverse Web API 用トークン（デフォルトスコープ）
token = get_token()

# Flow API 用トークン（スコープ指定）
token = get_token(scope="https://service.flow.microsoft.com/.default")

# PowerApps API 用トークン（接続検索用）
token = get_token(scope="https://service.powerapps.com/.default")

# Bearer ヘッダー付き Session
session = get_session()

# Dataverse CRUD ヘルパー
api_get("accounts?$top=1")
api_post("accounts", {"name": "Test"}, solution="SolutionName")
api_patch("accounts(id)", {"name": "Updated"})
api_delete("accounts(id)")

# メタデータ操作のリトライ（0x80040237, 0x80044363 対応）
retry_metadata(lambda: api_post("EntityDefinitions", body), "テーブル作成")

# Flow API ヘルパー
from auth_helper import flow_api_call
flow_api_call("GET", f"/providers/Microsoft.ProcessSimple/environments/{env_id}/flows")
```

#### 認証テスト

```bash
# 初回のみデバイスコード認証が走る。以降はサイレント。
python -c "import sys; sys.path.insert(0, '.github/skills/standard/scripts'); from auth_helper import get_token; print(get_token()[:20] + '...')"
```

#### MSAL Python 3.14 互換性問題

Python 3.14 では MSAL 内部トークンキャッシュ (`msal/token_cache.py`) が壊れる問題がある。

**症状**: 初回 API コールは成功するが、2回目以降で `TypeError: sequence item 0: expected str instance, dict found` が発生。`target=" ".join(target)` で scopes が dict として格納されている。

**対策** (`auth_helper.py` 実装済み):

1. `_inmemory_tokens` dict でスコープ別にトークンをインメモリキャッシュ
2. `credential.get_token()` は同じスコープで1回だけ呼び、結果をキャッシュ
3. `TypeError` や `ClientAuthenticationError` 発生時は新しい credential を永続キャッシュなしで再構築
4. `PP_NO_PERSISTENT_CACHE=1` 環境変数で OS 永続キャッシュを無効化可能

```bash
# Python 3.14 でキャッシュ破損が発生する場合
$env:PP_NO_PERSISTENT_CACHE="1"; Remove-Item .auth_record.json -ErrorAction SilentlyContinue; python ./setup_dataverse.py
```

#### ブラウザー対話認証 (`PP_USE_INTERACTIVE_BROWSER=true`) のサイレントリフレッシュ

`PP_USE_INTERACTIVE_BROWSER=true` 設定時、`InteractiveBrowserCredential` はシングルトン + `AuthenticationRecord` 永続化により **初回のみ** ブラウザーが開く。

- 認証レコードファイル: `.auth_record_browser.json`（スクリプトフォルダ直下）
- 動作:
  1. 初回: `authenticate()` でブラウザー認証 → `AuthenticationRecord` をファイルに保存
  2. 2回目以降: `AuthenticationRecord` をロード → 永続キャッシュからサイレントリフレッシュ
  3. キャッシュ期限切れ: 自動的にレコードを削除して再認証

- **異なるスコープ** (`Dataverse` / `Flow API` / `PowerApps API`) でも同一 credential + 同一キャッシュからサイレント取得
- ブラウザーが何度も開く場合はレコードファイルを削除して再認証:

```bash
Remove-Item .auth_record_browser.json -ErrorAction SilentlyContinue; python ./scripts/deploy_save_flow.py
```
