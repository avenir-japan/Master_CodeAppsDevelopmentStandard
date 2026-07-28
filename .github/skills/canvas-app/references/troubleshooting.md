# Canvas App トラブルシューティング

Canvas App の AI 編集、coauthoring、single app / package、UI 調整で頻出する問題と対処法。

## 1. MCP / coauthoring の基本切り分け

### 1.1 まず確認すること

- `canvas-authoring` MCP が正しく設定されているか
- `.NET 10 SDK` が入っているか
- Power Apps Studio の対象 app で coauthoring が有効か
- Designer タブが開いたままか

セットアップ自体の流れは [ai-codegen-workflow](ai-codegen-workflow.md) を参照。

### 1.2 compile は通るが画面が変わらない

- compile が成功しても画面が変わらない場合は、まず **別の app を開いていないか** を疑う。
- `canvas-app.config.json` や手元メモの appId ではなく、**Designer の URL に含まれる app-id を正** として確認する。
- coauthoring live 反映では、Designer タブを前面表示し続ける必要はないが、**タブを閉じると反映経路が切れる**。

切り分け順:

1. Designer の URL の `app-id` が対象 app と一致しているか
2. いま見ている画面が本当にその app の Designer か
3. タブを閉じていないか、サインアウトしていないか、セッションが切れていないか

### 1.3 coauthoring セッション切れ

- `sync_canvas` や `compile_canvas` が通っても結果が不自然な場合は、coauthoring セッションが切れていることがある。
- その場合は、Designer を開き直して coauthoring を有効にした状態で再接続する。
- 最終的な保存の正本は Designer 側の **Save / Publish** であり、compile 成功だけで保存完了とみなさない。

### 1.4 ブラウザ制約

- 組織ポリシーで VS Code 内蔵ブラウザが使えない場合がある。
- その場合は最初から **外部ブラウザ前提の runbook** に切り替える。

## 2. PAC CLI 制約と非推奨ワークアラウンド

### 2.1 app 名指定 pull を優先する場面がある

- `canvas-app.config.json` の `appId` や `studioUrl` が **古い app を指す** ことがある。
- 正本確認や再取得では `pac canvas download --name "<AppName>"` が安全な場合がある。

```bash
# appId 指定より名前指定が安全なケース
pac canvas download --name "MyCanvasApp" --file-name current.msapp
```

### 2.2 pack / unpack は deprecated で、壊れる場合がある

- `pac canvas pack --layout SourceCode` は app によって `ValidateSources` で **FormatException** で失敗することがある。
- clean な unpack / repack でも再現する場合は、YAML 自体ではなく **PAC 側の問題** を疑う。
- そもそも `pack` / `unpack` は deprecated であり、標準運用にはしない。

### 2.3 回避策: msapp を ZIP として扱う

msapp は ZIP 形式なので、どうしても必要な場合だけ次の回避策が使える。

1. msapp を ZIP として展開する
2. `Src/*.pa.yaml` を編集する
3. ZIP として再封入し、拡張子を `.msapp` に戻す

> [!WARNING]
> Microsoft Learn では、source control の対象は `Src` 配下の `pa.yaml` のみであり、JSON は安定ソースではない。
> `Controls/*.json` の確認は、標準運用ではなく **最終手段の切り分け** として扱う。

具体的な取得・編集・再封入・import 手順は
[import / deploy runbook](import-deploy-runbook.md) を参照。

## 3. Attachments UI 崩れの直し方

### 3.1 崩れやすい原因

- Attachments コントロール本体の幅と高さが既定値のまま
- 親 DataCard の幅や高さが既定値のまま
- `DataCardKey` ラベルが表示されたまま
- AutoLayout 側の親コンテナ高さが不足している

### 3.2 最初に確認するポイント

1. 親コンテナの `Height`
2. ManualLayout コンテナの `Height`
3. Attachments データカードの `Width` / `Height` / `X`
4. `DataCardKey.Visible`
5. Attachments 本体の `Width` / `Height` / `X` / `Y`
6. `NoAttachmentsText` と `Tooltip`

### 3.3 実践ルール

- **本体だけでなく親 DataCard まで含めてサイズ調整** する
- 見出しラベルの既定表示は不要なら消す（`DataCardKey.Visible = false`）
- `Fill` と `HoverFill` を周辺カードと揃えて視覚ノイズを減らす

## 4. compile と検証の運用

### 4.1 coauthoring 未接続 compile の限界

- coauthoring 未接続の compile は **false negative** やコネクタ未解決エラーを出すことがある。
- 接続系エラーが多発する場合は、**Designer を開いた状態で最終確認** する。
