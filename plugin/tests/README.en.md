# Tests

> Chinese is the primary language. [中文](README.md) · [日本語](README.ja.md)

## 1. Unit tests (no Glyphs installation required)

```bash
cd ..
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

The tests inject a small mock of the Glyphs 4 object model (`font.masters`,
`glyph.layerForId_()`, `layer.anchors`, `anchor.position`, `layer.bounds`,
`layer.width`, `font.features`, …); PyObjC and Glyphs are not needed.

`SMUFL_EXPORTER_NO_MAIN=1` stops the script from running its Glyphs menu
entry on import.

There are **57 tests**, covering:

- staff space conversion (UPM 1000 / 2048);
- canonical names, aliases, Unicode fallback, refusing to guess;
- multi-master strategy;
- optional glyphs, classes, descriptions;
- `salt` / `ssNN` alternates, `ssNN` sets, `liga` ligatures;
- `engravingDefaults` / `designSize` / `sizeRange` and `metadataSource`;
- BBox / advance width on and off;
- new field validation, NaN, duplicates, unknown keys;
- atomic writes, repeated runs, no overwrite on failure;
- the simulated Script menu entry.

## 2. Optional headless run on a real font (Glyphs 4 + PyObjC)

```bash
python3 -m venv .venv
.venv/bin/pip install pyobjc-framework-Cocoa

.venv/bin/python tests/headless_glyphs4.py \
  "/path/to/YourFont.glyphs" \
  /tmp/YourFont.json \
  --report /tmp/YourFont_report.txt
```

The tool only stubs `GSApplication` (it lives in the Glyphs executable, not
in the framework) so that `GlyphsApp` can be imported; `GSFont`, `GSGlyph`,
`GSLayer`, `GSAnchor`, `layer.bounds` and so on are the real GlyphsCore 4.2
classes. The font is opened read-only and never saved.

This tool is a development aid only. The normal Glyphs script needs no extra
PyObjC install; the Python bundled with Glyphs already provides AppKit.

## 3. Sample

No sample font is included. To verify, run the headless command above with
your own project.
