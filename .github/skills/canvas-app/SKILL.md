---
name: canvas-app
description: "Canvas App の AI 主導編集、Git によるソース管理、single app / package による限定的な受け渡しを整理し、PDF・添付ファイル要件では SharePoint staging + Power Automate 中継パターンまで扱う。"
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

Canvas App の作成・編集・ソース管理・環境移送を整理したうえで、
**PDF・添付ファイルを扱う画面** を **SharePoint staging + Power Automate 中継** で
AI Builder / 外部処理へ渡すための実装パターンまで扱う。

このスキルでは、Canvas App の運用を次の 3 モードに分けて扱う。

| モード               | 主目的               | 標準度     | 向いている作業                         |
| -------------------- | -------------------- | ---------- | -------------------------------------- |
| MCP + coauthoring    | AI 主導の作成・編集  | 第一選択   | 新規作成、既存修正、対話的な試行錯誤   |
| Git Integration      | ソース管理と軽微編集 | チーム標準 | 差分レビュー、履歴管理、軽微な直接修正 |
| single app / package | 限定的な受け渡し     | 例外運用   | 単体バックアップ、簡易移送、配布       |

> [!IMPORTANT]
> このスキルは **Canvas App を採用すると決まった後** に使う。
> 採用判断は [architecture スキル](../architecture/SKILL.md) を先に参照し、Code Apps / Canvas Apps / Model-Driven Apps の候補を比較したうえで、**Canvas App で進めることをユーザーに必ず確認する**。
> 顧客要望・保守体制・市民開発者の関与・モバイル要件・既存資産によって Canvas App が適切な場合があるため、AI が独断で UI 方式を確定してはいけない。

> [!NOTE]
> 本スキル内の例はインシデント管理サンプルなど **汎用題材** を題材としています。
> リスト名・フロー名・列名は、あなたのプロジェクトのエンティティに読み替えてください。
> パターン（Attachments + staging + Flow 中継 など）はそのまま適用できます。

## サブリファレンス（必要に応じて参照）

| リファレンス                                                                           | 内容                                                                        |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [AI codegen workflow](references/ai-codegen-workflow.md)                               | Canvas Apps plugin、MCP、coauthoring を使った AI 主導の作成・編集フロー     |
| [source code and Git integration](references/source-code-and-git-integration.md)       | pa.yaml 構造、Git Integration、軽微編集の境界                               |
| [ALM and import options](references/alm-and-import-options.md)                         | solutions / single app / package の違い、ALM 上の位置づけ                   |
| [coauthoring limitations](references/coauthoring-limitations.md)                       | coauthoring の制約、同時編集、非アクティブ時挙動、注意点                    |
| [data source and connector boundary](references/data-source-and-connector-boundary.md) | 接続追加を Studio 側で行う境界、AI が扱える範囲                             |
| [設計パターン](references/design-patterns.md)                                          | PDF 添付・SharePoint staging・Flow 中継・AI Builder 入力設計                |
| [トラブルシューティング](references/troubleshooting.md)                                | coauthoring / MCP 運用、Attachments UI 崩れ、例外時の非推奨ワークアラウンド |
| [import / deploy runbook](references/import-deploy-runbook.md)                         | single app / package を使う例外運用の runbook と確認チェックリスト          |

## まず押さえること

Canvas App では、**作る方法** と **管理する方法** と **渡す方法** を分けて考える。

1. 日々の AI 編集は **MCP + coauthoring** を使う
2. チームでの履歴管理は **Git Integration** を使う
3. 単体受け渡しや簡易移送だけ **single app / package** を使う

> [!IMPORTANT]
> `single app` や `package` は、Canvas App 開発の中心ではなく **移送手段** として扱う。
> Dataverse 依存や本格的な ALM がある案件では、まず **solutions** を正本として検討する。

## 標準運用は 3 モードで整理する

Canvas App の変更反映や管理方法は、次の 3 モードで使い分ける。

| モード               | 向いている場面                                          | 要点                                                                                                           |
| -------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| MCP + coauthoring    | 既存アプリをその場で直したい、新規 App を AI で作りたい | Designer の coauthoring セッションを開いたまま、`sync_canvas` と `compile_canvas` を使って live app と同期する |
| Git Integration      | チーム開発、レビュー、履歴管理                          | publish 済みの App を Git 上の `pa.yaml` として扱い、軽微な直接編集と差分レビューを行う                        |
| single app / package | 配布物が必要、Studio を開けない、簡易移送したい         | `.msapp` または package を export / import する。ただし ALM の正本にはしない                                   |

> [!TIP]
> 標準運用では **MCP + coauthoring を先に試す**。
> そのうえで **Git Integration を履歴管理の標準** に置き、`single app` や `package` は例外時だけ使う。

> [!IMPORTANT]
> Copilot からの live 反映は **msapp アップロードではない**。
> Power Apps Designer の coauthoring セッションに対して YAML 変更を流し込む方式であり、**ブラウザタブを閉じると反映経路が切れる**。
> ただし、タブを前面に表示し続ける必要はない。開いたまま維持されていればよい。

## MCP + coauthoring を第一選択にする理由

Microsoft Learn の現行フローでは、Canvas App の AI 主導編集は **Canvas Apps plugin + Canvas Authoring MCP + coauthoring** が中心に置かれている。

この方式では次ができる。

- 自然言語で新規 Canvas App を作る
- 既存 App を `sync_canvas` で同期して編集する
- `list_controls`、`describe_control`、`list_data_sources`、`describe_api` で設計前提を確認する
- `compile_canvas` で YAML を検証しながら live app に反映する

前提条件と手順は [AI codegen workflow](references/ai-codegen-workflow.md) を参照する。

## Git Integration は source control の標準

Git Integration は、Canvas App をチームで管理するための **source control モード** として扱う。

- publish 済みの App を Git 上で履歴管理する
- `pa.yaml` の差分をレビューする
- 軽微な修正は repository 側で行える
- 大きな UI 再設計や試行錯誤は MCP + coauthoring 側に寄せる

詳細は [source code and Git integration](references/source-code-and-git-integration.md) を参照する。

## single app / package は限定的な受け渡し

`single app (.msapp)` と `package` は、どちらも **移送手段** ではあるが、位置づけが異なる。

- `single app (.msapp)`: App 単体の保存や簡易受け渡し向け
- `package`: App と一部関連リソースの簡易移送向け

どちらも、本格的な ALM の正本にはしない。
Dataverse 依存、connection reference、flows を含む案件では **solutions を優先** する。

詳細は [ALM and import options](references/alm-and-import-options.md) を参照する。

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
④ 承認後、このスキルに従って実装・MCP + coauthoring・必要時のみ import / package・UI 調整を行う
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
1. どのモードを使うか決める
  - AI 主導編集: MCP + coauthoring
  - source control: Git Integration
  - 簡易移送: single app / package
2. MCP + coauthoring を使う場合は Canvas Apps plugin をセットアップする
  - `.NET 10 SDK` を確認
  - `/configure-canvas-mcp` で接続する
  - coauthoring を有効にした Designer タブを開いたまま維持する
3. PDF / 添付要件がある場合は SharePoint staging リストを用意する
4. Canvas に Edit Form + Attachments を配置し DataSource を staging にする
  - Item は Defaults(<ListName>)
  - 添付がある場合のみ SubmitForm
  - OnSuccess で後続ロジック / Flow を呼ぶ
5. Power Automate フロー（PowerApps V2 トリガー）を中継として作成する
  - staging item ID を受け取り GetItemAttachments / GetAttachmentContent
  - AI Builder（定義済みパラメータのみ）や外部処理へ渡す
6. `sync_canvas` / `compile_canvas` で反映し、Designer で Save / Publish する
7. Git Integration を使う案件では publish 後の `pa.yaml` を履歴管理する
8. single app / package は必要時のみ export / import する
9. Attachments UI 崩れや coauthoring の制約を確認し、Designer で最終確認する
```

## ドキュメント化の指針

Canvas App 開発の成果物は、次の 4 種類を分けて持つと再利用しやすい。

| 種類                    | 置き場所                                                     | 内容                                        |
| ----------------------- | ------------------------------------------------------------ | ------------------------------------------- |
| AI 編集フロー           | このスキルの `references/ai-codegen-workflow.md`             | MCP / coauthoring の汎用手順                |
| source control 指針     | このスキルの `references/source-code-and-git-integration.md` | pa.yaml と Git Integration の汎用知識       |
| ALM / 移送指針          | このスキルの `references/alm-and-import-options.md`          | solutions / single app / package の使い分け |
| 設計パターン            | このスキルの `references/design-patterns.md`                 | 汎用・案件非依存の添付 / Flow 中継構成知識  |
| トラブルシュート        | このスキルの `references/troubleshooting.md`                 | 汎用・案件非依存の対処法                    |
| import / deploy runbook | プロジェクト側の `work/`                                     | 環境・app 名・URL など案件固有の手順        |
| UI 調整テンプレート     | プロジェクト側の `work/`                                     | 画面ごとの座標・サイズ値                    |

> 特定環境の値（appId・studioUrl・リスト ID 等）は **プロジェクト側 runbook に閉じ込め**、
> 汎用知見は本スキルの `references/` に分離する。

## 関連スキル

| スキル                                       | 連携内容                                      |
| -------------------------------------------- | --------------------------------------------- |
| [architecture](../architecture/SKILL.md)     | Canvas App を採用するかの判断                 |
| [power-automate](../power-automate/SKILL.md) | 中継フロー（PowerApps V2 トリガー）の作成     |
| [ai-builder](../ai-builder/SKILL.md)         | Flow から呼び出す AI プロンプトの構築         |
| [dataverse](../dataverse/SKILL.md)           | staging を Dataverse にする場合のテーブル設計 |
