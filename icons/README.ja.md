# サイドバーのアイコン

> 中国語版を優先します。[中文](README.md) · [English](README.en.md)

ファイル名は `<名前>Template.<拡張子>`。plist では
`icon = <名前>Template;` として参照します。ファイルが無い場合、生成スクリプトは
その `icon` キーを省略します。

アイコンは Naruto 音楽フォント由来で、Copyright (C) YH & Kiyoaki,
2024-2026。著作権者の許可により Apache License 2.0 で本プロジェクトに収録して
います。

13 個あり、すべて `SMuFL Common Glyphs` で使われます。`smuflTemplate` は
`SMuFL Glyphs` とランゲージ項目でも使います。

| ファイル | 用途 | 描く内容 |
|---|---|---|
| `smuflTemplate.svg` | 2 つの分類 + ランゲージ項目 | 五線 + 音符 |
| `staffTemplate.svg` | Staff Structure | 譜表 / 小節線 |
| `notesRestsTemplate.svg` | Notes & Rests | 符頭 + 休符 |
| `clefsTemplate.svg` | Clefs & Octaves | ト音記号 |
| `timeSignaturesTemplate.svg` | Time Signatures | `4/4` |
| `dynamicsTemplate.svg` | Dynamics | `f` / `p` |
| `accidentalsTemplate.svg` | Accidentals | ♯ ♭ ♮ |
| `articulationsTemplate.svg` | Articulations | スタッカート / アクセント |
| `repetitionsTemplate.svg` | Repetitions | 反復記号 |
| `holdsPausesTemplate.svg` | Holds & Pauses | フェルマータ |
| `ornamentsTemplate.svg` | Ornaments & Lines | `tr` / モルデント |
| `techniquesTemplate.svg` | Techniques | 演奏技法 |
| `signsTextsTemplate.svg` | Signs & Texts | テンポ / フィンガリング |

## 仕様

- 16 × 16 pt、`viewBox="0 0 16 16"`。Glyphs は SVG の固有サイズで描画します。
- アルファチャンネルのみ。黒 + 透明背景で、色は無視されます。
- SVG / PDF / PNG（PNG は `@2x` が必要）。

## viewBox が揃っていない場合

```bash
python3 tools/normalize_svg.py --in-place icons/*.svg   # 16x16 に正規化
python3 tools/normalize_svg.py --check icons/*.svg      # 確認のみ
python3 tools/build_all.py
```

## 差し替え後

```bash
python3 tools/build_all.py
./install/build-release.sh
```

⌘Q で Glyphs を終了して再起動し、サイドバーを確認します。
