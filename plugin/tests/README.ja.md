# テスト

> 中国語版が正です。[中文](README.md) · [English](README.en.md)

## 1. 単体テスト（Glyphs のインストール不要）

```bash
cd ..
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

テストは Glyphs 4 のオブジェクトモデルの小さなモック
（`font.masters`、`glyph.layerForId_()`、`layer.anchors`、`anchor.position`、
`layer.bounds`、`layer.width`、`font.features` など）を注入します。
PyObjC も Glyphs も不要です。

`SMUFL_EXPORTER_NO_MAIN=1` は、インポート時に Glyphs のメニュー項目を
実行しないようにするためのものです。

現在 **57 個のテスト**があり、次をカバーしています。

- staff space の換算（UPM 1000 / 2048）
- 正規名、別名、Unicode フォールバック、推測しないこと
- 複数マスターの扱い
- 任意グリフ、classes、description
- `salt` / `ssNN` 代替字形、`ssNN` スタイルセット、`liga` リガチャ
- `engravingDefaults` / `designSize` / `sizeRange` と `metadataSource`
- BBox / advance width の有効・無効
- 新フィールドの検証、NaN、重複、未知のキー
- アトミック書き込み、再実行、失敗時に上書きしないこと
- Script メニュー項目のシミュレーション

## 2. 実フォントでの任意のヘッドレス実行（Glyphs 4 + PyObjC）

```bash
python3 -m venv .venv
.venv/bin/pip install pyobjc-framework-Cocoa

.venv/bin/python tests/headless_glyphs4.py \
  "/path/to/YourFont.glyphs" \
  /tmp/YourFont.json \
  --report /tmp/YourFont_report.txt
```

このツールは `GSApplication`（Glyphs の実行ファイル側にあり、フレームワークには
含まれない）だけをスタブにし、`GlyphsApp` をインポートできるようにします。
`GSFont`、`GSGlyph`、`GSLayer`、`GSAnchor`、`layer.bounds` などは GlyphsCore 4.2
の実クラスです。フォントは読み取り専用で開き、保存はしません。

このツールは開発・検証用です。通常の Glyphs スクリプトでは PyObjC を別途
インストールする必要はありません。Glyphs 内蔵の Python が AppKit を提供します。

## 3. サンプル

サンプルフォントは同梱していません（`Naruto_SMuFL.glyphs` はこのリポジトリの
対象外です）。確認する場合は、自分のプロジェクトで上記のヘッドレスコマンドを
実行してください。
