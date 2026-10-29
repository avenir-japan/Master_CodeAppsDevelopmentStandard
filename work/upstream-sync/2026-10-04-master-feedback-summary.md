# 2026-10-04 マスターへの反映内容

本日マスターへ戻した方針・手順の索引。UI 選定だけでなく、要件整理、設計ゲート、ライセンス、エージェント・フローの検証と納品までを対象とする。**このメモは実装や製品仕様の正本ではない。** 案件の確定した開発入力を優先し、詳細はリンク先のスキル・標準で確認する。ここにある既定値を案件の確定要件へ無条件に適用しない。

## 横断方針

- 既定の提案範囲は PoC / MVP。目的、検証仮説、成功条件、対象・対象外、本番化時に判断する事項を明示し、PoC / MVP の成功を本番品質・本番運用の保証と混同しない。本番向けの複雑さを自動追加しない。
- まず Teams / Microsoft 365 Copilot を入口として検討する。画面 UI が本当に必要なら Canvas App を基本案にし、要件実現が難しければ Code Apps / Model-Driven Apps も代替候補として実現性・ライセンス・費用を示す。採否はユーザー承認後に確定する。
- 利用者と実行主体のライセンスを別々に確認し、原則は既定ベースライセンス内かつ Copilot Credits 非消費。非消費はチャネル、認証利用者、トリガー、実行主体、機能の適用条件で判定し、未確認をゼロと扱わない。追加費用や消費が避けられない場合は代替案を先に検討し、例外は条件・費用影響を示して明示承認を得る。
- 全 Power Platform 案件で設計承認・本実装前に、採用機能・アクションと重要な入出力経路を想定最大規模を含めて整理し、最新の Microsoft 公式根拠、制限、権限、ライセンスと照合する。公式情報だけでは重要経路の可否を判断できない場合は最小構成で実機検証する。技術・ライセンス・Credits に未確認や不適合が残る重要経路は通常案として通過させず、代替構成を検討する。構成・規模・条件が変われば影響箇所を再判定する。
- ソリューション管理は継続するが、Dataverse カスタムテーブルは初期化の必須工程ではない。採用した場合だけ設計・作成する。

正本: [standard](../../.github/skills/standard/SKILL.md)、[architecture](../../.github/skills/architecture/SKILL.md)、[UI・構成パターン](../../.github/skills/architecture/references/design-patterns.md)、[ライセンス判定](../../.github/skills/standard/references/license-requirements.md)、[Phase 0 と開発標準](../../.github/skills/standard/references/power-platform-development-standard.md)、[スキルカタログ](../../.github/skills/README.md)。

## 要件・仕様書の引き渡し

- 案件固有の開発入力を先に読み、SPEC.md または分割時の業務要件を開発段階・目的・範囲の正本とする。原資料、変換途中の staging、実装メモと確定要件を区別し、README から正本へ辿れるようにする。
- 開発段階、PoC / MVP の仮説・成功条件・対象外、重要経路の入力形式・最大規模・利用条件を確認する。欠けた依存資料や競合する正本候補は、判断への影響と確認先を未決事項にし、未確定内容を推測で補わない。
- 資料の出所・確定状況・矛盾と変換結果を記録する。個別ファイルの Markdown 化や staging への配置だけを、統合された要件定義書一式の完成とは扱わない。PoC / MVP の検証範囲と未検証範囲を区別して引き渡す。

正本: [要件確認](../../.github/skills/spec-builder/references/requirements-discovery.md)、[仕様統合](../../.github/skills/spec-builder/SKILL.md)、[変換ガイド](../../.github/skills/spec-builder/references/conversion-guide.md)、[変換スクリプト](../../.github/skills/spec-builder/scripts/convert_documents.py)、[資料の Markdown 化](../../.github/skills/spec-to-markdown/SKILL.md)。

## エージェントの評価・納品

- 構造化 JSON は Instructions の保存・読み戻し、配列要素を含む契約適合、入力の確定メタデータとの一致を別々に確認する。処理成功・構造適合と内容の正確さも分け、固定した回帰ケースを複数回実行して変動を記録する。重要な業務事実は元の入力と人が照合し、根拠が曖昧なものを Instructions だけで確定しない。
- モデル比較は入力・Instructions・出力契約・ツール・採点基準をそろえ、条件とケース別結果を記録する。特定モデルや一律の合格点は固定しない。
- マネージドソリューションの納品では ZIP 内設定、インポート、必要な保存、コンポーネントの公開、チャネルからの稼働、関連フローとエンドツーエンドの成功を独立に確認する。チャネルの状態は ZIP の `channels` や公開状態だけから推定しない。新規・更新インポートの結果も混同しない。
- GPT Instructions に raw JSON 例を加えた際の式解釈エラーは限定的なトラブルシュート事例であり、raw JSON が常に失敗するという製品仕様として扱わない。

正本: [Copilot Studio](../../.github/skills/copilot-studio/SKILL.md)、[マネージド納品の制約](../../.github/skills/copilot-studio/references/managed-solution-constraints.md)、[トラブルシュート](../../.github/skills/copilot-studio/references/troubleshooting.md)。

## フローと工程の報告

- PoC / MVP のフローは目的と検証に必要なアクションに絞る。ただし正しさ・必要な検証を犠牲にして削らず、本番向けの追加は理由とともに案件判断する。
- Microsoft 365 Copilot Chat に返すクリック可能なリンクは、検証したケースでは成功応答の表示用 `message` に Markdown リンクが必要だった。機械可読な URL 出力は別に保ち、失敗応答と共有リンク作成後に返す順序を回帰確認する。全チャネルへの一般化はしない。
- エージェント連携フローのトリガー定義、環境での種別、実際の呼び出し元は個別に記録する。帳票の固定欄や確認済みの書式を入力契約の変更に便乗して変えず、入力から確かめられない値を推測しない。
- 複数工程の依頼は仕様・変換処理・フロー接続・関連文書それぞれを「完了」「未着手」「要確認」で報告する。一部の成果物を全工程の完了、未接続の処理を稼働中のフローと表現しない。

正本: [Power Automate](../../.github/skills/power-automate/SKILL.md)、[コードファーストのフロー作成](../../.github/skills/power-automate/references/code-first-flow-authoring.md)。

## 案件ごとに残す確認結果

案件の仕様・設計側に、要件の正本と未決事項、PoC / MVP の成功条件・対象外、重要経路の公式根拠 URL・確認日・適用条件、想定規模との照合、必要な実機検証、利用者と実行主体のライセンス判定、Credits 判定、代替案・承認を記録する。エージェントとフローの評価・納品は対象バージョン、日時、ケース別結果と証跡を分離して残す。このメモ自体は、個別案件の適合判定や実機検証の証拠ではない。
