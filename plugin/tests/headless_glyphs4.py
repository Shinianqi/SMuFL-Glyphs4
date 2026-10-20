#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Optional headless integration test using Glyphs 4's own GlyphsCore.

This is NOT needed to run the exporter in Glyphs.  It is a development aid:
it loads a real .glyphs project through GlyphsCore (the same framework the
Glyphs app uses), calls the exporter's pure `run_export()` function, and
prints the validation report.  It verifies the actual Glyphs 4 API calls
(`font.masters`, `glyph.layerForId_()`, `layer.anchors`, `anchor.position`,
`layer.bounds`, `layer.width`, font version/UPM properties) without opening
the Glyphs GUI.

Requirements:
  * macOS with Glyphs 4 installed
  * a Python 3.9+ environment with PyObjC (objc + Foundation/AppKit):
        python3 -m venv .venv
        .venv/bin/pip install pyobjc-framework-Cocoa

Usage:
  .venv/bin/python tests/headless_glyphs4.py /path/to/Font.glyphs \
      /tmp/Font.json [/path/to/Font.smufl-config.json]

The font file is opened read-only; this harness does not save it.
"""
import argparse
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
os.environ["SMUFL_EXPORTER_NO_MAIN"] = "1"


def load_glyphs_app():
    try:
        import objc
        from Foundation import NSBundle, NSObject
    except Exception as exc:
        raise SystemExit(
            "PyObjC is required for this optional harness. Create a venv and run "
            "`.venv/bin/pip install pyobjc-framework-Cocoa`.\n"
            f"Import error: {exc}"
        )
    app = "/Applications/Glyphs 4.app"
    if not os.path.isdir(app):
        raise SystemExit("Glyphs 4 was not found at /Applications/Glyphs 4.app")
    for rel in (
        "Contents/Frameworks/GlyphsCore.framework",
        "Contents/Frameworks/GlyphsApp.framework",
        "Contents/Frameworks/GlyphsKit.framework",
        "Contents/Frameworks/GSFontTools.framework",
    ):
        bundle = NSBundle.bundleWithPath_(os.path.join(app, rel))
        if bundle is not None:
            bundle.load()
    # GSApplication lives in the Glyphs executable, not in the frameworks.
    # GlyphsApp imports it at module import time; a stub is enough because
    # this harness only uses GSFont/GSGlyph/GSLayer/GSAnchor.
    real_lookup = objc.lookUpClass

    class _DummyApplication(NSObject):
        pass

    def lookup(name):
        try:
            return real_lookup(name)
        except Exception:
            return _DummyApplication

    objc.lookUpClass = lookup
    sys.path.insert(0, os.path.join(app, "Contents", "Scripts"))
    import GlyphsApp  # noqa: E402
    return GlyphsApp


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font", help="path to a .glyphs / .glyphspackage project")
    parser.add_argument("output", nargs="?", help="output JSON path (default: next to font)")
    parser.add_argument("config", nargs="?", help="optional sidecar config JSON")
    parser.add_argument("--report", help="also write the validation report to this path")
    args = parser.parse_args(argv)

    if args.output is None:
        args.output = os.path.splitext(os.path.abspath(args.font))[0] + ".json"

    try:
        GlyphsApp = load_glyphs_app()
        font = GlyphsApp.GSFont(args.font)
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        return 2

    import smufl_metadata_exporter as exporter

    report = exporter.Report()
    result = exporter.run_export(
        font,
        args.output,
        config_path=args.config,
        script_dir=ROOT,
        report=report,
    )
    text = exporter.format_report(result)
    print(text)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        print(f"Validation report: {args.report}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
