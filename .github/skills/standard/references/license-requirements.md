## ライセンス確認ガイド

このドキュメントは、Power Platform 案件でライセンスを固定表として断定せず、都度最新の公式情報を確認するための運用ガイドです。

## 1. 基本方針

- ライセンス要件は、納品形態ではなく構成に依存する
- Copilot Credits、Code Apps、Copilot Studio の課金条件は更新されやすい
- 提案、見積、納品前チェックの各タイミングで最新 docs を再確認する

## 2. 何を確認するか

最低限、次を確認します。

- UI は Code Apps か Canvas Apps か
- Dataverse カスタムテーブルを直接使うか
- プレミアムコネクタを使うか
- Copilot Studio を使うか
- 自律型エージェントや高度推論を使うか
- AI Builder やプロンプトツールを使うか

## 3. 確認の進め方

### 第1段階

案件要件から、利用するコンポーネントとコネクタを洗い出します。

### 第2段階

最新の Microsoft Learn または公式ライセンスガイドで、次を確認します。

- Power Apps
- Power Automate
- Microsoft Copilot Studio
- AI Builder
- Power Platform 全体のライセンス FAQ

### 第3段階

顧客へは、固定値の断定ではなく、必要なライセンスの種類と確認済み日付を残します。

## 4. GitHub Copilot 利用時の推奨運用

GitHub Copilot や VS Code 上のエージェントで調査する場合は、Microsoft Learn の検索機能を使ってその時点の公式記述を確認してから回答します。

このリポジトリでは、古くなりやすい数値表を長く保持するより、最新 docs へ引き直す運用を優先します。

## 5. ドキュメントへの書き方

ライセンス章には次だけを書くのを推奨します。

- どの構成で追加ライセンスが発生しやすいか
- 詳細は最新の Microsoft Learn または公式ガイドを確認すること
- 見積時点の確認日を残すこと

避けるべき書き方:

- 長期間正しい前提で Copilot Credits の固定消費量を書く
- Code Apps のライセンスを無条件で断定する
- 顧客固有条件を無視して一律に Premium 必須とする

## 6. 関連ドキュメント

- [managed-solution-delivery.md](./managed-solution-delivery.md)
- [power-platform-development-standard.md](./power-platform-development-standard.md)
