# Canvas App import / deploy runbook テンプレート

coauthoring を使って live app に反映する手順を第一選択とし、必要時のみ msapp を取得・編集・再封入・import するためのテンプレート。
**環境固有の値（app 名・appId・studioUrl・リスト ID 等）はプロジェクト側 runbook に転記して使う。**

> [!NOTE]
> このテンプレートは汎用手順のみ。実際の値は各プロジェクトの `work/` 配下の runbook に書く。

## 1. coauthoring live 反映を優先する

標準運用では、まず Power Apps Designer の coauthoring セッションを使って live app に直接反映する。
`.msapp` ベースの作業は、配布物が必要な場合や coauthoring を使えない場合の代替手段とする。

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

## 3. msapp import を使う場合だけ実施する手順

coauthoring を使えない場合や、`.msapp` を配布物として残したい場合だけ、以下を実施する。

### 3A. 取得（pull / download）

```bash
# 名前指定が安全（config の appId/studioUrl が古いことがある）
pac canvas download --name "<AppName>" --file-name current.msapp
```

- 取得した msapp を **配布用の正本候補** として扱い、編集前にコピーを残す。
- `canvas-app.config.json` の `appId` / `studioUrl` が現行 app を指しているか確認する。

### 3B. 編集（msapp = ZIP 直接編集）

`pac canvas pack --layout SourceCode` が FormatException で失敗する場合の回避ルート。

```text
1. current.msapp を ZIP として展開
2. Src/*.pa.yaml を編集（数式・プロパティ）
3. Controls/*.json を編集（座標・サイズ・Visible など見た目に効く値）
4. ZIP として再封入し拡張子を .msapp に戻す
```

> [!WARNING]
> pa.yaml だけでは import 後の見た目に反映されないことがある。
> `Controls/4.json` 等のコントロール定義にも旧値が残っていないか必ず確認する。

## 3. 反映方法を選ぶ

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

## 4. 反映後チェックリスト

- [ ] 中継フローの参照名が **表示名** と一致しているか（`MyFlow` vs `マイフロー`）
- [ ] Power Apps V2 トリガーの引数数が一致しているか（不一致なら Flow 再追加）
- [ ] staging リストの DataSource 接続が解決しているか
- [ ] Attachments の親 DataCard まで含めてサイズが整っているか
- [ ] 添付あり時のみ `SubmitForm` する条件が効いているか
