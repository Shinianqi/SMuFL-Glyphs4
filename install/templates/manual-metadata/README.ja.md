# SMuFL Metadata — 手動インストール

> 中国語版を優先します。[中文](README.md) · [English](README.en.md)

フォントメタデータ書き出しプラグイン。分類表は
`release/manual/SMuFL Glyphs/` にあります。

## インストール

1. ⌘Q で Glyphs を完全に終了します。
2. `SMuFL Metadata.glyphsPlugin` を次にコピーします。

```text
~/Library/Application Support/Glyphs 4/Plugins/
```

3. Glyphs を開き直します。

**Script** メニューに `Export SMuFL Metadata…` が追加されます。

## 使い方

1. `.glyphs` プロジェクトを開きます。
2. **Script > Export SMuFL Metadata…** を実行します。
3. 保存先を選びます。既定はプロジェクトと同じ場所の `<フォント名>.json` です。

出力には SMuFL の `engravingDefaults`、`glyphAdvanceWidths`、
`glyphsWithAnchors`、`glyphBBoxes`、`glyphsWithAlternates`、`ligatures`、
`sets`、`optionalGlyphs` が含まれます。`.glyphs` プロジェクトは変更しません。

### 設定

`smufl-config.example.json` をプロジェクトの隣に
`<プロジェクトファイル名>.smufl-config.json` としてコピーし、必要な項目だけ
編集します。すべてのキーは任意です。

### スクリプト版を使う場合

`smufl_metadata_exporter.py` と `smufl_glyphnames.json` を次に置きます。

```text
~/Library/Application Support/Glyphs 4/Scripts/
```

その後 Option キーを押しながら **Script → Reload Scripts**（⌘⌥⇧Y）を選ぶか、Glyphs を再起動します。

## アンインストール

Glyphs を終了して次を削除します。

```text
~/Library/Application Support/Glyphs 4/Plugins/SMuFL Metadata.glyphsPlugin
```

## 必要なもの

プラグインは Glyphs 内蔵の Python で動作し、PyObjC が必要です。無い場合は
`install_pyobjc.command`、またはその中の手動コマンドを実行し、⌘Q で Glyphs を
終了してから再起動してください。
