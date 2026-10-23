# Power Platform 認証パターンリファレンス

## 弊社標準テナントでは Device Code を既定にしない（重要）

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

弊社の標準開発テナントでは、**条件付きアクセスポリシーや利用制限** によりデバイスコードフロー（パブリッククライアント）がブロックされる前提で扱う。
したがって、Power Platform 系スクリプトの既定認証は Device Code ではなくブラウザ対話認証とする。

### 既定設定: ブラウザー対話認証を使う

`.env` に以下を追加:

```env
PP_USE_INTERACTIVE_BROWSER=true
```

これにより `auth_helper.py` は `DeviceCodeCredential` の代わりに `InteractiveBrowserCredential` を使用する。

他テナントで作業する場合のみ、Device Code が使えるかを個別確認する。

### 動作

1. 初回: ブラウザーが開き Azure AD ログイン → MFA 完了 → トークン取得
2. `AuthenticationRecord` をホームディレクトリの `~/.power-platform-cli/auth_record_{TENANT_ID}_browser.json` に保存
3. 2回目以降: ファイルからレコードをロード → サイレントリフレッシュ（ブラウザー不要）
4. 再認証が必要な場合: レコードを保持したままエラーを返す。対象アカウントと利用する Edge プロファイルを確認してから明示的に再認証する

### 注意点

- WSL や SSH リモート環境では `localhost` リダイレクトが機能しない場合がある
- その場合は Windows ローカルで認証を完了する。認証レコード単体ではトークンを移せないため、実行環境ごとにサインインする

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
# 社内開発では初回のみブラウザー対話認証。以降はサイレント。
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

```powershell
# Python 3.14 でキャッシュ破損が発生する場合
$tenantId = "<.env の TENANT_ID>"
$env:PP_NO_PERSISTENT_CACHE="1"; Remove-Item (Join-Path $HOME ".power-platform-cli/auth_record_${tenantId}_device.json") -ErrorAction SilentlyContinue; python ./setup_dataverse.py
```

#### ブラウザー対話認証 (`PP_USE_INTERACTIVE_BROWSER=true`) のサイレントリフレッシュ

`PP_USE_INTERACTIVE_BROWSER=true` 設定時、`InteractiveBrowserCredential` はシングルトン + `AuthenticationRecord` 永続化により **初回のみ** ブラウザーが開く。

- 認証レコードファイル: `~/.power-platform-cli/auth_record_{TENANT_ID}_browser.json`（明示した `client_id` には `_{client_id}` を付けて分離）
- 旧スクリプトフォルダのレコードは `TENANT_ID` が一致した場合のみ移行し、読み込み時もテナント不一致のレコードは再認証する
- 動作:
  1. 初回: `authenticate()` でブラウザー認証 → `AuthenticationRecord` をファイルに保存
  2. 2回目以降: `AuthenticationRecord` をロード → 永続キャッシュからサイレントリフレッシュ
  3. 再認証が必要: レコードは削除せずエラーを返す。Edge プロファイル確認後、`setup_environment.py --auth-only` または `authenticate(scope)` で明示的に認証する

- **異なるスコープ** (`Dataverse` / `Flow API` / `PowerApps API`) でも同一 credential + 同一キャッシュからサイレント取得
- ブラウザーが何度も開く場合は接続先・テナントとアカウントを確認する。レコードの削除は自動実行しない:

```powershell
python .github/skills/standard/scripts/setup_environment.py --auth-only
```

永続トークンキャッシュは OS による暗号化を必須とし、暗号化できない場合に平文へフォールバックしない。`PP_NO_PERSISTENT_CACHE=1` を設定すると永続キャッシュを使用せず、再認証が必要になる可能性がある。
