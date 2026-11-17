# ナレッジソースの登録方式と選定（Standard ハーネス）

確認日: 2026-11-06。以下は Copilot Studio の **Standard ハーネス**向け公式資料の比較。**Standard ハーネス（実行・課金の区分）と v1 / cliagent（v2、このリポジトリで扱うエージェント構成）は同じ選択軸ではない**。Teams / Microsoft 365 Copilot は利用者の入口。採用する構成で該当するナレッジ登録画面・検索経路・公開後の動作と課金条件を確認し、v2 に同じ手順が使えると推定しない（[ハーネスの概要](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)）。

## 文書と SharePoint リストの登録方式

| 対象・方式 | 登録・格納／検索 | Dataverse ナレッジ保存容量 | 更新・権限と採用条件 |
| --- | --- | --- | --- |
| SharePoint の**文書・ページ**：サイト URL を登録（「ナレッジを追加」の SharePoint） | 文書は SharePoint に残り、SharePoint 検索を利用 | 文書のコピー・検索索引については **消費しない**（[公式比較表](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-unstructured-data#whats-the-difference-between-the-two-sharepoint-options-in-add-knowledge)の `No`）。エージェントの構成情報まで一切容量を使わないという意味ではない | 利用者の SharePoint 権限を確認。既存サイトの文書を対象に、検索品質・鮮度を検証する第一候補 |
| SharePoint **リスト**： 「ファイルのアップロード」欄の SharePoint でリストを選択、またはリスト URL を入力 | [リスト登録手順](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-sharepoint#add-sharepoint-lists-as-a-knowledge-source)は Dataverse への取り込み・索引化と元リストへのリアルタイム接続を記載 | **取り込み経路では消費を見込む**。ただし同じ製品の比較表には別経路のリスト対応・容量消費 `No` ともあり、リスト全体の容量条件は未確定（下記参照） | 更新頻度・権限・行数を確認。正確な最新値や件数が要件ならナレッジ検索以外の取得経路も比較する |
| ローカルファイルを直接アップロード | 個々のファイルを Dataverse に保存・索引化 | **ファイル容量を消費**（[公式手順](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-file-upload)） | 固定資料が少数で利用者全員への公開範囲が共通の場合の代替。更新時は再アップロードし、元の SharePoint 権限は引き継がない |
| SharePoint **ファイル／フォルダー**を取り込む（「ファイルのアップロード」欄の SharePoint） | コピーと意味検索用索引を Dataverse に保存。元データは SharePoint | **消費する**（[公式比較表](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-unstructured-data#whats-the-difference-between-the-two-sharepoint-options-in-add-knowledge)の `Yes`）。ファイル・索引の容量区分と増分は環境で確認 | 約 4～6 時間の同期遅延があり、回答前に元ファイルへの利用者権限を確認。文書のサイト URL 方式で必要な回答が得られない場合の代替 |

**公式資料間の未解決点:** [リスト登録手順](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-sharepoint#add-sharepoint-lists-as-a-knowledge-source)は「ファイルのアップロード」欄からリストを追加し Dataverse に取り込むと記載。一方、[二つの SharePoint オプションの公式比較表](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-unstructured-data#whats-the-difference-between-the-two-sharepoint-options-in-add-knowledge)は、SharePoint 接続（ファイルアップロードではない方）も `SharePoint lists: Supported`、`Dataverse storage consumption: No` と記載する。両記述が同じリスト登録経路・保存対象を指すかは特定できない。**リストを容量ゼロで利用できるとも、すべてのリスト利用で容量を消費するとも断定しない。** ベースライセンス内での採用可否も未確定として扱う。顧客環境で検証できない納品では、未解決事項として引き継ぎ、追加費用のない方式として確約しない。

**混同しないこと:** サイト URL 登録、リスト URL の入力、SharePoint ファイル／フォルダーの取り込みは別の操作。リスト URL を入力するだけで文書のサイト URL 参照と同じ容量条件になるわけではない。独自の Dataverse カスタムテーブルを作らなくても、取り込み先の保存容量は消費し得る（[システムテーブルを含む容量の集計](https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage#capacity-page-details)）。Dataverse **テーブル**を別途ナレッジとして追加する経路は、上記の SharePoint 取り込みとは異なる。

**精度の評価:** Dataverse の意味検索が SharePoint 検索より常に正確とは断定しない。必要な資料を含む質問、文書更新直後の質問、権限の異なる利用者による質問、回答根拠の引用を同一セットで比較し、正答率・根拠の適合・鮮度・誤回答・応答時間を記録する。暗号化された秘密度ラベル付きファイルやパスワード保護文書は、検索できない場合がある。ラベルの取り扱いは方式ごとに確認する。

## ライセンス・容量・費用の判定

- 各方式とも、ナレッジ回答の生成に使うエージェントの利用権・公開後の呼び出し経路・Copilot Credits 条件を確認する。**SharePoint サイト方式だから必ず無償**、あるいは **Dataverse にコピーするから Power Apps Premium が必須**と一律には判定しない。
- Standard ハーネスの公式料金表では、Microsoft 365 Copilot ライセンスを持つ認証済み社内利用者が本人 ID でエージェントを使う対象 B2E 実行の生成回答等に「No charge」の条件がある。それ以外の利用者／チャネル／経路へ一般化しない。容量の利用可能性、使用量の計測、容量からの控除、従量課金、容量不足時の動作は個別に判定する（[ライセンス確認ガイド](../../standard/references/license-requirements.md)）。
- 直接アップロード、SharePoint ファイル／フォルダー取り込み、SharePoint リストの取り込みは、文書のサイト URL 参照と異なり Dataverse 保存容量の確認対象。[非構造化ナレッジの公式資料](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-unstructured-data#limits-and-limitations)は、Dataverse に保存した OneDrive / SharePoint コンテンツの利用者に少なくとも Power Apps または Dynamics 365 の Basic User ライセンスと指定の Dataverse 読み取り権限が必要と記載する。リストやローカル直接アップロードにこの文言を無条件に拡張せず、登録経路ごとの利用権・必要なロール・容量を確認する。Microsoft 365 + Copilot の契約だけで充足すると推定しない。
- Copilot Studio for Teams プランだけで必要な生成機能を利用できると推定しない。ハーネス、エージェント構成（v1 / cliagent）、利用入口（Teams / Microsoft 365 Copilot）を分け、作成者・利用者・実行主体の権利と対象環境での公開後実行を確認する。

## 検証導入パッケージの条件付き初期提案

このパッケージは Microsoft 365 + Copilot による認証済み社内利用、Teams / Microsoft 365 Copilot を初期候補とし、追加ライセンスや Credits 消費を既定案として約束しない。**文書・ページには既存 SharePoint サイト URL 参照を第一候補**とし、元の権限を維持しながら、文書コピー・索引用の Dataverse 保存容量を避ける。**リストも対象になる可能性があるため、文書だけで全要件を満たすとは決めない。**

1. 文書による説明・要約と、リストの行・件数・最新状態への質問を分ける。リストが必要なら対象リスト・列・行数・更新頻度・利用者の閲覧範囲を確認する。正確な最新値や件数が要件なら、ナレッジ登録だけでなく行の取得経路も比較する。リストの取り込みを容量ゼロの標準案として確定しない。
2. 採用するハーネス・エージェント構成と利用入口で、それぞれのナレッジ登録操作、利用者認証、回答・引用・更新・権限の動作を確認する。ドキュメントが Standard ハーネス向けだから v2 で使えない、あるいは同じ手順で使える、のどちらも推定しない。
3. 契約・作成者と利用者の利用権、Copilot Credits、取り込み方式なら対象環境の Dataverse 残容量と増分を案件側で照合する。顧客に技術調査を丸投げせず、必要な資料・閲覧権限・管理画面へのアクセスや管理者の立ち会いだけを依頼して確認を支援する。追加費用の可能性がある実機検証と例外案は事前承認を得る。
4. 最初は文書１サイトの少数資料と権限の異なる利用者の代表質問で検証する。リストが必要なら対象１リストの代表質問を追加し、登録前後の容量、根拠・鮮度・権限漏えいを確認する。重要経路や費用が未確認の間は本実装を始めない。

サイト全体を見せず固定資料が少数で公開範囲が共通なら、直接アップロードを簡易検証の代替候補にする。サイト URL 方式で文書の検索・根拠提示が不十分な場合に限り、SharePoint ファイル／フォルダー取り込みを容量・権限・費用確認後の代替案として比較する。**意味検索を使えることだけで高精度と決めない。** 既存サイトがない、対象構成の対応・利用権が未確認、またはリストの取り込みをベース条件内で成立させられない場合は採用を保留して代替構成を提案する。共有 URL、環境 ID、顧客固有情報はリポジトリに記載しない。

## Microsoft 公式資料

- [二つの SharePoint オプションと保存先・検索・同期の比較](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-unstructured-data#whats-the-difference-between-the-two-sharepoint-options-in-add-knowledge)
- [ローカルファイルのアップロード](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-file-upload)
- [SharePoint サイトとリストをナレッジとして追加](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-sharepoint#add-sharepoint-lists-as-a-knowledge-source)
- [SharePoint ファイル・フォルダーの取り込み](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-unstructured-data#add-sharepoint-files-and-folders)
- [Dataverse 容量レポートとテーブルの集計](https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage#capacity-page-details)
- [Dataverse テーブルをナレッジに追加](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-dataverse)
- [Copilot Credits の請求レートと No charge の適用条件](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management)
- [Copilot Studio のライセンス・サブスクリプション](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing-subscriptions)
