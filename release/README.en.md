# Release packages

Install/uninstall packages for the two components, plus manual install files.

| File | Purpose |
|---|---|
| `pkg/SMuFL Glyphs.pkg` | Install the classification tables (GlyphData, Groups, icons, filters) |
| `pkg/SMuFL Glyphs Uninstall.pkg` | Remove them |
| `pkg/SMuFL Metadata.pkg` | Install the metadata exporter plugin |
| `pkg/SMuFL Metadata Uninstall.pkg` | Remove it |

Manual install:

| Folder | Purpose |
|---|---|
| `manual/SMuFL Glyphs/` | Copy `Info/` and `Filters/` into Glyphs' Application Support |
| `manual/SMuFL Metadata/` | Copy `SMuFL Metadata.glyphsPlugin` into `Plugins/` |

## Install

The two components are independent; install either one.

1. Double-click `SMuFL Glyphs.pkg` and follow the installer.
2. Double-click `SMuFL Metadata.pkg` and follow the installer.
3. Quit Glyphs completely (Cmd-Q) and reopen it.

The packages are unsigned. If Gatekeeper blocks the first launch, right-click
and choose Open.

The packages write to the current user's:

```text
~/Library/Application Support/Glyphs 4/
```

## Uninstall

Double-click the matching `Uninstall.pkg`; the final page says the
uninstallation is complete. Then restart Glyphs.

## Version

1.0.0.
