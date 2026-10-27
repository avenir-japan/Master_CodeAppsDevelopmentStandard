# VS Code・GitHub Copilot 初回セットアップ

対象: 開発者の端末ごとの初回セットアップ。設定に秘密情報をコミットしない。

- 確認日: 2026-10-27
- 確認した VS Code バージョン: 1.142.0（`code --version`）
- 更新履歴: 2026-10-27 初版
- 公式情報: [VS Code Copilot ドキュメント](https://code.visualstudio.com/docs/copilot/overview)

## 1. VS Code と拡張機能

VS Code を導入し、リポジトリの [推奨拡張機能](../../../../.vscode/extensions.json) を拡張機能ビューで確認する。インストール済み拡張機能と組織の許可を確認してから進める。

公式情報: [VS Code 拡張機能](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace)

## 2. エージェントプラグイン

拡張機能ビューに `@agentPlugins` と入力して探す。表示されなければ、コマンドパレットで「Preferences: Open User Settings (JSON)」を開き、`"chat.plugins.enabled": true` を追加する。JSON の既存項目の直後に追記する場合は前の行の末尾にカンマが必要。組織ポリシーで制御される場合があるため、既定値は各自の画面で確認する。既存設定を削除しない。

公式情報: [VS Code Agent Plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins)、[ユーザー設定の編集](https://code.visualstudio.com/docs/configure/settings)、[Copilot 設定](https://code.visualstudio.com/docs/copilot/copilot-settings)

## 3. Microsoft Learn MCP Server

このリポジトリの [`.vscode/mcp.json`](../../../../.vscode/mcp.json) に登録済み。初回は MCP サーバーの信頼・起動を許可する。新しいチャットで「Microsoft Learn MCP のツールで Copilot Studio のソリューションのインポート手順を調べて」と依頼し、`microsoft_docs_search` 等の呼び出しを確認する。

呼ばれない場合は、MCP サーバー一覧で起動状態と出力ログを確認する。設定ファイルの場所が原因の場合、既存の設定を削除・上書きせず、ワークスペース直下の `.mcp.json`（`mcpServers` 形式）への切り替えを検討する。この形式には試験的設定 `chat.mcp.workspaceRootConfig.enabled` の有効化が必要で、`.vscode/mcp.json`（`servers` 形式）は現行 VS Code の案内では互換性のため維持されている。切り替えは同じサーバーを二重登録しないよう管理者と確認し、単純なファイル移動はしない。認証情報を追加しない。

公式情報: [Microsoft Learn MCP Server](https://learn.microsoft.com/training/support/mcp)、[VS Code MCP サーバー設定](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)

## 4. Azure 上の指定モデル

モデル選択の歯車（Manage Language Models）から Add Models → Azure を選び、グループ名と本人が入力する API キーを登録する。`chatLanguageModels.json` には、社内で案内されたデプロイ名・表示名・エンドポイントとモデルに対応する機能・上限を設定する。API キーは VS Code の入力画面に本人が入力し、ファイルやリポジトリに書かない。グループやモデルの具体名は社内の案内に従う。

以下は入力欄の**形だけ**を示す。`0` は実際の上限ではなく、モデルに合わせて入力するための仮置きであり、そのまま保存して使わない。入力上限と出力上限の合計はモデルの上限以内とする。`toolCalling`・`vision`・`thinking` はモデルで対応している場合にのみ `true` を設定する。

```json
[
  {
    "name": "＜グループ名＞",
    "vendor": "azure",
    "models": [
      {
        "id": "＜Azure のデプロイ名＞",
        "name": "＜モデル選択に表示する名前＞",
        "url": "＜Azure ポータル等で確認したエンドポイント URL＞",
        "toolCalling": true,
        "vision": true,
        "maxInputTokens": 0,
        "maxOutputTokens": 0,
        "thinking": true
      }
    ]
  }
]
```

既定の Copilot ハーネスで使用する場合は `chat.agentHost.byokModels.enabled` の設定・組織ポリシーを確認する。表示されない場合は、自社キーのモデルの利用許可、ツール呼び出し対応、VS Code の再起動、「その他のモデル」を順に確認する。モデルの実際の能力や設定値は社内の案内と Azure 側の情報で照合する。

公式情報: [VS Code Language Models](https://code.visualstudio.com/docs/copilot/language-models)、[Copilot 設定](https://code.visualstudio.com/docs/copilot/copilot-settings)、[Azure OpenAI モデル](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models)

## 5. 権限モード

社内の開発環境・開発用リポジトリでは、承認の確認を減らすため Allow all または Autopilot を推奨する。確認なしでファイル編集・コマンド実行が進むため、対象を限定し、変更内容と実行結果を必ず確認する。選択肢が表示されない場合は組織のポリシーを確認し、制限を回避しない。

公式情報: [Manage approvals and permissions](https://code.visualstudio.com/docs/agents/run/approvals)、確認日: 2026-10-27。確認環境の VS Code: 1.102.0 (x64)。

### できること

- **Allow all**: ファイル編集・ターミナルのコマンド・外部ツールの呼び出しを、確認なしで実行する。
- **Autopilot**: Allow all と同じくすべてのツールを自動承認したうえで、エラー時に再試行し、作業を止める質問にも自動で応答し、タスクが完了したと判断するまで作業を続ける。例: SPEC.md に沿った実装→テスト→エラー修正を、途中で承認せずに進める。
- **選び方**: Autopilot は Copilot harness セッションではチャット入力欄のモード選択で選ぶ（Local harness セッションでは権限の選択で選ぶ）。初めて Allow all または Autopilot を選ぶと警告が出る。
- **注意**: 信頼できるワークスペースでだけ使う。サンドボックスを有効にしていれば、ターミナルのファイル・ネットワークの制限は残る。組織の設定で選択肢が表示されない場合がある。

## 6. 通常ブラウザでの認証・操作

社内ポリシーで VS Code 内ブラウザが使えない場合は、ポータル操作に限り、Copilot が示した URL を指定の Edge プロファイルの通常ブラウザで人が開く。既存のサインイン状態を優先し、要求された場合だけ本人がサインイン・操作して完了を伝える。Power Platform の API／CLI 作業では既存の認証プロファイルと Python の認証レコード・永続トークンキャッシュからのサイレント取得を優先し、毎回ブラウザ認証しない。これらの認証状態は同一とは限らず、失効時やポリシーによる要求時には再認証が必要となる。Python の対話認証で指定の Edge プロファイルが開くかも確認する。[ブラウザ自動化方針](browser-automation.md) と [対話型セットアップ](interactive-setup.md) に従い、ポリシーを回避する自動化は行わない。

公式情報: [VS Code の利用ガイド](https://code.visualstudio.com/docs)（VS Code 内ブラウザの組織内での利用可否は社内ポリシーによる。公開手順の該当ページは未確認）

## 7. Copilot Chat・Copilot Cowork と GitHub の接続

管理者が展開済みの githubmcp プラグインを有効にし、初回に各自の GitHub アカウントでサインインする。「マスターリポジトリの README を読んで」と依頼して参照できることを確認する。Copilot Chat・Copilot Cowork からは GitHub を**読むだけ**にし、変更は VS Code の GitHub Copilot で行う。プラグインの展開状態と名称は管理者に確認する。最終パッケージ（ZIP）の中身の検査は VS Code の GitHub Copilot で行い、結果をテキストで残す。Copilot Chat・Copilot Cowork の GitHub 接続では、ZIP の中身を直接検査できない場合がある（2026 年 10 月時点の社内での確認。ツールの更新で変わり得る）。

公式情報: [Microsoft 365 Copilot のエージェントとプラグイン](https://learn.microsoft.com/microsoft-365-copilot/extensibility/overview)、[Microsoft 365 Copilot の GitHub コネクタ](https://learn.microsoft.com/microsoftsearch/github-connector)（githubmcp の管理者展開・初回サインイン操作の公開手順は未確認）

## 8. トラブルシュート

| 症状 | 確認すること | 対処 |
|---|---|---|
| `@agentPlugins` が表示されない | `chat.plugins.enabled` と組織ポリシー | ユーザー設定と組織の許可を確認する |
| Learn MCP のツールが呼ばれない | サーバー一覧、起動・信頼、出力ログ、設定ファイルの形式 | [手順 3](#3-microsoft-learn-mcp-server)で既存設定を保持して切り分ける |
| Azure モデルが選択肢にない | 自社キーの利用許可、ツール対応、モデル一覧 | [手順 4](#4-azure-上の指定モデル)に従い再起動・「その他のモデル」を確認する |
| 権限モード・統合ブラウザが使えない | 組織ポリシー、選択した Edge プロファイル | 制限を回避せず、[代替手順](browser-automation.md#組織のポリシーで-vs-code-統合ブラウザが使えない場合)を使う |
| GitHub の資料が読めない | プラグイン有効化、各自のサインイン、リポジトリへの権限 | 管理者と接続・閲覧権限を確認する |

公式情報: [VS Code MCP サーバーのトラブルシュート](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)、[VS Code Agent Plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins)
