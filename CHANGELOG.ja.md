# Changelog

> 中国語版を優先します。[中文](CHANGELOG.md) · [English](CHANGELOG.en.md)

## 1.0.0 — 2026-10-20

### 分類表

- SMuFL 1.5（draft）の公式メタデータ（`w3c-cg/smufl`、commit `f9d12b2`）から生成:
  `GlyphData-SMuFL.xml`（2,940 グリフ）と `Groups-SMuFL.plist`。
- サイドバー: `SMuFL Glyphs`（Classes A-Z 85 + Ranges A-Z 132）と
  `SMuFL Common Glyphs`（12 グループ、916 グリフ）。
- `Ornaments & Lines` に Trills、Arpeggios、Glissando、Combining Strokes を収録。
- `Staff Structure` を Staff Brackets と Staff Dividers に分割。Note Clusters と
  Extended Stein-Zimmermann Accidentals を削除。
- 起動ウィンドウの 5 項目: `SMuFL Common Glyphs`、`SMuFL Glyphs`、`Clefs`、
  `Time Signatures`、`Notes & Rests`。
- グリフは Unicode コードポイント順。数字で始まる 2 つの名前は Glyphs が
  受け付ける綴りに変更。
- カスタムフィルタ 3 つ（Core / Optional / Unicode Music Symbols）。
- グループ構造は `data/layout/legacy.json`（名前と range/class 参照のみ）。

### アンカー

- ⌘U で適用。
- 1,016 グリフにアンカー:
  - `data/layout/anchors.glyphs.json`: Bravura 1.482 の `glyphsWithAnchors` /
    `glyphBBoxes` から正規化したグリフ別アンカー（586 グリフ）
  - `data/layout/anchors.json`: range 単位のフォールバック（Dynamics、音符類、
    変音記号、マルチセグメント線）

### 書き出し

- SMuFL フォントメタデータ JSON を出力: `engravingDefaults`、
  `glyphAdvanceWidths`、`glyphsWithAnchors`、`glyphBBoxes`、
  `glyphsWithAlternates`、`ligatures`、`sets`、`optionalGlyphs`。
- プラグイン版とスクリプト版は同じ書き出しコアを共有。

### リリース

- `release/pkg/`: `SMuFL Glyphs`、`SMuFL Metadata` とそれぞれの `Uninstall` の
  4 つの pkg。
- `release/manual/`: 両コンポーネントの手動インストール用ファイル。
- `./install/build-release.sh` で生成。

### プロジェクト

- 生成・検証・リリース用スクリプト、Naruto フォント由来の 13 個のアイコン。
- Apache-2.0。Bravura 参照データは OFL-1.1。
