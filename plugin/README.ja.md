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

その後 **Script → Reload Scripts**。

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

## 設定

`smufl-config.example.json` を `.glyphs` ファイルの隣に
`<フォントファイル名>.smufl-config.json`（例: `MyFont.smufl-config.json`）
としてコピーし、必要な項目だけ上書きします。すべてのキーは任意です。

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

モックの Glyphs オブジェクトモデルを使う 57 個の単体テストです。Glyphs の
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
