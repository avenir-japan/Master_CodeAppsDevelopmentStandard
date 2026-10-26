## ライセンス確認ガイド

このドキュメントは、Power Platform 案件でライセンスを固定表として断定せず、都度最新の公式情報を確認するための運用ガイドです。

## 1. 基本方針

- このマスターリポジトリでは、検証導入パッケージの既定提案を **ベースライセンス（Microsoft 365 + Copilot）の範囲内** に置く
- Microsoft 365 サブスクリプションに含まれる **Copilot Studio for Teams プラン**と、別途利用権を持つ構成を混同しない。Teams プランでは生成オーケストレーションなど一部機能を利用できないため、案件の利用者・作成者のライセンスと採用機能を照合し、既定案が実現できるか確認する（[Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing-subscriptions)、[Microsoft Copilot Studio Licensing Guide](https://go.microsoft.com/fwlink/?linkid=2320995)）。ベースライセンス内という方針だけで機能の利用権を断定しない
- 既定の UI / チャネル優先順位は **Teams / Microsoft 365 Copilot → 画面 UI が本当に必要なら Canvas App を基本案** とする。Canvas App のデータソース・コネクタのライセンスは案件ごとに確認する
- Canvas App では仕様・技術要件を満たすのが難しい場合は **Code Apps / Model-Driven Apps** も代替候補として提案し、実現性・ライセンス・費用を確認してユーザー承認後に採否を決める
- Code Apps の利用者には Premium の利用権が必要。Premium ライセンスの割り当て以外に従量課金、App Pass、auto-claim も公式の前提条件に挙げられているため、案件に適用する付与方法と費用を確認する（[Microsoft Learn](https://learn.microsoft.com/en-us/power-apps/developer/code-apps/overview#license-end-users-with-power-apps-premium)、確認日: 2026-10-08）
- Dataverse カスタムテーブル、AI Builder、プレミアム / カスタムコネクタ、Credits 消費が見込まれる Copilot Studio パターンは、消費量の大小にかかわらず **ライセンスと Credits の評価項目** として案件ごとに確認する
- ライセンス要件は、納品形態ではなく構成に依存する
- Copilot Credits、Code Apps、Copilot Studio の課金条件は更新されやすい
- 利用者と実行主体のライセンス適合をそれぞれ確認し、原則として既定ベースライセンス内で成立させる
- Copilot Credits の消費ゼロを原則とし、公式情報で確認できない場合は「未確認」として扱い、ゼロ消費と推定しない
- Credits の料金表と脚注、製品別の消費ルールが一見矛盾する場合は、ハーネスの種類・チャネル・認証利用者・トリガー・実行主体・機能ごとの適用条件を照合し、判断不能なら「未確認」のまま通常案を停止する。現行の [Microsoft Copilot Studio Licensing Guide](https://go.microsoft.com/fwlink/?linkid=2320995) はハーネス別に作成時と実行時の Credits 条件を区別している。購入済み容量や付与済みクレジットで賄えることは Credits 非消費を意味しない
- 未確認事項を実機検証する場合でも、検証自体に Credits 消費や追加費用が生じ得るなら、検証範囲と費用影響についてユーザーの事前の明示承認を得る
- ベースライセンス外または Credits 消費ありの構成が避けられない場合は、代替案を先に検討する。実現が難しい場合は追加ライセンス・消費条件・費用影響を示して例外案を提示し、ユーザーの明示承認前に採用しない
- 提案、見積、納品前チェックの各タイミングで最新 docs を再確認する

- Power Automate のクラウドフローから Copilot Studio のエージェントを呼び出す自律型について、Microsoft サポートの回答（2026-10）では、エージェントが Standard ハーネスで作成され、フローで使う Copilot Studio コネクタの接続所有者に Microsoft 365 Copilot ライセンスが割り当てられ、社内の従業員向けでフェアユースの範囲内なら、エージェント側の処理はトリガーの種類によらず Copilot Credits を消費しないとされている。**この接続所有者・クラウドフロー起点の条件を裏付ける公開文書は未確認**。標準の提案には含めない代替手段とし、案件に応じて当社から提示してよい。採用時は実現可能性ゲートの判定表に各条件の適合と根拠を記録し、公開文書や実測で確認できない限りゼロ消費を確定扱いしない。フロー側のライセンス・費用は別途判定する（[Copilot Studio の課金と脚注](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management#copilot-credits-billing-rates)、[制限と Power Platform 要求](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas)）。

## 2. このパッケージで先に確認すること

最低限、次を確認します。

- Teams / Microsoft 365 Copilot を標準チャネルとして成立させられるか
- 画面 UI が本当に必要か
- 画面 UI が必要な場合、Canvas App を基本案として利用データ・コネクタのライセンスを確認したか。Canvas App では難しい場合に Code Apps / Model-Driven Apps の実現性・ライセンス・費用を評価し、ユーザー承認を得たか
- ベースライセンス範囲を超える要素が入っていないか
- 利用者と実行主体の双方で、ベースライセンス条件を満たしているか
- Copilot Credits の消費有無が経路・チャネル・トリガー等の適用条件に基づいて確認されているか
- 判定不能な経路を通常案として通していないか。例外案の条件と費用影響に明示承認があるか

### 追加ライセンス評価項目の整理

| 構成要素                                       | このパッケージでの扱い            | 確認方針                             |
| ---------------------------------------------- | --------------------------------- | ------------------------------------ |
| Teams / Microsoft 365 Copilot                  | 既定提案                          | チャネル要件と運用要件を確認         |
| Canvas App（標準コネクタ）                     | 画面 UI が必要なら候補            | データソース・利用者の条件を確認     |
| Code Apps                                      | Canvas App で難しい場合の代替候補 | 実現性・ライセンス・費用を確認       |
| Model-Driven Apps                              | Canvas App で難しい場合の代替候補 | Dataverse のライセンス条件を確認     |
| Dataverse カスタムテーブル                     | 追加ライセンス評価項目            | 最新の公式条件を確認                 |
| AI Builder                                     | 追加ライセンス評価項目            | 最新の公式条件とクレジット条件を確認 |
| プレミアム / カスタムコネクタ                  | 追加ライセンス評価項目            | 利用コネクタごとに確認               |
| 複雑な自律型フロー等の Copilot Studio パターン | 追加ライセンス評価項目            | クレジット消費条件を確認             |

## 3. 何を確認するか

最低限、次を確認します。

- UI / チャネルは Teams / Microsoft 365 Copilot で足りるか
- 画面 UI が必要なら Canvas App を基本案とし、データソース・コネクタのライセンスを確認する。実現が難しい場合は Code Apps / Model-Driven Apps も比較提案する
- Dataverse カスタムテーブルを直接使うか
- プレミアムコネクタを使うか
- Copilot Studio を使う場合、クレジット消費が発生する構成になっていないか
- クレジット非消費の根拠が、実際のチャネル、認証利用者、トリガー、実行主体、機能に適用されるか
- 自律型エージェントや高度推論を使うか
- AI Builder やプロンプトツールを使うか

## 4. 確認の進め方

### 第1段階

案件要件から、利用するコンポーネントとコネクタを洗い出します。

このとき、まず **ベースライセンス範囲内で完結する提案** を作り、そこから外れる要素だけを追加ライセンス評価項目として切り出します。

### 第2段階

最新の Microsoft Learn または公式ライセンスガイドで、次を確認します。

- Power Apps
- Power Automate
- Microsoft Copilot Studio
- AI Builder
- Power Platform 全体のライセンス FAQ

### 第3段階

顧客へは、固定値の断定ではなく、必要なライセンスの種類と確認済み日付を残します。

## 5. GitHub Copilot 利用時の推奨運用

GitHub Copilot や VS Code 上のエージェントで調査する場合は、Microsoft Learn の検索機能を使ってその時点の公式記述を確認してから回答します。

このリポジトリでは、古くなりやすい数値表を長く保持するより、最新 docs へ引き直す運用を優先します。

## 6. ドキュメントへの書き方

ライセンス章には次だけを書くのを推奨します。

- このパッケージの既定提案はベースライセンス範囲内であること
- Canvas App は画面 UI が本当に必要な場合の基本案とし、データソース・コネクタのライセンスを確認すること。Canvas App では難しい場合、Code Apps / Model-Driven Apps も代替候補として提示し、ライセンス・費用とユーザー承認を確認すること
- どの構成で追加ライセンスが発生しやすいか
- 詳細は最新の Microsoft Learn または公式ガイドを確認すること
- 見積時点の確認日を残すこと

避けるべき書き方:

- 長期間正しい前提で Copilot Credits の固定消費量を書く
- Code Apps の Premium 利用権という前提を省略する、または付与方法を Premium ライセンスの直接割り当てだけに限定する
- 顧客固有条件を無視して付与方法や費用を一律に決める

## 7. 関連ドキュメント

- [managed-solution-delivery.md](./managed-solution-delivery.md)
- [power-platform-development-standard.md](./power-platform-development-standard.md)
