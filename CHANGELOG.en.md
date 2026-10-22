# Changelog

> Chinese is the primary language. [中文](CHANGELOG.md) · [日本語](CHANGELOG.ja.md)

## 1.0.1 — 2026-10-22

### Classification tables

- `SMuFL Common Glyphs` is now 916 glyphs:
  - `Staff Structure` is split into Staff Brackets and Staff Dividers;
  - Note Clusters (40) and Extended Stein-Zimmermann Accidentals (13) are
    removed.
- The README lists the categories in the order the sidebar actually shows
  them (Common first).

No functional changes.

## 1.0.0 — 2026-10-20

### Classification tables

- Generated from the official SMuFL 1.5 (draft) metadata (`w3c-cg/smufl`,
  commit `f9d12b2`): `GlyphData-SMuFL.xml` (2,940 glyphs) and
  `Groups-SMuFL.plist`.
- Sidebar: `SMuFL Glyphs` (Classes A-Z 85 + Ranges A-Z 132) and
  `SMuFL Common Glyphs` (12 groups, 969 glyphs).
- `Ornaments & Lines` contains Trills, Arpeggios, Glissando and Combining
  Strokes.
- Five startup-window presets: `SMuFL Common Glyphs`, `SMuFL Glyphs`, `Clefs`,
  `Time Signatures`, `Notes & Rests`.
- Glyphs sort by Unicode codepoint; the two digit-leading names get a
  Glyphs-safe spelling.
- Three custom filters (Core / Optional / Unicode Music Symbols).
- Group structure lives in `data/layout/legacy.json` (names and range/class
  references only).

### Anchors

- Applied by Cmd-U.
- 1,016 glyphs carry anchors:
  - `data/layout/anchors.glyphs.json`: per-glyph anchors normalized from
    Bravura 1.482 `glyphsWithAnchors` / `glyphBBoxes` (586 glyphs);
  - `data/layout/anchors.json`: per-range fallbacks (Dynamics, noteheads,
    accidentals, multi-segment lines).

### Exporter

- Writes the SMuFL font metadata JSON: `engravingDefaults`,
  `glyphAdvanceWidths`, `glyphsWithAnchors`, `glyphBBoxes`,
  `glyphsWithAlternates`, `ligatures`, `sets`, `optionalGlyphs`.
- Plugin and script share the same export core.

### Release

- `release/pkg/`: four packages — `SMuFL Glyphs`, `SMuFL Metadata` and their
  `Uninstall` counterparts.
- `release/manual/`: manual install files for both components.
- Built with `./install/build-release.sh`.

### Project

- Build, verify and release scripts; 13 icons from the Naruto font.
- Apache-2.0; Bravura reference data is OFL-1.1.
