# SMuFL Metadata — manual install

Font metadata exporter plugin. The classification tables live in
`release/manual/SMuFL Glyphs/`.

## Install

1. Quit Glyphs completely (Cmd-Q).
2. Copy `SMuFL Metadata.glyphsPlugin` to:

```text
~/Library/Application Support/Glyphs 4/Plugins/
```

3. Reopen Glyphs.

**Script > Export SMuFL Metadata…** appears in the menu.

## Usage

1. Open a `.glyphs` project.
2. Run **Script > Export SMuFL Metadata…**.
3. Choose where to save; the default is `<font name>.json` next to the project.

The output contains SMuFL `engravingDefaults`, `glyphAdvanceWidths`,
`glyphsWithAnchors`, `glyphBBoxes`, `glyphsWithAlternates`, `ligatures`,
`sets`, `optionalGlyphs`. The `.glyphs` project is never modified.

### Configuration

Copy `smufl-config.example.json` to `<font file name>.smufl-config.json`
next to the project and edit what you need. Every key is optional.

### Script version instead

Put `smufl_metadata_exporter.py` and `smufl_glyphnames.json` in:

```text
~/Library/Application Support/Glyphs 4/Scripts/
```

Then **Script > Reload Scripts**.

## Uninstall

Quit Glyphs and delete:

```text
~/Library/Application Support/Glyphs 4/Plugins/SMuFL Metadata.glyphsPlugin
```

## Requirements

The plugin runs in Glyphs' own Python and needs PyObjC. If it is missing, run
`install_pyobjc.command` or the manual command inside it, then quit Glyphs
(Cmd-Q) and reopen.
