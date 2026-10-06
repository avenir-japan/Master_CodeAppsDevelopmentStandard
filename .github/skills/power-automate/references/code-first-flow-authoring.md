# Power Automate コードファースト実装ガイド

## 目的

Power Automate フローを pac / clone / export した定義で保守する場合、
コネクタの動的パラメータ、UI の解釈、公開時バリデーションの差で、
JSON が正しく見えてもデザイナーや publish で崩れることがある。

この文書は、コードファーストで Modern Flow を扱うときの実装順序と、
切り分けの優先順位をまとめる。

## 1. 最小雛形を UI で成立させてから clone する

コードベース実装の基本は、UI で保存可能な最小フローを先に成立させ、
その定義を clone して拡張すること。

### 原則

- まず Power Automate UI で最小フローを保存可能な状態まで作る
- その後に pac / clone / export で定義を取得する
- 取得した action 名、operationId、parameter shape、connectionReferences を正本として保持する
- 拡張時は既存 action を作り直すより、既存定義の近傍へ追加する

### 向いている場面

- Modern Flow をソリューション配下でコード管理する場合
- コネクタの動的パラメータ形が UI 依存で揺れやすい場合
- 既存フローの action 名や接続参照を壊さず拡張したい場合

### 避けること

- UI で一度も成立していないコネクタアクションを、JSON だけでゼロから合成する
- clone 済み定義の shape を無視して action を作り直す

## 2. import / save / publish は別ゲートとして診断する

Power Automate の実装では、次の 3 つを別の検証ゲートとして扱う。

1. import / pack が通るか
2. デザイナーで save できるか
3. publish できるか

### import / pack が通るか

- ソリューション構造
- JSON 構文
- connectionReferences の整合性
- XML / solution metadata の整合性

### save できるか

- action の配置制約
- 動的パラメータ shape
- UI が action をどう解釈しているか
- Scope / variable / runAfter の組み合わせ

### publish できるか

- コネクタの operationSchema
- 接続解決
- 公開時バリデーション
- save 済み定義と公開時に許可される定義の差

### 典型例

- import は成功、save は成功、publish だけ失敗
  - JSON 構文よりコネクタ定義や operationSchema を疑う
- import は成功、デザイナーで赤エラー
  - UI が期待する parameter shape と clone 定義の差を疑う

pack / import 成功だけをもって「フローは正しい」と判断しないこと。

## 3. docs と UI がずれたら code view と clone 定義を正本にする

Learn、swagger、過去の実装例と、Power Automate デザイナーの実際の code view が
食い違うことがある。

### 正本順位

1. 現在の環境で UI 保存済みの code view
2. その環境から pac / clone / export した定義
3. 公式 docs / swagger

### 判断基準

- docs は操作の存在確認と意味確認に使う
- 実際に送る parameter key や body 階層は、UI 保存済み定義に合わせる
- 同じ operationId でも、コードビューの階層が違えば UI 側に合わせる

### 避けること

- docs の記載だけを根拠に、UI が別 shape を期待している action を上書きする
- 別環境の code view を、そのまま現在環境の最終正本とみなす

## 4. pac solution sync の結果が怪しいときは fresh clone で切る

pac solution sync の直後に同じファイルを並列で読むと、ローカル更新途中の内容を拾い、
stale に見えることがある。

### 切り分け手順

1. sync と同時に対象 JSON を読まない
2. 取得結果が不自然なら、別ディレクトリへ fresh clone を取る
3. fresh clone と作業フォルダで結果が一致するか比較する

### 使いどころ

- 画面では保存済みなのに、ローカル clone では古い action 数に見える
- sync 後の JSON が途中状態に見える
- export の問題か、ローカル読み取り競合かを切り分けたい

### 避けること

- 1 回の sync 結果だけで「環境側が古い」と断定する
- stale に見えた時点で、すぐにフロー本体の修正に進む

## 5. 関連する基本原則

- 既定アクション優先、Graph HTTP は未サポート処理だけに限定する
- トリガー・アクション名は作成直後に固定する
- 接続参照はソリューション内で管理し、環境側の解決状態まで確認する

エージェント連携が想定されるフローでは、コード上で期待するトリガー定義、環境で確認したフローの種別、実際の呼び出し元を別々に記録する。どれか一つだけから他を断定せず、未確認ならそのまま記載する。一般的なクラウドフローとも、特定のエージェント専用フローとも、証拠なしに呼び分けない。

帳票など既存の様式へ出力する際は、差し込み対象外の固定欄を入力契約に勝手に追加せず、入力から確かめられない値を別の日時・属性から推測しない。確認済みの書式や凡例はデータ連携の修正に伴って自動で変更しない。案件ごとに差し込み対象と変更可能な範囲を確認する。

複数工程にまたがる依頼の報告では、仕様・変換処理・フロー定義への接続・関連文書などを、依頼された範囲に応じて「完了」「未着手」「要確認」に分ける。一部の成果物ができても全工程の完了とは表現せず、未接続の処理を稼働中のフローとして扱わない。

基本原則の正本は [../SKILL.md](../SKILL.md) を参照。
