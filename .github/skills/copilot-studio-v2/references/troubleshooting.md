# copilot-studio-v2 — トラブルシューティング

新アーキテクチャ（cliagent）で遭遇しやすい問題と対処をまとめる。
正常系の判断と前提は [../SKILL.md](../SKILL.md) を参照。

## よくあるエラー

| 症状                                         | 原因                                | 対処                                |
| -------------------------------------------- | ----------------------------------- | ----------------------------------- |
| `0x8004023b "Connection State is closed"`    | 変更直後で認可セッション未確立      | 少し待ってリトライ                  |
| `undeclared property 'parentbotcomponentid'` | 親ナビゲーション名が誤り            | `ParentBotComponentId` を使う       |
| bot の `$select` で 400                      | 新アーキに存在しない列を指定        | まず全体取得して必要列だけ見る      |
| `0x80040265`                                 | `bots` 更新時に `name` が欠けている | PATCH 時に `name` を同送する        |
| 公開時 `1 missing connection reference`      | MCP 追加後のバインド不整合          | MCP を削除 → 再追加 → 再公開        |
| 公開後も MCP がエラー                        | Confirm 未実施                      | UI で Confirm を実施                |
| Confirm を押しても接続できない               | 古い接続参照が残っている            | 削除 → 再追加 → 再公開 → 再 Confirm |
| 日本語出力で `UnicodeEncodeError`            | Windows コンソール既定の文字コード  | UTF-8 前提で出力する                |

## 切り分けの順序

1. まず v1 / v2 を取り違えていないか確認する
2. v2 なら `bots.configuration` と botcomponents のどちらが論点か切り分ける
3. MCP 関連なら API ではなく UI の状態を疑う
4. 公開エラーは再公開だけでなく **Confirm** の有無まで確認する
5. 接続系エラーはコネクタ接続の承認状態も見る

## よくある誤解

- v1 の GPT YAML ルールを v2 に持ち込む
- MCP 追加後、再公開だけで反映されると思う
- Dataverse 上のレコード差分だけで Confirm 相当を説明しようとする
- v2 を Code Apps 埋め込み用途にも使えると誤認する
