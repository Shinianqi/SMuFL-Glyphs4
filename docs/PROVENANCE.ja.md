# ファイルの出所

> 中国語版を優先します。[中文](PROVENANCE.md) · [English](PROVENANCE.en.md)

| パス | 出所 |
|---|---|
| `data/upstream/*.json` | `w3c-cg/smufl` の `metadata/`、commit `f9d12b2` |
| `data/layout/legacy.json` | グループ構造（名前 + range/class 参照） |
| `data/layout/anchors.json` | range 単位のアンカーのフォールバック |
| `data/layout/anchors.glyphs.json` | Bravura の `glyphsWithAnchors` / `glyphBBoxes` から正規化したグリフ別アンカー |
| `data/generated/*` | `tools/` が生成 |
| `tools/*`、`install/*`、`templates/*` | 本プロジェクト |
| `icons/*` | Naruto 音楽フォント（Copyright (C) YH & Kiyoaki, 2024-2026）、著作権者の許可により Apache-2.0 で使用 |
| `plugin/smufl_metadata_exporter.py`、`plugin/tests/*` | 本プロジェクト |
| `plugin/bundle/Contents/MacOS/{main.py,plugin}` | GlyphsSDK テンプレート |
| `plugin/smufl_optional_reference.json`、`plugin/smufl_sets_template.json`、`data/layout/anchors.glyphs.json` | Bravura `redist/Bravura.json` |
| `data/third-party/bravura/LICENSE-OFL-1.1.txt` | SIL 公式テキスト |

上流スナップショットは `shasum -a 256 -c data/upstream/SHA256SUMS` で検証できます。
