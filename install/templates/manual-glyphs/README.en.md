# SMuFL Glyphs — manual install

> Chinese is the primary language. [中文](README.md) · [日本語](README.ja.md)

Classification tables (GlyphData, Groups, icons, filters). The plugin lives in
`release/manual/SMuFL Metadata/`.

## Install

1. Quit Glyphs completely (Cmd-Q).
2. Copy `Info` and `Filters` from this folder to:

```text
~/Library/Application Support/Glyphs 4/
```

The result should be:

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

3. Reopen Glyphs.

If you already have your own `GlyphData-*.xml` or `Groups-*.plist`, copy the
files one by one instead of replacing the whole folder.

## Usage

- The sidebar shows `SMuFL Glyphs` and `SMuFL Common Glyphs`.
- The startup window has five presets.
- Glyphs sort by Unicode codepoint.

Anchors must be applied manually: select the glyphs and run
**Glyph > Set Anchors (Cmd-U)**. `Dynamics` get `opticalCenter`; noteheads get
`stemUpSE`, `stemDownNW`, `splitStemUpSE`, `splitStemDownNW`; accidentals get
the `cutOut*` anchors.

## Uninstall

Quit Glyphs and delete:

```text
~/Library/Application Support/Glyphs 4/Info/GlyphData-SMuFL.xml
~/Library/Application Support/Glyphs 4/Info/Groups-SMuFL.plist
~/Library/Application Support/Glyphs 4/Info/Icons/*Template.svg
~/Library/Application Support/Glyphs 4/Filters/CustomFilterSMuFL.plist
```

## Troubleshooting

- **Nothing in the sidebar**: make sure the files are in
  `Application Support/Glyphs 4/Info/`, not `Glyphs 4/Info/Info/`.
- **`Invalid filter in sidebar`**: remove `Filters/CustomFilterSMuFL.plist`.
- **Glyphs reports an error on startup**: remove the files you just copied and
  check that the XML/plist were not altered by an editor.
