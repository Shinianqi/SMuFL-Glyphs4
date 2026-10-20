# アンカー

> 中国語版を優先します。[中文](ANCHORS.md) · [English](ANCHORS.en.md)

`GlyphData` の `anchors` 属性は位置付きのアンカーをサポートします。

```xml
<glyph name="ogonek" anchors="ogonek@maxX;baseline" .../>
```

書式は `名前@x式;y式` で、カンマ区切りで複数指定できます。変数:

| 変数 | 意味 |
|---|---|
| `minX` / `maxX` / `width` / `centerX` | 水平 |
| `minY` / `maxY` / `height` / `centerY` | 垂直 |
| `baseline` / `ascender` / `descender` / `xHeight` / `capHeight` | 垂直メトリクス |

## 使い方

![アンカーの適用](images/anchors.gif)

Glyphs はグリフ作成時にアンカーを書き込みません。**Glyph > Set Anchors（⌘U）**
を実行したときに適用されます。不要な場合は ⌘U を押さなければグリフは空のままです。

## データ

| ファイル | 内容 |
|---|---|
| `data/layout/anchors.glyphs.json` | グリフごとのアンカー。Bravura 1.482 の `glyphsWithAnchors` と `glyphBBoxes` を式に正規化。586 グリフ |
| `data/layout/anchors.json` | range 単位のフォールバック。Dynamics、音符類、変音記号、Multi-segment lines |

グリフごとのデータが優先され、無い場合だけ range ルールを使います。現在 1,016
グリフにアンカーがあり、`stemUpSE`、`stemDownNW`、`splitStem*`、`cutOut*`、
`noteheadOrigin`、`opticalCenter`、`repeatOffset`、`graceNoteSlash*` などを
カバーしています。

座標は Bravura の staff space 値を各グリフのバウンディングボックスに対して
`minX/centerX/maxX` と `minY/centerY/maxY/baseline` に量子化した近似値です。
必要に応じて手で調整してください。

## 変更

- 個別のグリフ: `anchors.glyphs.json` の `glyphs` の項目を編集。
- range 単位: `anchors.json` の `rules` を編集。`ranges` は
  `data/upstream/ranges.json` のキーを使います。

```bash
python3 tools/build_all.py
```
