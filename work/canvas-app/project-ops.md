# Canvas App 案件運用メモ

> [!IMPORTANT]
> この文書は **設計書の代替ではなく、実装運用メモ** です。
> 要件、画面仕様、データ定義、受入条件の正本は、先に作成した案件設計書を参照してください。

## 1. 設計書の正本

- 案件名:
- 設計書パス:
- 設計書版数 / 更新日:
- UI 方式の決定:
  - Canvas App / Code Apps / Model-Driven Apps
- Canvas App 採用理由の参照先:

## 2. 今回この文書で管理するもの

- 実装モード
- 実装担当 / 保存担当 / 公開担当
- 実値
  - Designer URL
  - Environment ID
  - App ID
  - Data source 参照名
  - Flow 参照名
- 実装再開手順
- 設計との差分メモ

## 3. 採用モード

- 主モード:
  - MCP + coauthoring / Git Integration / single app / package
- 採用理由:
- 例外運用:
  - 例: 顧客環境移送時のみ single app を使う

## 4. 担当と役割分担

- Canvas App 実装担当:
- Power Apps Studio 操作担当:
- data source / connection 追加担当:
- Save 担当:
- Publish 担当:
- 顧客確認担当:

## 5. 実装に使う実値

### 5.1 Power Apps

- Designer URL:
- Environment ID:
- App ID:
- Browser:
- Coauthoring:
  - 有効 / 無効

### 5.2 Data source / connector

- SharePoint リスト名:
- Dataverse テーブル名:
- Canvas 上の Data source 名:
- 利用 connector 名:
- connection 追加済みか:

### 5.3 Flow / AI 連携

- Flow 表示名:
- Flow 内部名:
- Power Apps からの参照名:
- AI Builder 利用有無:

## 6. 実装再開手順

1. 設計書の正本を開く
2. この文書の「5. 実装に使う実値」を確認する
3. Power Apps Designer を開く
4. coauthoring を有効にする
5. 必要なら Canvas Apps plugin / MCP 接続状態を確認する
6. data source と connector が Studio 上で見えることを確認する
7. 実装を再開する
8. 変更後は Designer 上で確認し、Save / Publish の担当へ引き継ぐ

## 7. 実装時の注意

- data source や connection の追加は Studio 側で行う
- `compile_canvas` が通っても、Designer で最終確認する
- `single app / package` は例外運用に限定する
- 設計変更が出たら、まず設計書側に反映するかを判断する

## 8. 設計との差分メモ

| 日付       | 区分         | 内容                  | 設計書へ反映要否 | 対応者 |
| ---------- | ------------ | --------------------- | ---------------- | ------ |
| yyyy-mm-dd | 例: 実装差分 | 例: Flow 参照名を変更 | 要 / 不要        | 名前   |

## 9. 例外運用メモ

- single app を使う条件:
- package を使う条件:
- import 後の確認事項:
- 顧客環境での手動作業:

## 10. 完了前チェック

- 設計書の正本参照先が明記されている
- 採用モードが明記されている
- 実値が最新になっている
- data source / connector の担当が明記されている
- Save / Publish 担当が明記されている
- 設計との差分があれば記録されている
