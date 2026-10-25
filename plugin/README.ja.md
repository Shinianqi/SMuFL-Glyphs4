# メタデータ書き出し

> 中国語版を優先します。[中文](README.md) · [English](README.en.md)

Glyphs 4 の現在のプロジェクトから SMuFL のフォントメタデータ JSON を生成します。

## インストール

**A. プラグイン（推奨）**

`release/pkg/SMuFL-Metadata.pkg` をダブルクリックするか、
`release/manual/SMuFL Metadata/SMuFL Metadata.glyphsPlugin` を次にコピーします。

```text
~/Library/Application Support/Glyphs 4/Plugins/
```

pkg は署名されていないため、初回起動時の手順は
[`release/README.ja.md`](../release/README.ja.md) を参照してください。

Glyphs を再起動すると、**Script** メニューに `Export SMuFL Metadata…` が追加されます。

**B. スクリプト**

次の 2 ファイルを `~/Library/Application Support/Glyphs 4/Scripts/` に置きます。

```text
plugin/smufl_metadata_exporter.py
data/generated/smufl_glyphnames.json
```

その後 Option キーを押しながら **Script → Reload Scripts**（⌘⌥⇧Y）を選ぶか、Glyphs を再起動します。

どちらも Glyphs が使う Python に PyObjC が必要です。無い場合は
`plugin/install_pyobjc.command`（またはその中の手動コマンド）を実行し、
⌘Q で終了してから再起動してください。

## 出力

`.glyphs` ファイルと同じ場所に `<フォント名>.json` として書き出します。

| フィールド | 由来 | 既定 |
|---|---|---|
| `fontName` / `fontVersion` | フォント情報（上書き可） | 必須 |
| `designSize` / `sizeRange` | 設定または Glyphs のカスタムパラメータ | 任意 |
| `engravingDefaults` | アウトライン/ノードから計測（29 項目） | 自動 |
| `glyphAdvanceWidths` | `layer.width / (upm/4)` | 有効 |
| `glyphsWithAnchors` | マスター層の SMuFL アンカー | 有効 |
| `glyphBBoxes` | `layer.bounds / (upm/4)` | 有効 |
| `glyphsWithAlternates` | `salt` / `ssNN` / `cvNN` | 有効 |
| `ligatures` | `liga` / `dlig` / `clig` / `rlig` | 有効 |
| `sets` | `ssNN` + `smufl_sets_template.json` | 有効 |
| `optionalGlyphs` | U+F400–U+F8FF | 有効 |

書き込みはアトミックです。失敗しても中途半端なファイルを残さず、`.glyphs`
プロジェクトも変更しません。

## グリフ名

スクリプトはグリフ名を変更しません。Glyphs は通常 Unicode から production name
（`uniE050`）を生成するため、書き出し前に各 SMuFL グリフの Unicode を確認して
ください。グリフ名とコードポイントを一致させる運用の場合は、従来どおり改名して
から書き出してください。

## 設定

設定ファイルやカスタムパラメータがなくても書き出せます。

自動測定値を上書きしたい、マスターを指定したい、別名や手動アンカーを追加したい、
出力の一部を止めたい場合だけ、次の二つを使います。

### Glyphs のカスタムパラメータ

Font Info → Font → Custom Parameters に追加します:

| パラメータ | 値 | 単位 |
|---|---|---|
| `SMuFL Design Size` | 正の整数 1 つ | decipoint（1/720 インチ）。`120` = 12 pt |
| `SMuFL Size Range` | 正の整数 2 つ。`80, 480` または `80 480` | decipoint。`80, 480` = 8–48 pt |

どちらも任意です。ない場合、対応する `designSize` / `sizeRange` は省略されます。

### 設定ファイル

`smufl-config.example.json` を次の名前でコピーします:

```
<プロジェクトファイル名>.smufl-config.json
```

`.glyphs` ファイルの隣に置きます。名前はプロジェクトファイル名から取り、
ファミリー名ではありません:

```
Naruto.glyphs          → Naruto.smufl-config.json
Naruto-Regular.glyphs  → Naruto-Regular.smufl-config.json
```

必要なキーだけ変更します。`null` は「上書きしない」の意味です。
`SMUFL_CONFIG_PATH` で別の場所を指定することもできます。

設定ファイルはすべてのキーを上書きでき、カスタムパラメータではできない部分も扱えます:

| キー | 用途 | 単位 / 例 |
|---|---|---|
| `fontName` | ファミリー名を上書き | `"Naruto"` |
| `fontVersion` | バージョンを上書き | `1.234` |
| `designSize` | 最適サイズを上書き | decipoint、`120` |
| `sizeRange` | サイズ範囲を上書き | `[80, 480]` |
| `master` | 複数マスターから選ぶ | 名前または ID、`"Regular"` |
| `metadataSource` | 既存 JSON をフォールバックに使う | `.glyphs` からの相対パス |
| `engravingDefaults` | 個別の測定値やテキストフォントを上書き | staff space。`textFontFamily` は配列 |
| `setsTemplate` | `ssNN` の type/description を上書き | 例を参照 |
| `glyphNameAliases` | 独自名を SMuFL 名へ対応づける | `{"myFlat": "accidentalFlat"}` |
| `glyphsWithAnchors` | アンカーを追加・上書き | staff space、`[x, y]` |
| `include*` | 出力セクションを止める | `false` で出力しない |
| `_comment` | 自由記述 | 書き出しでは無視 |

`designSize` / `sizeRange` の優先順位:

```
設定ファイル > Glyphs のカスタムパラメータ > metadataSource > 出力しない
```

両方ある場合は設定ファイルが優先です。`null` にするとカスタムパラメータを使います。

## データファイル

| ファイル | 用途 | ライセンス |
|---|---|---|
| `smufl_metadata_exporter.py` | 書き出し本体 | Apache-2.0 |
| `data/generated/smufl_glyphnames.json` | 正規名/コードポイント/説明/classes | Apache-2.0 + SMuFL 表示 |
| `smufl_optional_reference.json` | 任意グリフの説明/classes 参照 | **OFL-1.1** |
| `smufl_sets_template.json` | `ssNN` スタイルセットのテンプレート | **OFL-1.1** |

公式の `glyphnames.json` をそのまま使うこともできます（環境変数
`SMUFL_GLYPHNAMES_PATH`）。ただしその場合 `optionalGlyphs[].classes` は空になります。

## テスト

```bash
cd plugin
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

モックの Glyphs オブジェクトモデルを使う 59 個の単体テストです。Glyphs の
インストールは不要です。実フォントでの確認は `tests/README.md` を参照してください。

## Glyphs でのグリフ名の違い

Glyphs は数字で始まるグリフ名を受け付けないため、データ表では次の名前にしています。

```text
4stringTabClef -> fourStringTabClef
6stringTabClef -> sixStringTabClef
```

書き出し時に SMuFL の正規名へ戻すので、出力 JSON は正規名のままです。
`unicode` / `production` には影響しません。

## ライセンス

書き出し本体は Apache-2.0。プラグインのランチャー
（`bundle/Contents/MacOS/`）は GlyphsSDK 由来で Apache-2.0。参照用 JSON 2 件は
OFL-1.1 なので、著作権表示を消さないでください。詳細はリポジトリの `NOTICE` を参照。
