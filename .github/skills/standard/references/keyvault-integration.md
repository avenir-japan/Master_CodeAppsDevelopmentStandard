## Key Vault 連携メモ

このドキュメントは、環境変数の Secret 型を使うときの最小メモです。Key Vault は毎案件で必須ではないため、本書では簡潔に整理します。

## 1. 使う場面

- API キー
- OAuth クライアントシークレット
- 接続文字列
- 暗号鍵

## 2. 基本方針

- 平文テキスト型に機密値を入れない
- Secret 型の環境変数を使う
- Azure Key Vault 側で権限管理する

## 3. 実務ポイント

- Power Platform 側には秘密値そのものではなく参照情報を持たせる
- Dataverse サービスプリンシパルや必要なサービス主体へ権限付与が必要になる
- Copilot Studio と組み合わせる場合は追加設定が必要になることがある

## 4. 注意

- Key Vault 周りの UI 名称やタグ運用は変更されることがある
- 実装時は最新の Microsoft Learn を確認する
- 本リポジトリでは、Key Vault は必要案件でのみ採用する

## 5. 関連ドキュメント

- [environment-variables.md](./environment-variables.md)
- [managed-solution-delivery.md](./managed-solution-delivery.md)
