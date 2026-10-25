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

## Glyph names

The script does not rename glyphs. Glyphs normally derives the production name
from Unicode (`uniE050`), so make sure every SMuFL glyph has its Unicode set
before export. If your workflow relies on glyph names matching codepoints, run
your usual rename step.

## Configuration

The exporter works without a config file or custom parameters.

Use the two options below only when you want to override measured values, pick
a master, add aliases or manual anchors, or turn off parts of the output.

### Glyphs custom parameters

Add these in Font Info → Font → Custom Parameters:

| Parameter | Value | Unit |
|---|---|---|
| `SMuFL Design Size` | one positive integer | decipoints (1/720 inch); `120` = 12 pt |
| `SMuFL Size Range` | two positive integers, e.g. `80, 480` or `80 480` | decipoints; `80, 480` = 8–48 pt |

Both are optional; without them the corresponding `designSize` / `sizeRange`
is omitted.

### Configuration file

Copy `smufl-config.example.json` to:

```
<project file name>.smufl-config.json
```

next to the `.glyphs` file. The name comes from the project file, not the
family name:

```
Naruto.glyphs          → Naruto.smufl-config.json
Naruto-Regular.glyphs  → Naruto-Regular.smufl-config.json
```

Edit only the keys you need; `null` means "do not override".
`SMUFL_CONFIG_PATH` can point elsewhere.

The config file can override any key, including things custom parameters cannot:

| Key | Purpose | Unit / example |
|---|---|---|
| `fontName` | override the family name | `"Naruto"` |
| `fontVersion` | override the version | `1.234` |
| `designSize` | override the design size | decipoints, `120` |
| `sizeRange` | override the size range | `[80, 480]` |
| `master` | pick a master when there are several | name or ID, `"Regular"` |
| `metadataSource` | fall back to an existing JSON | path relative to the `.glyphs` file |
| `engravingDefaults` | override individual measurements or the text font | staff spaces; `textFontFamily` is an array |
| `setsTemplate` | override `ssNN` type/description | see the example |
| `glyphNameAliases` | map custom names to SMuFL names | `{"myFlat": "accidentalFlat"}` |
| `glyphsWithAnchors` | add or override anchors | staff spaces, `[x, y]` |
| `include*` | switch output sections off | `false` omits the section |
| `_comment` | free-form note | ignored by the exporter |

Priority for `designSize` / `sizeRange`:

```
config file > Glyphs custom parameters > metadataSource > omitted
```

If both are set, the config file wins; leave the key `null` to use the custom
parameter.

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

59 unit tests against a mock Glyphs object model; no Glyphs installation
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
