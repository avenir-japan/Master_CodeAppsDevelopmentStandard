# Canvas App source code and Git Integration

Canvas App の `pa.yaml` を **source control と軽微編集** のために扱うときの基準。

## 1. これは何のための方式か

この方式は、Canvas App を **Git で履歴管理し、差分レビューする** ためのモードである。

- publish 済み App の状態をリポジトリで管理する
- maker の変更をノイズ少なくレビューする
- 軽微な修正を repository 側で行う

ライブ編集や大きな UI 試行錯誤は、[ai-codegen-workflow](ai-codegen-workflow.md) 側を優先する。

## 2. 主要な考え方

- Git Integration は **source control の正本** をつくるための機能
- 変更は publish 後に Git 側へ現れる
- branch 上のコードは **published app 相当** とみなす
- 直接編集はできるが、**minor edit** を基本とする

## 3. `pa.yaml` の構造

`Src` フォルダ配下に、主に次がある。

- `App.pa.yaml`: App 全体
- `[screen name].pa.yaml`: 各 screen
- `Component/[component name].pa.yaml`: component

## 4. source control で使う対象

source control の対象として扱うのは、**`Src` 配下の `*.pa.yaml` のみ** とする。

> [!IMPORTANT]
> `msapp` 内の JSON は save / load の間で安定しない。
> そのため、JSON を source code として維持・レビューする前提は置かない。

## 5. 直接編集の境界

直接編集してよいもの:

- 文言修正
- 軽微な formula 修正
- 小さなレイアウト調整
- review しやすい範囲の property 修正

直接編集を避けるもの:

- 大規模な screen 再設計
- 新規画面を複数追加する変更
- 大量の connector / data source 依存を増やす変更
- 試行錯誤が多い UI 改修

それらは MCP + coauthoring 側で行い、安定後に source control へ載せる方が安全。

## 6. 既知の制約

- code component を含む App では、repository 上の直接編集に制約がある
- merge conflict は慎重に扱う
- App が読み込めなくなった場合は、unsupported edit を疑う

## 7. この方式を選ぶべきケース

- チームで PR レビューしたい
- 変更履歴を監査したい
- maker の変更を Git で管理したい
- 軽微な修正を repo から安全に行いたい
