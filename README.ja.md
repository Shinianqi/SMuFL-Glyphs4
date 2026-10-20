# SMuFL for Glyphs 4

> 中国語版が正です。本日本語版は中国語版からの翻訳です。[中文](README.md) · [English](README.en.md)

Glyphs 4 は macOS アプリです。本リポジトリはその SMuFL 分類表とフォントメタデータ書き出しプラグインを提供します。データは SMuFL 1.5（draft）の公式メタデータに基づいています。インストーラは Glyphs 3 のフォルダ構成にも対応します。

## スクリーンショット

起動ウィンドウ（5 つのプリセット）:

![起動ウィンドウ](docs/images/startup.png)

サイドバー（2 つの分類）:

![サイドバー](docs/images/sidebar.png)

## 分類表

| 項目 | 数 |
|---|---|
| グリフ | 2,940 |
| classes | 85 |
| ranges | 132 |
| サイドバー分類 | `SMuFL Glyphs`、`SMuFL Common Glyphs` |
| 起動ウィンドウの項目 | 5 |

```text
SMuFL Glyphs
├── Classes A-Z
└── Ranges A-Z

SMuFL Common Glyphs
├── Staff Structure
├── Clefs & Octaves
├── Notes & Rests
├── Accidentals
├── Time Signatures
├── Repetitions
├── Dynamics
├── Articulations
├── Holds & Pauses
├── Ornaments & Lines
├── Techniques
└── Signs & Texts
```

起動ウィンドウ：`SMuFL Common Glyphs`（969）、`SMuFL Glyphs`（2,940）、
`Clefs`（61）、`Time Signatures`（32）、`Notes & Rests`（212）。
グリフは Unicode コードポイント順に並びます。

### インストール

`release/` の pkg を使います。詳細は [`release/README.md`](release/README.md)。

## 書き出しプラグイン

Glyphs 4 の Script メニューから実行し、SMuFL のフォントメタデータ JSON を出力します。
`.glyphs` ファイルは変更しません。

出力項目：`fontName`、`fontVersion`、`designSize`、`sizeRange`、
`engravingDefaults`、`glyphAdvanceWidths`、`glyphsWithAnchors`、`glyphBBoxes`、
`glyphsWithAlternates`、`ligatures`、`sets`、`optionalGlyphs`。

設定は [`plugin/README.md`](plugin/README.md) を参照してください。

## 再ビルド

```bash
python3 tools/build_all.py
```

Python 標準ライブラリのみ使用します。サイドバー構成は
[`data/layout/legacy.json`](data/layout/legacy.json)、アンカールールは
[`data/layout/anchors.json`](data/layout/anchors.json) にあります。
詳しくは [`docs/BUILD.ja.md`](docs/BUILD.ja.md)。

## ライセンス

Apache-2.0（[`LICENSE`](LICENSE)）。第三者への表示は [`NOTICE`](NOTICE)：
SMuFL（FSA）、GlyphsSDK（Apache-2.0）、Bravura（OFL-1.1、参照 JSON 2 件のみ）。
