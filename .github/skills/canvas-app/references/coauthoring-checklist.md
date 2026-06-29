# Canvas App coauthoring live 反映チェックリスト

Canvas App を Copilot から直接反映したいときに、最初に確認する短い手順。
**msapp を upload する方式ではなく、Power Apps Designer の coauthoring セッションに対して `.pa.yaml` の変更を反映する方式** を前提とする。

## 1. まず覚えること

1. 既存 Canvas App への変更反映は、標準運用では **coauthoring live 反映を優先** する
2. `pac canvas` には、既存 app へ `.msapp` を upload / update するコマンドはない
3. Designer タブは **前面表示不要** だが、**開いたまま維持が必要**
4. 反映後の正本保存は Designer 側の **Save**、必要なら **Publish**

## 2. 事前チェック

次の 6 点がそろっていれば始められる。

1. 対象 app を Power Apps Designer で開いている
2. Settings → Updates → Coauthoring が有効
3. ブラウザは Edge / Chrome / Firefox など Power Apps 対応ブラウザ
4. Designer の URL が取れる
5. 変更対象は既存 app であり、新規 app 作成ではない
6. 反映後に Save / Publish する人が決まっている

## 3. 実行手順

1. Designer の URL を基準に environment ID と app ID を確認する
2. Copilot / MCP を app に connect する
3. sync で server state を取得する
4. `.pa.yaml` を編集する
5. compile で live app に反映する
6. Designer 画面で見た目と動作を確認する
7. Save、必要なら Publish を実行する

## 4. うまくいかないときの見分け方

### 4.1 compile は通るが画面が変わらない

まず次を疑う。

1. 別の app を開いている
2. URL の app ID ではなく古い config 値を見ている
3. Designer タブを閉じた、またはセッションが切れている

### 4.2 compile の結果が不自然

1. coauthoring 未接続だと false negative が混ざることがある
2. 接続系エラーは Designer を開いた状態で再確認する

### 4.3 どうしても coauthoring を維持できない

その場合だけ `.msapp` export / import 運用へ切り替える。

## 5. どちらを選ぶか

| やりたいこと                  | 推奨手段              |
| ----------------------------- | --------------------- |
| 既存 app をその場で修正したい | coauthoring live 反映 |
| Copilot から直接反映したい    | coauthoring live 反映 |
| 配布用ファイルとして残したい  | msapp export / import |
| Designer を開けない           | msapp export / import |

## 6. 関連ドキュメント

- 詳細 runbook: [import / deploy runbook](import-deploy-runbook.md)
- よくある問題: [troubleshooting](troubleshooting.md)
