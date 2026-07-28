# Canvas App coauthoring limitations

coauthoring を使うときに先に知っておくべき制約一覧。

## 1. 基本理解

coauthoring は、複数の maker が同じ App を同時編集するための機能である。
Canvas Authoring MCP も、この coauthoring セッションを前提に live editing を行う。

## 2. 主な制約

- 同時編集人数には上限がある
- 検索が使えない場合がある
- Save As が使えない
- Undo / Redo が使えない
- 別 App を開く操作に制約が出る
- authoring version の切り替えができない

## 3. 非アクティブ時の挙動

- 編集状態で 2 時間非アクティブだと、read-only 側へ移ることがある
- 反応しないまま放置すると、別 maker 側へ編集権限が移ることがある

## 4. ロケールの注意

- 最初に編集を開いた maker の locale に App の言語挙動が引っ張られる
- 別 locale で同じ App を開くと、formula エラーの原因になることがある

## 5. 競合しやすい操作

- 同じ control の同時編集
- control の rename
- 別 coauthor が追加した flow の即時利用
- AI Builder component の追加
- geospatial control の追加

## 6. 実務上の扱い

- 大きな変更を入れる人を決める
- 保存担当を決める
- locale を混在させない
- 変な挙動が出たら、セッション切れと競合を先に疑う

## 7. この文書を参照すべきタイミング

- compile は通るのに反映が不安定
- 複数人で同じ App を触る
- 編集競合や謎の formula エラーが出る
