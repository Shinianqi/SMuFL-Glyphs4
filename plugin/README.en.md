# Metadata exporter

> Chinese is the primary language. [中文](README.md) · [日本語](README.ja.md)

Generates the SMuFL font metadata JSON from the current Glyphs 4 project.

## Installation

**A. Plugin (recommended)**

Double-click `release/pkg/SMuFL-Metadata.pkg`, or copy
`release/manual/SMuFL Metadata/SMuFL Metadata.glyphsPlugin` to:

```text
~/Library/Application Support/Glyphs 4/Plugins/
```

The package is unsigned; the first-launch steps are in
[`release/README.en.md`](../release/README.en.md).

Restart Glyphs. **Script > Export SMuFL Metadata…** appears in the menu.

**B. Script**

Put these two files in `~/Library/Application Support/Glyphs 4/Scripts/`:

```text
plugin/smufl_metadata_exporter.py
data/generated/smufl_glyphnames.json
```

Then hold Option and choose **Script → Reload Scripts** (Cmd-Opt-Shift-Y), or restart Glyphs.

Both need PyObjC in the Python that Glyphs uses. If it is missing, run
`plugin/install_pyobjc.command` (or the manual command in that file), then
quit Glyphs with Cmd-Q and reopen.

## Output

Written next to the `.glyphs` file as `<font name>.json`.

| Field | Source | Default |
|---|---|---|
| `fontName` / `fontVersion` | font info, overridable | required |
| `designSize` / `sizeRange` | config or Glyphs custom parameters | optional |
| `engravingDefaults` | measured from outlines/nodes (29 values) | auto |
| `glyphAdvanceWidths` | `layer.width / (upm/4)` | on |
| `glyphsWithAnchors` | SMuFL anchors of the master layer | on |
| `glyphBBoxes` | `layer.bounds / (upm/4)` | on |
| `glyphsWithAlternates` | `salt` / `ssNN` / `cvNN` | on |
| `ligatures` | `liga` / `dlig` / `clig` / `rlig` | on |
| `sets` | `ssNN` + `smufl_sets_template.json` | on |
| `optionalGlyphs` | U+F400–U+F8FF | on |

Writes are atomic: a failure leaves no partial file and never modifies the
`.glyphs` project.

## Configuration

Copy `smufl-config.example.json` to `<font file name>.smufl-config.json`
next to the `.glyphs` file (for example `MyFont.smufl-config.json`) and
override what you need. Every key is optional.

## Data files

| File | Purpose | License |
|---|---|---|
| `smufl_metadata_exporter.py` | export core | Apache-2.0 |
| `data/generated/smufl_glyphnames.json` | canonical names/codepoints/descriptions/classes | Apache-2.0 + SMuFL notice |
| `smufl_optional_reference.json` | reference descriptions/classes for optional glyphs | **OFL-1.1** |
| `smufl_sets_template.json` | `ssNN` stylistic set template | **OFL-1.1** |

The exporter also accepts the unmerged official `glyphnames.json` (set
`SMUFL_GLYPHNAMES_PATH`), but then `optionalGlyphs[].classes` is empty.

## Tests

```bash
cd plugin
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

57 unit tests against a mock Glyphs object model; no Glyphs installation
needed. Real-font headless checks are described in `tests/README.md`.

## Glyph name differences

Glyphs does not accept glyph names that start with a digit, so the data
table uses:

```text
4stringTabClef -> fourStringTabClef
6stringTabClef -> sixStringTabClef
```

The exporter maps them back to the canonical SMuFL names internally. The
output JSON always uses the canonical names; `unicode` / `production` are
unaffected.

## License

The exporter is Apache-2.0. The plugin launcher (`bundle/Contents/MacOS/`)
comes from GlyphsSDK, Apache-2.0. The two reference JSON files are OFL-1.1;
do not remove their copyright headers. See the repository `NOTICE`.
