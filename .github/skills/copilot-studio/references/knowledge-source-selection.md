# ナレッジソースの登録方式と選定（Standard ハーネス）

確認日: 2026-11-05。以下は Copilot Studio の **Standard ハーネス**向け公式資料の比較。Teams / Microsoft 365 Copilot 単独利用向け cliagent（v2）に同じ UI・検索経路・課金条件が適用されるとは推定しない。採用するエージェントのハーネスと対象環境で別途確認する。

## ファイル・SharePoint の三方式

| 方式 | 登録・格納／検索 | 更新・権限 | 向く条件と制約 |
| --- | --- | --- | --- |
| ローカルファイルを直接アップロード | 個々のファイルを Dataverse に保存・索引化 | ファイルは静的。変更時は再アップロードが必要。エージェントへアクセスできる利用者が内容を参照可能 | 少数の公開範囲が共通で固定的な資料の検証。元の SharePoint ファイルのアクセス権を回答時に引き継ぐ方式ではない。Dataverse ファイル容量を消費する |
| SharePoint サイト URL を登録（「ナレッジを追加」の SharePoint） | 文書は SharePoint に残り、SharePoint 検索を利用。登録 URL とその配下を検索 | 検索インデックスに反映された内容を参照し、利用者の SharePoint 権限を確認 | 既存サイト／サイト配下を対象に、更新の鮮度・権限継承・Dataverse 容量の節約を優先する場合。検索品質は対象文書と SharePoint 検索の適合性で検証する |
| SharePoint ファイル／フォルダーを取り込む（「ファイルのアップロード」欄の SharePoint） | 選択したファイルのコピーを Dataverse に保存し、ベクトル索引による意味検索を行う。元データは SharePoint | 自動同期は公式比較で約 4～6 時間。回答前に元ファイルへの利用者権限を確認 | 対象を少数のファイル／フォルダーに絞り、全文の意味検索品質を優先する場合。Dataverse データ容量・索引容量、同期遅延、対象ファイル形式・上限を確認 |

**混同しないこと:** 「SharePoint サイト URL を登録」と「ファイルのアップロード欄から SharePoint ファイルを選ぶ」は別方式。後者は、担当者がファイルを独自の Dataverse カスタムテーブルへ手作業でコピーする設計ではない。Dataverse **テーブル**を別途ナレッジとして追加する経路もあるが、SharePoint ファイルの取り込みとは異なる。SharePoint **リスト**には別の取り込み・検索仕様があるため、上表の文書向け比較をそのまま適用しない。

**精度の評価:** Dataverse の意味検索が SharePoint 検索より常に正確とは断定しない。必要な資料を含む質問、文書更新直後の質問、権限の異なる利用者による質問、回答根拠の引用を同一セットで比較し、正答率・根拠の適合・鮮度・誤回答・応答時間を記録する。暗号化された秘密度ラベル付きファイルやパスワード保護文書は、検索できない場合がある。ラベルの取り扱いは方式ごとに確認する。

## ライセンス・容量・費用の判定

- 各方式とも、ナレッジ回答の生成に使うエージェントの利用権・公開後の呼び出し経路・Copilot Credits 条件を確認する。**SharePoint サイト方式だから必ず無償**、あるいは **Dataverse にコピーするから Power Apps Premium が必須**と一律には判定しない。
- Standard ハーネスの公式料金表では、Microsoft 365 Copilot ライセンスを持つ認証済み社内利用者が本人 ID でエージェントを使う対象 B2E 実行の生成回答等に「No charge」の条件がある。それ以外の利用者／チャネル／経路へ一般化しない。容量の利用可能性、使用量の計測、容量からの控除、従量課金、容量不足時の動作は個別に判定する（[ライセンス確認ガイド](../../standard/references/license-requirements.md)）。
- 直接アップロードと SharePoint 取り込みは Dataverse 保存容量を消費する。[非構造化ナレッジの公式資料](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-unstructured-data#limits-and-limitations)は、Dataverse に保存した SharePoint コンテンツの利用者には少なくとも Power Apps または Dynamics 365 の Basic User ライセンスと指定の Dataverse 読み取り権限が必要と記載している。これを Microsoft 365 + Copilot の契約だけで満たすと推定せず、利用者の利用権・必要なロール・保存／索引容量を案件ごとに確認する。
- Copilot Studio for Teams プランだけで必要な生成機能を利用できると推定しない。Standard ハーネスか cliagent か、作成者・利用者・実行主体の利用権を確認する。

## 検証導入パッケージの条件付き初期提案

このパッケージは Microsoft 365 + Copilot による認証済み社内利用、Teams / Microsoft 365 Copilot を初期候補とし、追加ライセンスや Credits 消費を既定案として約束しない。**既存の SharePoint サイトと権限を利用できる場合は、サイト URL をナレッジに登録する方式を第一候補**とする。独自の Dataverse 格納やファイル複製を前提とせず、元ファイルの権限を維持し、Dataverse 保存容量の追加を避けられるため。ただし、ハーネス・サイト検索対象・文書形式・検索索引の鮮度・対象利用者の認証・ライセンス／Credits 適合が確認できるまで採用を確定しない。

- サイト全体を見せず、ごく少数の固定資料でアクセス範囲が共通なら、直接アップロードを簡易検証の代替候補とする。更新は手動で、サイト内ファイル単位の権限制御は引き継がない。
- サイト URL 方式で必要な質問の検索・根拠提示が不十分で、対象文書を限定でき、同期遅延と Dataverse 容量・権限・費用を許容できるときに限り、SharePoint ファイル／フォルダー取り込みを比較検証する。**意味検索を使えることだけで高精度と決めない。**
- 顧客に既存の SharePoint サイトや対象資料がない、または対象ハーネスの対応・利用権が未確認なら、第一候補の採用は保留し、資料と条件を確認して代替構成を再提案する。

最初の検証単位は、承認済みの小規模な資料一式と権限が異なる利用者のテスト質問。同じ質問を各候補で試し、根拠・鮮度・権限漏えいがないことと管理センターの容量・使用量を確認してから選定する。共有 URL、環境 ID、顧客固有の情報をリポジトリに記載しない。

## Microsoft 公式資料

- [二つの SharePoint オプションと保存先・検索・同期の比較](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-unstructured-data#whats-the-difference-between-the-two-sharepoint-options-in-add-knowledge)
- [ローカルファイルのアップロード](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-file-upload)
- [SharePoint サイトをナレッジとして追加](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-sharepoint)
- [SharePoint ファイル・フォルダーの取り込み](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-unstructured-data#add-sharepoint-files-and-folders)
- [Dataverse テーブルをナレッジに追加](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-dataverse)
- [Copilot Credits の請求レートと No charge の適用条件](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management)
- [Copilot Studio のライセンス・サブスクリプション](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing-subscriptions)
