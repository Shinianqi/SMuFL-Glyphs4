# Changelog

> 中国語版を優先します。[中文](CHANGELOG.md) · [English](CHANGELOG.en.md)

## 1.1.0 — 2026-10-27

### 書き出し

- `fontVersion` の小数部を 3 桁にゼロ埋め（`1 + 5` → `1.005`）。
- Unicode のない canonical / alias グリフでも bbox と advance width を書き出す。
- `wedgeArmStrokeWidth` を整数に丸めない。
- 手動アンカーの検証で毎回フォント全体を走査しない。
- `uniXXXX` の大文字小文字チェックを修正。

### ドキュメント

- プラグイン README に設定の説明を追加: `SMuFL Design Size` /
  `SMuFL Size Range` の単位・例・優先順位と、設定ファイルのキー一覧。
- グリフ名の説明を追加。Reload Scripts は Option キーを押す旨に修正。
- 設定例のコメントを英語に変更。

### データ

- 上流を `a86fde4e` に更新: Sagittal の説明 3 件の NBSP を通常のスペースに変更。

### ライセンス

- Bravura の OFL 本文を正式な著作権表示に更新。

## 1.0.1 — 2026-10-22

### 分類表

- `SMuFL Common Glyphs` を 916 グリフに調整:
  - `Staff Structure` を Staff Brackets と Staff Dividers に分割;
  - Note Clusters（40）と Extended Stein-Zimmermann Accidentals（13）を削除。
- README の分類順を実際のサイドバー表示（Common が先）に合わせた。

機能的な変更はありません。

## 1.0.0 — 2026-10-20

### 分類表

- SMuFL 1.5（draft）の公式メタデータ（`w3c-cg/smufl`、commit `f9d12b2`）から生成:
  `GlyphData-SMuFL.xml`（2,940 グリフ）と `Groups-SMuFL.plist`。
- サイドバー: `SMuFL Glyphs`（Classes A-Z 85 + Ranges A-Z 132）と
  `SMuFL Common Glyphs`（12 グループ、969 グリフ）。
- `Ornaments & Lines` に Trills、Arpeggios、Glissando、Combining Strokes を収録。
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
