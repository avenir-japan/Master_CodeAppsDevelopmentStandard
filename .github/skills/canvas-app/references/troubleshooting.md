# Canvas App トラブルシューティング

Canvas App の取得・編集・import・UI 調整・compile で頻出する問題と対処法。

## 1. PAC CLI 制約と回避策

### 1.1 app 名指定 pull を優先する場面がある

- `canvas-app.config.json` の `appId` や `studioUrl` が **古い app を指す** ことがある。
- 正本確認や再取得では `pac canvas download --name "<AppName>"` が安全な場合がある。

```bash
# appId 指定より名前指定が安全なケース
pac canvas download --name "MyCanvasApp" --file-name current.msapp
```

### 1.2 SourceCode pack が壊れる場合がある

- `pac canvas pack --layout SourceCode` は app によって `ValidateSources` で **FormatException** で失敗することがある。
- clean な unpack / repack でも再現する場合は、YAML 自体ではなく **PAC 側の問題** を疑う。

### 1.3 回避策: msapp を ZIP として扱う

msapp は ZIP 形式なので、次の回避策が使える。

1. msapp を ZIP として展開する
2. `Src/*.pa.yaml` を編集する
3. 必要なら `Controls/*.json` も編集する
4. ZIP として再封入し、拡張子を `.msapp` に戻す

> [!WARNING]
> `Src/*.pa.yaml` だけを直しても、import 後の見た目に反映されない場合がある。
> その場合は `Controls/4.json` などの **コントロール定義** にも旧値が残っていないか確認する。
> pa.yaml と Controls/\*.json の **両方** を揃えて初めて反映される。

具体的な取得・編集・再封入・import 手順は
[import / deploy runbook](import-deploy-runbook.md) を参照。

## 2. Attachments UI 崩れの直し方

### 2.1 崩れやすい原因

- Attachments コントロール本体の幅と高さが既定値のまま
- 親 DataCard の幅や高さが既定値のまま
- `DataCardKey` ラベルが表示されたまま
- AutoLayout 側の親コンテナ高さが不足している

### 2.2 最初に確認するポイント

1. 親コンテナの `Height`
2. ManualLayout コンテナの `Height`
3. Attachments データカードの `Width` / `Height` / `X`
4. `DataCardKey.Visible`
5. Attachments 本体の `Width` / `Height` / `X` / `Y`
6. `NoAttachmentsText` と `Tooltip`

### 2.3 実践ルール

- **本体だけでなく親 DataCard まで含めてサイズ調整** する
- 見出しラベルの既定表示は不要なら消す（`DataCardKey.Visible = false`）
- `Fill` と `HoverFill` を周辺カードと揃えて視覚ノイズを減らす

## 3. compile と検証の運用

### 3.1 coauthoring 未接続 compile の限界

- coauthoring 未接続の compile は **false negative** やコネクタ未解決エラーを出すことがある。
- 接続系エラーが多発する場合は、**Designer を開いた状態で最終確認** する。

### 3.2 compile は通るが画面が変わらない

- compile が成功しても画面が変わらない場合は、まず **別の app を開いていないか** を疑う。
- `canvas-app.config.json` や手元メモの appId ではなく、**Designer の URL に含まれる app-id を正** として確認する。
- coauthoring live 反映では、Designer タブを前面表示し続ける必要はないが、**タブを閉じると反映経路が切れる**。

切り分け順:

1. Designer の URL の `app-id` が対象 app と一致しているか
2. いま見ている画面が本当にその app の Designer か
3. タブを閉じていないか、サインアウトしていないか、セッションが切れていないか

### 3.3 coauthoring セッション切れ

- `sync_canvas` や `compile_canvas` が通っても結果が不自然な場合は、coauthoring セッションが切れていることがある。
- その場合は、Designer を開き直して coauthoring を有効にした状態で再接続する。
- 最終的な保存の正本は Designer 側の **Save / Publish** であり、compile 成功だけで保存完了とみなさない。

### 3.4 ブラウザ制約

- 組織ポリシーで VS Code 内蔵ブラウザが使えない場合がある。
- その場合は最初から **外部ブラウザ前提の runbook** に切り替える。
