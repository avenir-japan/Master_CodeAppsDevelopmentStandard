---
name: canvas-app
description: "Canvas App（ローコード）で PDF・添付ファイルを扱う画面を構築し、SharePoint staging + Power Automate 中継で AI Builder / 外部処理に渡す。msapp の取得・編集・import と coauthoring による live 反映の検証済みパターンを提供する。"
category: ui
triggers:
  - "Canvas App"
  - "キャンバスアプリ"
  - "Attachments"
  - "添付コントロール"
  - "PDF添付 Canvas"
  - "SubmitForm"
  - "Defaults"
  - "Edit Form"
  - "SharePoint staging"
  - "msapp"
  - "pac canvas"
  - "pac canvas pack"
  - "pac canvas download"
  - "SourceCode"
  - "pa.yaml"
  - "Studio 貼り付け"
  - "coauthoring"
  - "Canvas UI 崩れ"
---

# Canvas App 開発スキル

Canvas App（ローコード）で **PDF・添付ファイルを扱う画面** を構築し、
**SharePoint staging + Power Automate 中継** で AI Builder / 外部処理へ渡すための検証済みパターン集。
msapp の取得・編集・import、coauthoring による live 反映、Attachments UI 調整まで Canvas 固有の運用をカバーする。

> [!IMPORTANT]
> このスキルは **Canvas App を採用すると決まった後** に使う。
> 採用判断は [architecture スキル](../architecture/SKILL.md) を先に参照し、Code Apps / Canvas Apps / Model-Driven Apps の候補を比較したうえで、**Canvas App で進めることをユーザーに必ず確認する**。
> 顧客要望・保守体制・市民開発者の関与・モバイル要件・既存資産によって Canvas App が適切な場合があるため、AI が独断で UI 方式を確定してはいけない。

> [!NOTE]
> 本スキル内の例はインシデント管理サンプルなど **汎用題材** を題材としています。
> リスト名・フロー名・列名は、あなたのプロジェクトのエンティティに読み替えてください。
> パターン（Attachments + staging + Flow 中継、msapp ZIP 編集等）はそのまま適用できます。

## サブリファレンス（必要に応じて参照）

| リファレンス                                                   | 内容                                                                  |
| -------------------------------------------------------------- | --------------------------------------------------------------------- |
| [設計パターン](references/design-patterns.md)                  | PDF 添付・SharePoint staging・Flow 中継・AI Builder 入力設計          |
| [トラブルシューティング](references/troubleshooting.md)        | PAC CLI 制約・msapp ZIP 編集回避策・Attachments UI 崩れ・compile 運用 |
| [import / deploy runbook](references/import-deploy-runbook.md) | msapp の取得・編集・再封入・import と live 反映、短い確認チェックリスト |

## 反映方式は 2 系統ある

Canvas App の変更反映は、**まず coauthoring live 反映を第一選択** とし、配布や coauthoring 非対応時のみ msapp import を使う。

| 方式 | 向いている場面 | 要点 |
| --- | --- | --- |
| coauthoring live 反映 | 既存アプリをその場で直したい、Copilot から直接反映したい | Designer の coauthoring セッションを開いたまま、同期した `.pa.yaml` を編集して live app に反映する |
| msapp import | 配布物として渡したい、coauthoring を使えない、Designer を開けない | `.msapp` を作って Power Apps ポータルから import する |

> [!TIP]
> 標準運用では **coauthoring live 反映を先に試す**。
> `.msapp` の import は、配布物が必要な場合、または coauthoring セッションを維持できない場合の代替手段として扱う。

> [!IMPORTANT]
> Copilot からの live 反映は **msapp アップロードではない**。
> Power Apps Designer の coauthoring セッションに対して YAML 変更を流し込む方式であり、**ブラウザタブを閉じると反映経路が切れる**。
> ただし、タブを前面に表示し続ける必要はない。開いたまま維持されていればよい。

## 核心方針: 添付・AI 連携は Flow 中継に寄せる

```
★ 最重要原則

Canvas から AI Builder / Copilot Studio / 外部 API を「直接」叩かない。
  → 要求形式・認証差分で不安定になりやすい

代わりに Power Automate を中継にする:
  Canvas（Edit Form + Attachments）
    → SharePoint staging リストに SubmitForm
    → LastSubmit.ID を Flow に渡す
    → Flow 側で添付取得・変換・AI 呼び出し・保存を一元化

利点:
  ✅ Canvas 側のファイル型制約（AddMedia は PDF に不向き）を回避
  ✅ 入力整形・例外処理・ログ・接続差分吸収を Flow に閉じ込める
  ✅ AI Builder / 外部 API への受け渡しを Flow 1 箇所で管理
```

## 前提: 設計フェーズ完了後に実装に入る（必須）

**このスキルでアプリを組む前に、画面構成とデータフロー（Canvas → staging → Flow → 後続処理）を
ユーザーに提示し、承認を得ていること。**

```
① architecture スキルで UI 方式候補を比較し、Canvas App 採用をユーザーに確認
② [設計パターン](references/design-patterns.md) を読み、添付フロー・staging・Flow 中継を設計
③ ユーザーに設計を提示し、「この設計で進めてよいですか？」と承認を得る
④ 承認後、このスキルに従って実装・coauthoring live 反映・必要時のみ import・UI 調整を行う
```

## 最初の相談文テンプレート

Canvas App の具体設計に入る前に、次の形で UI 方式を確認する。

```markdown
Canvas App で進める前に、UI 実装方式を確認させてください。

今回の要件は Canvas App でも実現可能ですが、Code Apps や Model-Driven Apps の方が適する場合もあります。
顧客要望や保守体制で優先したい方式があれば、先に確定したいです。

確認したい点:

- 顧客としては Code Apps / Canvas App / Model-Driven Apps のどれを希望していますか？
- 主な利用者は誰ですか？ 市民開発者や業務部門が保守する想定はありますか？
- 利用人数はどの程度ですか？（少人数 / 部門利用 / 全社利用）
- モバイル利用は重要ですか？
- 既存の Canvas App 資産や流用したい画面はありますか？
- 複雑な UI（カンバン、複雑テーブル、独自ビジュアル）が必要ですか？

現時点の私の推奨:

- 推奨方式: {Code Apps / Canvas App / Model-Driven Apps}
- 理由: {理由}
- 代替案を選ぶ場合の制約: {制約}

この前提で、どの UI 方式で進めるか指定してください。
未確定なら、こちらで比較表を出して一緒に決めます。
```

> [!TIP]
> いきなり Canvas App 前提で詳細設計に入らず、まず **顧客要望・保守者・利用人数・モバイル要件・既存資産・UI 複雑度** の 6 点を揃える。
> この確認を先に行うと、途中で Code Apps や Model-Driven Apps に戻る手戻りを減らせる。

## 開発フローの全体像

```
1. SharePoint staging リストを用意（汎用リスト・添付有効・必須列は最小）
2. Canvas に Edit Form + Attachments を配置し DataSource を staging にする
   - Item は Defaults(<ListName>)
   - 添付がある場合のみ SubmitForm
   - OnSuccess で非表示の後続ロジック / Flow を呼ぶ
3. Power Automate フロー（PowerApps V2 トリガー）を中継として作成
   - staging item ID を受け取り GetItemAttachments / GetAttachmentContent
   - AI Builder（定義済みパラメータのみ）や外部処理へ渡す
4. まず coauthoring で live 反映し、Designer で Save / Publish
5. 配布や coauthoring 非対応時のみ msapp を取得・編集・import（→ import-deploy runbook）
6. Attachments UI 崩れを調整（→ troubleshooting）
7. coauthoring 未接続 compile の限界に注意し、Designer で最終確認
```

## ドキュメント化の指針

Canvas App 開発の成果物は、次の 4 種類を分けて持つと再利用しやすい。

| 種類                    | 置き場所                                     | 内容                                 |
| ----------------------- | -------------------------------------------- | ------------------------------------ |
| 設計パターン            | このスキルの `references/design-patterns.md` | 汎用・案件非依存の構成知識           |
| トラブルシュート        | このスキルの `references/troubleshooting.md` | 汎用・案件非依存の対処法             |
| import / deploy runbook | プロジェクト側の `work/`                     | 環境・app 名・URL など案件固有の手順 |
| UI 調整テンプレート     | プロジェクト側の `work/`                     | 画面ごとの座標・サイズ値             |

> 特定環境の値（appId・studioUrl・リスト ID 等）は **プロジェクト側 runbook に閉じ込め**、
> 汎用知見は本スキルの `references/` に分離する。

## 関連スキル

| スキル                                       | 連携内容                                      |
| -------------------------------------------- | --------------------------------------------- |
| [architecture](../architecture/SKILL.md)     | Canvas App を採用するかの判断                 |
| [power-automate](../power-automate/SKILL.md) | 中継フロー（PowerApps V2 トリガー）の作成     |
| [ai-builder](../ai-builder/SKILL.md)         | Flow から呼び出す AI プロンプトの構築         |
| [dataverse](../dataverse/SKILL.md)           | staging を Dataverse にする場合のテーブル設計 |
