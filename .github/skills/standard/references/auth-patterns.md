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
2. `AuthenticationRecord` を**実行環境のユーザーの**ホームディレクトリの `~/.power-platform-cli/auth_record_{TENANT_ID}_browser.json` に保存
3. 2回目以降: 同じ実行環境・ユーザープロファイルでレコードをロードし、利用可能な永続トークンキャッシュからサイレント取得を試みる（再認証が必要な場合もある）
4. 再認証が必要な場合: レコードを保持したままエラーを返す。対象アカウントと利用する Edge プロファイルを確認してから明示的に再認証する

### 注意点

- WSL や SSH リモート環境では `localhost` リダイレクトが機能しない場合がある
- Windows ローカルでの認証結果は別の実行環境へ自動共有されない。認証レコード単体ではトークンを移せないため、実行環境ごとに利用可能な認証方式を確認してサインインする

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
3. Device Code 経路の `TypeError` や `ClientAuthenticationError` 発生時は新しい credential を永続キャッシュなしで再構築して再認証し、レコードを保存し直す（ブラウザー経路にはこの処理はない）
4. `PP_NO_PERSISTENT_CACHE=1` で OS 永続キャッシュの**使用を停止**可能。レコードの読み書きは止まらず、既存キャッシュは削除されない

```powershell
# Python 3.14 で永続キャッシュの問題を切り分ける（このセッション中のみ）
$env:PP_NO_PERSISTENT_CACHE = "1"
# 使用する案件スクリプトを、対象環境の認証方式で再実行する
```

既存レコードを残したまま永続キャッシュだけ無効化すると、同じ実行環境でもキャッシュ内のトークンが見つからず再認証が必要になる場合がある。ブラウザー経路では既存レコードからの `get_token()` エラーを自動的に対話認証へ切り替えないため、対象アカウントを確認して `authenticate()` または `setup_environment.py --auth-only` で明示的に再認証する。Device Code 経路でレコードを初期化する必要がある場合のみ、下記の対象ファイルを特定して削除する。

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

## 実行環境とキャッシュの管理

`auth_helper.py` の認証レコードは実行ユーザーのホームディレクトリ内 `~/.power-platform-cli/` に保存される（ブラウザー用 `_browser.json`、明示 `client_id` 用 `_browser_{client_id}.json`、Device Code 用 `_device.json`）。旧版の `.auth_record_browser.json` / `.auth_record.json` は同じスクリプトディレクトリに残る場合があり、`TENANT_ID` が一致すれば新しい保存先へ**コピー**される（旧ファイルは削除されない）。いずれもアカウント識別情報を含むので共有・納品・コミットせず、実行ユーザー以外が読めないよう管理する。

永続トークンキャッシュは `TokenCachePersistenceOptions(name="power_platform_token_cache_v3")` により構成される。Microsoft の [Python API リファレンス](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.tokencachepersistenceoptions?view=azure-python) によると、既定で現在のプラットフォームのユーザーデータ保護 API によって暗号化され、利用できなければエラーとなる。本実装は平文保存へのフォールバックを許可しない。実ファイル・資格情報の保存場所や削除手段を OS 共通の固定パスとして扱わない。WSL、SSH、コンテナー、異なる OS・ユーザーではレコードと永続キャッシュを共有できるとは限らず、それぞれの実行環境で認証を設定する。

`PP_NO_PERSISTENT_CACHE=1` は**層2の構成を省略するだけ**で、既存の永続キャッシュの消去も層1の無効化も行わない（空文字列なら無効化されない）。既存レコードに対応するキャッシュが使えない場合、サイレント取得は失敗し得る。再認証が必要なら利用するテナント・アカウント・認証方式を確認して明示的に `authenticate()` を実行する。必要がある場合に限り、まず対象の実行環境・テナント・ブラウザー用 `client_id` を特定し、そのレコードだけを削除する（例: Device Code のレコードを明示的にリセットする場合）。

```powershell
$tenantId = "<対象 .env の TENANT_ID>"
$record = Join-Path $HOME ".power-platform-cli\auth_record_${tenantId}_device.json"
# 対象環境・ユーザー・認証方式とパスを確認してから実行
Remove-Item -LiteralPath $record
```

この例は **Device Code の認証レコードだけ**を削除し、ブラウザー用レコードや OS 永続トークンキャッシュを消去しない。ブラウザー用は対象の `auth_record_${tenantId}_browser.json`（明示 `client_id` 指定時は `auth_record_${tenantId}_browser_${clientId}.json`）を個別に指定する。旧版レコードが残っていると再コピーされるため、必要なら同じスクリプトディレクトリの旧版ファイルも対象を確認して整理する。永続トークンキャッシュ自体の削除が必要な場合は、このレコード削除例で完了したとみなさず、対象 OS / ユーザーのサポートされる資格情報管理・サインアウト手順を個別に確認する。共有キャッシュや他アプリの資格情報を一括削除しない。
