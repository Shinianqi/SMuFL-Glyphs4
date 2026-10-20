# リリースパッケージ

> 中国語版を優先します。[中文](README.md) · [English](README.en.md)

2 つのコンポーネントそれぞれのインストール/アンインストール pkg と、
手動インストール用のファイルです。

| ファイル | 用途 |
|---|---|
| `pkg/SMuFL-Glyphs.pkg` | 分類表（GlyphData、Groups、アイコン、フィルタ）をインストール |
| `pkg/SMuFL-Glyphs-Uninstall.pkg` | 分類表を削除 |
| `pkg/SMuFL-Metadata.pkg` | メタデータ書き出しプラグインをインストール |
| `pkg/SMuFL-Metadata-Uninstall.pkg` | プラグインを削除 |

手動インストール:

| フォルダ | 用途 |
|---|---|
| `manual/SMuFL Glyphs/` | `Info/` と `Filters/` を Glyphs の Application Support にコピー |
| `manual/SMuFL Metadata/` | `SMuFL Metadata.glyphsPlugin` を `Plugins/` にコピー |

## インストール

2 つのコンポーネントは独立しています。どちらだけでも構いません。

1. `SMuFL-Glyphs.pkg` をダブルクリックして手順に従います。
2. `SMuFL-Metadata.pkg` をダブルクリックして手順に従います。
3. ⌘Q で Glyphs を完全に終了し、再起動します。

パッケージは署名されていません。初回起動時に Gatekeeper に止められた場合は、
右クリック →「開く」を選びます。

インストール先:

```text
~/Library/Application Support/Glyphs 4/
```

## アンインストール

対応する `Uninstall.pkg` をダブルクリックします。最後のページに
「卸载完成」（アンインストール完了）と表示されます。その後 Glyphs を再起動します。

## バージョン

1.0.0。
