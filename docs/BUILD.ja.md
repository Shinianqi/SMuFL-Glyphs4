# ビルド

> 中国語版を優先します。[中文](BUILD.md) · [English](BUILD.en.md)

Python 3.9+ が必要です（標準ライブラリのみ）。`.pkg` のビルドには macOS が必要です。

## データの生成

```bash
python3 tools/build_all.py
```

| スクリプト | 出力 |
|---|---|
| `build_glyphdata.py` | `data/generated/GlyphData-SMuFL.xml` |
| `build_groups.py` | `data/generated/Groups-SMuFL.plist` |
| `build_glyphnames_snapshot.py` | `data/generated/smufl_glyphnames.json` |

最後に `verify.py` で結果を確認します。

出力は決定的で、生成物はコミット済みです。インストールや利用に Python は不要です。

## SMuFL データの更新

```bash
python3 tools/fetch_upstream.py --ref <tag-or-commit>
python3 tools/build_all.py
git diff --stat data/
```

`fetch_upstream.py` は GitHub contents API を使い、`VERSION.json` と
`SHA256SUMS` も更新します。現在のデータは `gh-pages` 上の 1.5 draft に追従しています。

## インストールとパッケージ

```bash
./install/install.sh              # 開発用インストール
./install/install.sh --uninstall
./install/build-release.sh        # release/ に 4 つの pkg と手動インストール用ファイル
```

## プラグイン

```bash
./plugin/build.sh          # build/SMuFL Metadata.glyphsPlugin
```

バンドルは `plugin/bundle/` の GlyphsSDK 骨組み、書き出し本体、生成済みの
`smufl_glyphnames.json` から構成されます。`build-release.sh` がこれを呼びます。

## テスト

```bash
cd plugin
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

## サイドバーの編集

`data/layout/legacy.json` を編集します。

- グループ: `{"name": ..., "icon": ..., "children": [...]}`
- リーフ: `{"name": ..., "range": "<ranges.json のキー>"}` または
  `{"name": ..., "class": "<classes.json のキー>"}`
- `languages[0].precreate` が起動ウィンドウの項目を定義します。`from` は
  `all` / `category:<名前>` / `basics:<名前>` / `name:<リーフ名>` に対応します。

リーフにグリフ一覧は含まれません。グリフは公式データから取得します。

> `Flags` の名前の末尾にはゼロ幅スペース（U+200B）があります。Glyphs の
> `categories.strings` が `Flags` を「旗」にローカライズするため、この文字で
> 回避してサイドバーには `Flags` と表示させています。編集時に削除しないでください。
