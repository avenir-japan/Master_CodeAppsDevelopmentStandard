## ライセンス確認ガイド

このドキュメントは、Power Platform 案件でライセンスを固定表として断定せず、都度最新の公式情報を確認するための運用ガイドです。

## 1. 基本方針

- このマスターリポジトリでは、検証導入パッケージの**条件付き初期提案**を **ベースライセンス（Microsoft 365 + Copilot）の範囲内** に置く。顧客契約・利用者／実行主体の利用権、利用可能なチャネル、既存資産と案件の確定要件を確認し、未確認なら採用を確定しない。既定提案で案件要件を上書きしない
- Microsoft 365 サブスクリプションに含まれる **Copilot Studio for Teams プラン**と、別途利用権を持つ構成を混同しない。Teams プランでは生成オーケストレーションなど一部機能を利用できないため、案件の利用者・作成者のライセンスと採用機能を照合し、既定案が実現できるか確認する（[Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing-subscriptions)、[Microsoft Copilot Studio Licensing Guide](https://go.microsoft.com/fwlink/?linkid=2320995)）。ベースライセンス内という方針だけで機能の利用権を断定しない
- 既定の UI / チャネル優先順位は **Teams / Microsoft 365 Copilot → 画面 UI が本当に必要なら Canvas App を基本案** とする。Canvas App のデータソース・コネクタのライセンスは案件ごとに確認する
- Canvas App では仕様・技術要件を満たすのが難しい場合は **Code Apps / Model-Driven Apps** も代替候補として提案し、実現性・ライセンス・費用を確認してユーザー承認後に採否を決める
- Code Apps の利用者には Premium の利用権が必要。Premium ライセンスの割り当て以外に従量課金、App Pass、auto-claim も公式の前提条件に挙げられているため、案件に適用する付与方法と費用を確認する（[Microsoft Learn](https://learn.microsoft.com/en-us/power-apps/developer/code-apps/overview#license-end-users-with-power-apps-premium)、確認日: 2026-10-08）
- Dataverse カスタムテーブル、AI Builder、プレミアム / カスタムコネクタ、Credits 消費が見込まれる Copilot Studio パターンは、消費量の大小にかかわらず **ライセンスと Credits の評価項目** として案件ごとに確認する
- ライセンス要件は、納品形態ではなく構成に依存する
- Copilot Credits、Code Apps、Copilot Studio の課金条件は更新されやすい
- 利用者と実行主体のライセンス適合をそれぞれ確認し、原則として既定ベースライセンス内で成立させる
- Copilot Credits の消費ゼロを原則とし、適用条件を公式情報または対象構成について確認済みの Microsoft サポート回答（SR）で裏付けられない場合は「未確認」として扱い、ゼロ消費と推定しない
- Credits の料金表と脚注、製品別の消費ルールが一見矛盾する場合は、ハーネスの種類・チャネル・認証利用者・トリガー・実行主体・機能ごとの適用条件を照合し、判断不能なら「未確認」のまま通常案を停止する。現行の [Microsoft Copilot Studio Licensing Guide](https://go.microsoft.com/fwlink/?linkid=2320995) はハーネス別に作成時と実行時の Credits 条件を区別している。購入済み容量や付与済みクレジットで賄えることは Credits 非消費を意味しない
- 未確認事項を実機検証する場合でも、検証自体に Credits 消費や追加費用が生じ得るなら、検証範囲と費用影響についてユーザーの事前の明示承認を得る
- ベースライセンス外または Credits 消費ありの構成が避けられない場合は、代替案を先に検討する。実現が難しい場合は追加ライセンス・消費条件・費用影響を示して例外案を提示し、ユーザーの明示承認前に採用しない
- 提案、見積、納品前チェックの各タイミングで最新 docs を再確認する
- このパッケージでは、Copilot Studio のエージェントを標準ハーネスで作成する。GitHub Copilot ハーネスは利用量課金の対象で、作成・テスト・評価・実行で Copilot Credits を消費する場合があり、その利用は Microsoft 365 Copilot ライセンスに含まれない。ハーネスは作成時に選び、作成後に相互に移せない（[概要](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/overview)、[利用料](https://learn.microsoft.com/en-us/power-platform/admin/manage-usage-github-copilot-harness)、確認日: 2026-10-27）

- Copilot Studio に紐づく自律トリガー（エージェント側のイベント等のトリガーで動くフロー）は Copilot Credits を消費する。エージェントから呼ばれるトリガー以外のエージェントフローも課金対象になる（[Billing rates and management](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management)、確認日: 2026-10-27）。
- Power Automate のクラウドフローから Copilot Studio のエージェントを呼び出す自律型について、Microsoft サポートへの問い合わせ（SR、2026-10）で、エージェントが Standard ハーネスで作成され、フローで使う Copilot Studio コネクタの接続所有者に Microsoft 365 Copilot ライセンスが割り当てられ、社内の従業員向けでフェアユースの範囲内なら、エージェント側の処理はトリガーの種類によらず Copilot Credits を消費しないと確認済み。**この接続所有者・クラウドフロー起点の条件を裏付ける公開文書は未確認**だが、SR 回答を根拠として扱う。自律型の構成・実装はこのパッケージの標準スコープや既定提案に含めず、標準案で要件を満たせない場合に検討する例外的な代替手段とする。採用時は実現可能性ゲートの判定表に SR 回答を根拠として各条件の適合を記録し、条件を満たす場合に限ってエージェント側の Credits 非消費を判定する。条件外や適合を確認できない場合は非消費と推定しない。フロー側のライセンス・費用は別途判定する（[Copilot Studio の課金と脚注](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management#copilot-credits-billing-rates)、[制限と Power Platform 要求](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-quotas)）。

### 顧客テナントでの公開後実行: 利用権・容量・請求を分ける

公開後に利用者が実行できるかは、対象の **Standard ハーネス、Teams／Microsoft 365 Copilot での認証済み社内利用、Microsoft 365 Copilot ライセンス、対象の AI 機能と呼び出し経路** を案件ごとに照合して判定する。以下は Microsoft Learn（2026-10-30 確認）と依頼者から提供された 2026-10 のサポート回答要旨に基づく。SR の回答本文は確認していない。匿名・外部利用者、他チャネル、他ハーネス、一般のクラウドフローには SR の結論を拡張しない。

| 判定する軸 | 納品前に確認すること |
| --- | --- |
| 1. 利用権・追加ライセンス | 作成者・認証利用者・接続所有者・実行主体と機能ごとの利用権。AI Builder クレジットや Power Automate Premium が不要という SR 結論は対象構成に限定する |
| 2. 対象環境で利用可能な容量 | 購入済み Copilot Studio 容量の有無と、対象環境への割り当て、テナント未割り当てプールの利用設定、または環境に紐づけた従量課金プランを確認する。明示割り当てだけを唯一の方法としない |
| 3. 使用量の計測・表示 | 管理センターで公開後の対象実行の使用量・表示条件を確認する。表示された利用量をそのまま請求・控除量とみなさない |
| 4. 購入済み容量からの控除 | 認証済み M365 Copilot 利用者の対象実行が No charge となる表・脚注・前提と、該当しない経路を区別する。容量が必要でも控除ゼロとなる条件がある |
| 5. 従量課金 | 対象実行が No charge か、環境の従量課金プランで請求され得るかを判定する。従量課金を使用するならプランと対象環境の紐付けを確認する |
| 6. 容量不足時の実行可否 | テナントに容量なし／容量があっても当該環境で利用不可を分け、公開後に対象 AI ツール・プロンプト・モデルが実行可能か確認する。非課金と実行可能は別判定とする |

[Copilot Studio の請求レートと脚注](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management)は Standard ハーネスにおける認証済み Microsoft 365 Copilot 利用者の対象 B2E 実行を No charge とする一方、エージェントフローは **「エージェントがフローを呼び出したとき」トリガー**の条件を明記し、別トリガーへ一般化しない。[容量管理](https://learn.microsoft.com/en-us/power-platform/admin/manage-copilot-studio-copilot-credits-capacity)には未割り当てテナント容量、環境割り当て、従量課金、超過時の制御が別々に記載されている。No charge と容量不足時の実行可否は別々に判定し、案件の構成・環境で照合する。エージェントのテスト、フローのテスト、プロンプトの単体テストが成功しても、**顧客テナントでの公開後実行や非課金の根拠にはならない**。

**サポート回答要旨（依頼者提供、回答時期: 2026-10、メール本文・実環境値は持ち込まない）:**

- **SR 2610090060002798**: 前提を満たす対象の AI ツール／AI Builder 機能には対象環境で利用可能な Copilot Studio 容量が必要。対象実行は購入済み容量から控除されず従量課金も発生しないとの回答。エージェントフローは「エージェントがフローを呼び出したとき」トリガー、フェアユース内が対象。対象構成では AI Builder クレジット、Power Automate Premium は不要との回答。前払い容量の環境への明示割り当ては必須とは限らず、未割り当てテナント容量の利用設定を確認。従量課金利用時は環境へのプラン紐付けが必要。
- **SR 2610140060001409**: テナントに容量がない場合と、容量が当該環境で利用できない場合について、対象前提ではエージェントの作成・公開、固定応答、生成回答、エージェントから呼ぶフローの通常アクションは動作する一方、トピック内／直接ツールとしてのプロンプトとフロー内の AI Builder 機能は使えないとの回答。設定・環境で挙動が異なり得るという留保があり、公開資料が全機能について同じ分岐を明記しているとは扱わない。

上記二つの SR は **Standard ハーネス／M365 Copilot ライセンスを持つ社内利用者による Teams／Microsoft 365 Copilot での認証済み利用／回答で扱った対象機能・経路** に限り、他チャネルには適用しない。[公式料金表](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management)の No charge 表記は対象条件の控除・課金判定を裏付けるが、「No charge でも対象環境に利用可能な容量が必要」「容量不足時にどの機能が止まるか」という細かな機能別の結論は SR に依存する。公式の[容量管理](https://learn.microsoft.com/en-us/power-platform/admin/manage-copilot-studio-copilot-credits-capacity)には超過時の一般的な停止条件やエージェントフローの例外もあるため、これと SR の『容量なし』の個別回答を同じ条件の規則として統合しない。対象環境で相違が出た場合は条件・確認日・実測結果を残し、未確認として管理者と再照会する。

## 2. このパッケージで先に確認すること

最低限、次を確認します。

- 顧客契約・チャネルの提供条件と案件要件・既存資産を照合し、Teams / Microsoft 365 Copilot を初期候補として成立させられるか
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
