## Key Vault 連携メモ

このドキュメントは、環境変数の Secret 型を使うときの最小メモです。Key Vault は毎案件で必須ではないため、本書では簡潔に整理します。

## 1. 使う場面

- API キー
- OAuth クライアントシークレット
- 接続文字列
- 暗号鍵

## 2. 基本方針

- 平文テキスト型に機密値を入れない
- Secret 型の環境変数を使う場合は、顧客テナントの Azure Key Vault にある秘密値を参照する
- Azure Key Vault 側で権限管理する

## 3. 実務ポイント

- Power Platform 側には秘密値そのものではなく Key Vault への参照情報を持たせる。社内 Key Vault の参照を既定値や現在値として納品しない
- Key Vault は Power Platform と同じテナントに置き、顧客環境で参照先を設定する
- Dataverse サービスプリンシパルと必要なユーザーへ Key Vault Secrets User ロールを付与する
- Copilot Studio で参照する場合は、Microsoft Copilot Studio Service への権限付与と Secret の許可タグ設定も確認する
- Secret 型を使えるコンポーネントは Power Automate、Copilot Studio、カスタムコネクタに限定されるため、利用元の要件を先に確認する

## 4. 注意

- Key Vault 周りの UI 名称やタグ運用は変更されることがある
- 実装時は最新の Microsoft Learn を確認する
- 本リポジトリでは、Key Vault は必要案件でのみ採用する
- Power Automate で秘密値を取得する場合は、取得アクションの出力と後続アクションの入出力を保護し、実行履歴で秘密値が露出しないようにする

## 5. 関連ドキュメント

- [Microsoft Learn: Use environment variables for Azure Key Vault secrets](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables-azure-key-vault-secrets)
- [environment-variables.md](./environment-variables.md)
- [managed-solution-delivery.md](./managed-solution-delivery.md)
