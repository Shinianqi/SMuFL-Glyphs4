# SMuFL Glyphs — 手動インストール

分類表（GlyphData、Groups、アイコン、フィルタ）。プラグインは
`release/manual/SMuFL Metadata/` にあります。

## インストール

1. ⌘Q で Glyphs を完全に終了します。
2. このフォルダの `Info` と `Filters` を次にコピーします。

```text
~/Library/Application Support/Glyphs 4/
```

結果は次のようになります。

```text
~/Library/Application Support/Glyphs 4/
├── Filters/
│   └── CustomFilterSMuFL.plist
└── Info/
    ├── GlyphData-SMuFL.xml
    ├── Groups-SMuFL.plist
    └── Icons/
        └── *Template.svg
```

3. Glyphs を開き直します。

既に独自の `GlyphData-*.xml` や `Groups-*.plist` がある場合は、フォルダごと
上書きせず 1 ファイルずつコピーしてください。

## 使い方

- サイドバーに `SMuFL Glyphs` と `SMuFL Common Glyphs` が表示されます。
- 起動ウィンドウに 5 つのプリセットがあります。
- グリフは Unicode コードポイント順に並びます。

アンカーは手動で適用します。グリフを選択して
**Glyph > Set Anchors（⌘U）** を実行します。`Dynamics` には `opticalCenter`、
音符類には `stemUpSE`、`stemDownNW`、`splitStemUpSE`、`splitStemDownNW`、
変音記号には `cutOut*` が入ります。

## アンインストール

Glyphs を終了して次を削除します。

```text
~/Library/Application Support/Glyphs 4/Info/GlyphData-SMuFL.xml
~/Library/Application Support/Glyphs 4/Info/Groups-SMuFL.plist
~/Library/Application Support/Glyphs 4/Info/Icons/*Template.svg
~/Library/Application Support/Glyphs 4/Filters/CustomFilterSMuFL.plist
```

## トラブルシューティング

- **サイドバーに何も出ない**: ファイルが `Application Support/Glyphs 4/Info/`
  にあるか確認します（`Glyphs 4/Info/Info/` になっていないか）。
- **`Invalid filter in sidebar`**: `Filters/CustomFilterSMuFL.plist` を削除します。
- **起動時にエラー**: コピーしたファイルを削除し、XML/plist がエディタで
  壊れていないか確認します。
