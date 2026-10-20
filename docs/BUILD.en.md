# Build

> Chinese is the primary language. [中文](BUILD.md) · [日本語](BUILD.ja.md)

Requires Python 3.9+ (standard library only); building `.pkg` requires macOS.

## Generate the data

```bash
python3 tools/build_all.py
```

| Step | Output |
|---|---|
| `build_glyphdata.py` | `data/generated/GlyphData-SMuFL.xml` |
| `build_groups.py` | `data/generated/Groups-SMuFL.plist` |
| `build_glyphnames_snapshot.py` | `data/generated/smufl_glyphnames.json` |
| `verify.py` | consistency checks |

Output is deterministic; the generated files are committed so users never need
to run Python.

## Update SMuFL

```bash
python3 tools/fetch_upstream.py --ref v1.5
python3 tools/build_all.py
git diff --stat data/
```

`fetch_upstream.py` uses the GitHub contents API and updates `VERSION.json`
and `SHA256SUMS`.

## Install and package

```bash
./install/install.sh              # development install
./install/install.sh --uninstall
./install/build-release.sh        # 4 packages + manual files in release/
```

## Plugin

```bash
./plugin/build.sh          # build/SMuFL Metadata.glyphsPlugin
```

The bundle is the `plugin/bundle/` GlyphsSDK skeleton plus the exporter and the
generated `smufl_glyphnames.json`. `build-release.sh` calls it.

## Tests

```bash
cd plugin
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

## Editing the sidebar

Edit `data/layout/legacy.json`:

- group: `{"name": ..., "icon": ..., "children": [...]}`
- leaf: `{"name": ..., "range": "<ranges.json key>"}` or
  `{"name": ..., "class": "<classes.json key>"}`
- `languages[0].precreate` defines the startup-window entries; `from` accepts
  `all` / `category:<name>` / `basics:<name>` / `name:<leaf name>`.

Leaves contain no glyph lists; glyphs come from the official data.

> The name `Flags` has a zero-width space (U+200B) at the end. Glyphs'
> `categories.strings` localizes `Flags`, and this character bypasses the
> localization so the sidebar still shows `Flags`. Do not delete it when editing.
