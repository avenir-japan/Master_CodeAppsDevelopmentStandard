# Canvas App data source and connector boundary

Canvas App の AI 編集で、**何を Studio 側で人がやり、何を AI が続けて扱えるか** の境界を整理する。

## 1. 基本原則

data source、connection、connector の追加は **Power Apps Studio 側で実施** する。
AI は、その後に見えるようになった data source や API を前提に設計・編集・検証を続ける。

## 2. AI が直接できないこと

- SharePoint 接続の新規作成
- Dataverse 接続の新規追加
- SQL / Excel / OneDrive などの認証操作
- custom connector の接続確立

これらは Studio の Data パネルや接続 UI で人が行う。

## 3. 人が Studio でやること

1. Data パネルを開く
2. Add data を選ぶ
3. 対象の data source / connector を検索する
4. 認証し、対象リスト・テーブル・ファイル・接続先を選ぶ

## 4. その後に AI が扱えること

- `list_data_sources` で data source 一覧を確認する
- `get_data_source_schema` で列名と型を確認する
- `list_apis` で connector 一覧を確認する
- `describe_api` で操作と引数を確認する
- それを前提に `pa.yaml` や Power Fx を編集する

## 5. なぜこの境界があるか

- 接続作成は認証や UI 操作を伴う
- 接続先の選択は tenant / environment / permission 依存が大きい
- AI 側で安全に自動化できる境界を超えるため

## 6. 実務上の進め方

1. 必要な data source / connector を洗い出す
2. 人が Studio で追加する
3. AI が一覧と schema を確認する
4. その前提で画面や formula を実装する

## 7. この文書を参照すべきケース

- 「SharePoint をつないでから gallery を作りたい」
- 「Dataverse テーブルを追加したい」
- 「Office 365 Users を使った People Picker を作りたい」
- 「connector を追加したのに AI から見えない」
