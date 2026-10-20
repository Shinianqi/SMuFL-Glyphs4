# encoding: utf-8
"""Glyphs 4 General Plugin wrapper for the SMuFL metadata exporter."""

import os
import sys
import time

_RESOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
_LOG_PATH = os.path.join(os.path.expanduser("~"), "Library", "Logs", "SMuFLMetadataExporter.log")


def _log(message):
    try:
        os.makedirs(os.path.dirname(_LOG_PATH), exist_ok=True)
        with open(_LOG_PATH, "a", encoding="utf-8") as handle:
            handle.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] plugin: {message}\n")
    except Exception:
        pass


_log("plugin module imported")

try:
    import objc
    from AppKit import NSMenuItem
    from GlyphsApp import Glyphs, SCRIPT_MENU
    from GlyphsApp.plugins import GeneralPlugin
except Exception as exc:
    _log(f"plugin import failed: {exc!r}")
    raise

if _RESOURCE_DIR not in sys.path:
    sys.path.insert(0, _RESOURCE_DIR)

# The exporter normally runs main() at import time.  In the plugin, import it
# as a library and call main() only from the menu action.
os.environ["SMUFL_EXPORTER_NO_MAIN"] = "1"
try:
    import smufl_metadata_exporter as exporter
except Exception as exc:
    _log(f"exporter import failed: {exc!r}")
    raise


class SMuFLMetadataPlugin(GeneralPlugin):
    @objc.python_method
    def settings(self):
        self.name = "Export SMuFL Metadata…"
        _log("settings")

    @objc.python_method
    def start(self):
        menu = Glyphs.menu[SCRIPT_MENU]
        # Glyphs can re-run a plugin's start() during a reload without
        # recreating the menu.  Do not append a second identical item.
        try:
            for existing in menu.itemArray():
                if existing.title() == self.name:
                    # Reuse the item but retarget it at the current plugin
                    # instance, so a reload cannot leave a stale target.
                    existing.setTarget_(self)
                    existing.setAction_(self.exportMetadata_)
                    _log("menu item reused")
                    return
        except Exception as exc:
            _log(f"menu scan failed: {exc!r}")
        item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            self.name, self.exportMetadata_, ""
        )
        item.setTarget_(self)
        menu.append(item)
        _log("menu item added")

    def exportMetadata_(self, sender):
        _log("menu action")
        exporter.main()

    @objc.python_method
    def __file__(self):
        return __file__
