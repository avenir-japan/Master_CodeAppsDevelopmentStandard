# Canvas App import / deploy runbook テンプレート

Canvas App の移送手段を整理したうえで、**標準は MCP + coauthoring**、**例外時のみ single app / package** を使うための runbook。
**環境固有の値（app 名・appId・studioUrl・リスト ID 等）はプロジェクト側 runbook に転記して使う。**

> [!NOTE]
> このテンプレートは汎用手順のみ。実際の値は各プロジェクトの `work/` 配下の runbook に書く。

> [!IMPORTANT]
> 本格的な ALM が必要な案件では、まず **solutions** を正本として扱う。
> この文書は single app / package を完全に否定するものではないが、**開発の中心手段として推奨するものでもない**。

## 1. 先に反映モードを決める

| モード               | 使いどころ           | この runbook での扱い |
| -------------------- | -------------------- | --------------------- |
| MCP + coauthoring    | 日々の作成・編集     | 第一選択              |
| Git Integration      | ソース管理・レビュー | 別文書を正本とする    |
| single app / package | 単体保存・簡易移送   | 例外手段              |

反映や編集の標準運用では、まず **Power Apps Designer の coauthoring セッション** を使って live app に反映する。
配布物が必要な場合や、Studio / coauthoring を使えない場合だけ single app / package を検討する。

詳しい前提整理は [ALM and import options](alm-and-import-options.md) を参照する。

手早く確認したい場合は、先に [coauthoring live 反映チェックリスト](coauthoring-checklist.md) を参照する。

## 2. coauthoring live 反映（第一選択）

`.msapp` を upload する代わりに、Power Apps Designer の coauthoring セッションに対して同期した `.pa.yaml` の変更を反映する。

```text
1. Power Apps Designer で対象 app を開く
2. Settings → Updates → Coauthoring を有効にする
3. そのブラウザタブを開いたままにする
4. Copilot / MCP で app に connect する
5. sync で server state を .pa.yaml として取得する
6. .pa.yaml を編集する
7. compile して live app に反映する
8. Designer 上で見た目と動作を確認する
9. Save、必要なら Publish を実行する
```

> [!IMPORTANT]
> この方式は **タブを前面表示し続ける必要はない** が、**閉じてはいけない**。
> タブを閉じる、サインアウトする、セッションが失効する、といった状態になると coauthoring 経路が切れ、再度 connect し直す必要がある。

> [!NOTE]
> compile は名前上は検証に見えるが、coauthoring セッションが有効な場合は live app への反映経路としても使える。
> ただし最終的な保存は Designer 側の Save を正本と考える。

## 3. single app / package を使う場合だけ実施する手順

coauthoring を使えない場合や、`.msapp` を配布物として残したい場合だけ、以下を実施する。

> [!WARNING]
> package は **export した package をそのまま import する運用** が前提であり、
> 途中で package 自体を書き換える運用は公式サポートの対象外として扱う。

### 3A. 取得（pull / download）

```bash
# 名前指定が安全（config の appId/studioUrl が古いことがある）
pac canvas download --name "<AppName>" --file-name current.msapp
```

- 取得した msapp を **配布用の正本候補** として扱い、編集前にコピーを残す。
- `canvas-app.config.json` の `appId` / `studioUrl` が現行 app を指しているか確認する。

### 3B. 編集（非推奨ワークアラウンド）

Microsoft Learn の整理では、**source control の対象は `Src/*.pa.yaml` のみ** であり、JSON は安定ソースとして扱わない。
そのため、msapp の中身を直接編集する運用は **非推奨ワークアラウンド** として扱う。

また、`pac canvas pack` / `unpack` は deprecated であり、標準運用には置かない。

それでも回避が必要な場合だけ、次を実施する。

```text
1. current.msapp を ZIP として展開
2. Src/*.pa.yaml を確認・編集する
3. ZIP として再封入し拡張子を .msapp に戻す
```

> [!WARNING]
> `Controls/*.json` を source code として維持する運用は推奨しない。
> どうしても UI 反映差異の切り分けで確認する場合でも、**標準運用ではなく最終手段** として扱う。

## 4. 反映方法を選ぶ

PAC CLI の `pac canvas` には、2026-06 時点で **既存 Canvas App に `.msapp` を upload / update するコマンドはない**。

### 3C. msapp import（代替手段）

Power Apps ポータルで次を実行する。

```text
1. Apps 一覧を開く
2. Import app を選ぶ
3. From file を選ぶ
4. current.msapp を指定する
5. import 完了後に Designer を開く
```

- `.msapp` を配布物として渡したい場合はこの方式を使う。
- import 後は **Designer を開いて最終確認** する。
- Attachments など UI 崩れが出たら [troubleshooting](troubleshooting.md) のチェックリストで調整する。

### 3D. package import（簡易移送）

package を使う場合は、Power Apps ポータルの Export Package / Import canvas app を使う。

- package は **ALM 用の正本** として扱わない
- Dataverse 依存、connection reference、flows を含む案件では solutions を優先する
- import 後に connection の再選択や flow の再関連付けが必要になることがある
- update import の場合、import 後に publish が必要になる

## 5. 反映後チェックリスト

- [ ] 中継フローの参照名が **表示名** と一致しているか（`MyFlow` vs `マイフロー`）
- [ ] Power Apps V2 トリガーの引数数が一致しているか（不一致なら Flow 再追加）
- [ ] staging リストの DataSource 接続が解決しているか
- [ ] Attachments の親 DataCard まで含めてサイズが整っているか
- [ ] 添付あり時のみ `SubmitForm` する条件が効いているか
