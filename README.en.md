# SMuFL for Glyphs 4

> Chinese is the primary language; this version is a translation. [中文](README.md) · [日本語](README.ja.md)

Glyphs 4 is a macOS app. This repository provides SMuFL classification tables and a font metadata exporter for it; data comes from the official SMuFL 1.5 (draft) metadata. The installer also covers the Glyphs 3 folder layout.

## Screenshots

Startup window with the five presets:

![Startup window](docs/images/startup.png)

Sidebar with both categories:

![Sidebar](docs/images/sidebar.png)

## Classification tables

| Item | Count |
|---|---|
| Glyphs | 2,940 |
| Classes | 85 |
| Ranges | 132 |
| Sidebar categories | `SMuFL Glyphs`, `SMuFL Common Glyphs` |
| Startup-window presets | 5 |

```text
SMuFL Glyphs
├── Classes A-Z
└── Ranges A-Z

SMuFL Common Glyphs
├── Staff Structure
├── Clefs & Octaves
├── Notes & Rests
├── Accidentals
├── Time Signatures
├── Repetitions
├── Dynamics
├── Articulations
├── Holds & Pauses
├── Ornaments & Lines
├── Techniques
└── Signs & Texts
```

Presets: `SMuFL Common Glyphs` (969), `SMuFL Glyphs` (2,940), `Clefs` (61),
`Time Signatures` (32), `Notes & Rests` (212). Glyphs sort by codepoint.

Anchors: run **Glyph > Set Anchors (Cmd-U)** to add `opticalCenter` (dynamics)
and `stemUpSE` / `stemDownNW` / split stem anchors (noteheads). See
[`docs/ANCHORS.md`](docs/ANCHORS.md).

### Install

Use the packages in `release/pkg/`:

| Package | Purpose |
|---|---|
| `SMuFL Glyphs.pkg` | Install the classification tables |
| `SMuFL Glyphs Uninstall.pkg` | Remove them |
| `SMuFL Metadata.pkg` | Install the exporter plugin |
| `SMuFL Metadata Uninstall.pkg` | Remove it |

Quit Glyphs completely (Cmd-Q) and reopen. Manual install and details:
[`release/README.md`](release/README.md).

## Exporter

Runs from the Glyphs 4 Script menu and writes the SMuFL font metadata JSON:
`fontName`, `fontVersion`, `designSize`, `sizeRange`, `engravingDefaults`,
`glyphAdvanceWidths`, `glyphsWithAnchors`, `glyphBBoxes`,
`glyphsWithAlternates`, `ligatures`, `sets`, `optionalGlyphs`. It does not
modify the `.glyphs` project.

Install with `release/pkg/SMuFL Metadata.pkg`, or copy
`release/manual/SMuFL Metadata/SMuFL Metadata.glyphsPlugin` into
`~/Library/Application Support/Glyphs 4/Plugins/`.
See [`plugin/README.md`](plugin/README.md).

## Rebuild

```bash
python3 tools/build_all.py
./install/build-release.sh
```

Standard library only. Sidebar structure lives in
[`data/layout/legacy.json`](data/layout/legacy.json); anchor rules in
[`data/layout/anchors.json`](data/layout/anchors.json). See
[`docs/BUILD.en.md`](docs/BUILD.en.md).

## License

Apache-2.0, see [`LICENSE`](LICENSE). Third-party notices in [`NOTICE`](NOTICE):
SMuFL (FSA), GlyphsSDK (Apache-2.0), Bravura reference data (OFL-1.1), Naruto
icons (© YH & Kiyoaki).

## Credits

[SMuFL](https://www.w3.org/community/music-notation/),
[GlyphsSDK](https://github.com/schriftgestalt/GlyphsSDK),
[Bravura](https://github.com/steinbergmedia/bravura), Naruto music font
(sidebar icons).
