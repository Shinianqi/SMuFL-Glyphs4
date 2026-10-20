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


インストール先:

```text
~/Library/Application Support/Glyphs 4/
```

### 署名されていないパッケージ

pkg を初めて開くと、macOS が「Apple は検証できませんでした」と表示してブロックします。

1. **完了** をクリックします。
2. **システム設定 → プライバシーとセキュリティ** を開き、**セキュリティ** まで
   スクロールします。
3. 「アプリケーションの許可」の下に表示されるブロックされた pkg の
   **このまま開く** をクリックします。
4. Touch ID またはパスワードで確認します。
5. 続いて表示されるダイアログでも **このまま開く** をクリックします。

一覧に表示されない場合は、pkg をもう一度ダブルクリックしてから設定を
開き直してください。

## アンインストール

対応する `Uninstall.pkg` をダブルクリックします。最後のページに
「卸载完成」（アンインストール完了）と表示されます。その後 Glyphs を再起動します。

## バージョン

1.0.0。
