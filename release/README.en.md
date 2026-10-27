# Release packages

> Chinese is the primary language. [中文](README.md) · [日本語](README.ja.md)

Install/uninstall packages for the two components, plus manual install files.

| File | Purpose |
|---|---|
| `pkg/SMuFL-Glyphs.pkg` | Install the classification tables (GlyphData, Groups, icons, filters) |
| `pkg/SMuFL-Glyphs-Uninstall.pkg` | Remove them |
| `pkg/SMuFL-Metadata.pkg` | Install the metadata exporter plugin |
| `pkg/SMuFL-Metadata-Uninstall.pkg` | Remove it |

Manual install:

| Folder | Purpose |
|---|---|
| `manual/SMuFL Glyphs/` | Copy `Info/` and `Filters/` into Glyphs' Application Support |
| `manual/SMuFL Metadata/` | Copy `SMuFL Metadata.glyphsPlugin` into `Plugins/` |

## Install

The two components are independent; install either one.

1. Double-click `SMuFL-Glyphs.pkg` and follow the installer.
2. Double-click `SMuFL-Metadata.pkg` and follow the installer.
3. Quit Glyphs completely (Cmd-Q) and reopen it.


Install location:

```text
~/Library/Application Support/Glyphs 4/
```

### Unsigned package

The first time you open the package, macOS blocks it with an "Apple could not
verify" warning. To continue:

1. Click **Done**.
2. Open **System Settings → Privacy & Security** and scroll to **Security**.
3. Under "Allow applications from", find the blocked package and click
   **Open Anyway**.
4. Confirm with Touch ID or your password.
5. Click **Open Anyway** again in the dialog that appears.

If the package is not listed, double-click it once and check the settings
again.

## Uninstall

Double-click the matching `Uninstall.pkg`; the final page says the
uninstallation is complete. Then restart Glyphs.

## Version

1.1.0.
