# Canvas App ALM and import options

Canvas App の **ALM、環境移送、単体受け渡し** を整理するための基準。

## 1. まず結論

- 本格的な ALM では **solutions を第一選択** にする
- `single app (.msapp)` は App 単体の保存や簡易受け渡し向け
- `package` は簡易移送向けだが、ALM の正本にはしない

## 2. 方式ごとの位置づけ

| 方式                  | 主目的                           | 向いている場面                                         | 注意点       |
| --------------------- | -------------------------------- | ------------------------------------------------------ | ------------ |
| solutions             | ALM の正本                       | Dataverse 依存、flows、connection reference を含む案件 | 標準方式     |
| single app (`.msapp`) | App 単体の受け渡し               | 単体バックアップ、簡易コピー、一時退避                 | App 単体中心 |
| package               | App と一部関連リソースの簡易移送 | Dataverse を使わない比較的単純な移送                   | ALM 非推奨   |

## 3. solutions を優先する理由

- Canvas app package は ALM 向きではない
- Dataverse 依存、flows、connection reference を含む App では package に制約がある
- 環境差分を構造化して扱いやすい

## 4. single app (`.msapp`)

single app は、Power Apps Studio の Download a copy / From file で扱う **App 単体ファイル** である。

向いている用途:

- 単体バックアップ
- 単体の受け渡し
- 簡易なローカル保存

注意点:

- 本格的な ALM の正本にはしない
- App 単体中心のため、周辺依存は別途確認が必要

## 5. package

package は Export Package / Import canvas app を使う方式で、App と一部関連リソースをまとめて運べる。

注意点:

- package 自体を書き換えて再 import する運用は標準にしない
- Dataverse 依存の App には向かない
- custom connector や connection は別途再構成が必要になる
- flows は再関連付けが必要になることがある
- update import 後は publish が必要になる

## 6. import 後の確認ポイント

- App が draft で止まっていないか
- publish が必要か
- connection を選び直す必要がないか
- flow の関連付けが切れていないか
- App Insights の設定が意図したものか

## 7. この方式を選ぶべきケース

solutions を選ぶ:

- 顧客納品
- 環境間移送
- Dataverse / flows / connection reference を含む

single app を選ぶ:

- App 単体を保存したい
- 一時的な受け渡しをしたい

package を選ぶ:

- Dataverse に依存しない簡易移送をしたい
- ALM ではなく、限定的な搬送が目的
