#!/usr/bin/env python3
"""Shared helpers for the data build.

Only the official SMuFL metadata files under data/upstream/ are used.
"""
from __future__ import annotations

import json
import os
import re
import sys
from typing import Any, Dict, Iterable, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPSTREAM = os.path.join(ROOT, "data", "upstream")
LAYOUT = os.path.join(ROOT, "data", "layout")
GENERATED = os.path.join(ROOT, "data", "generated")
ICONS = os.path.join(ROOT, "icons")

GLYPH_DATA_XML = os.path.join(GENERATED, "GlyphData-SMuFL.xml")
GROUPS_PLIST = os.path.join(GENERATED, "Groups-SMuFL.plist")
GLYPHNAMES_JSON = os.path.join(GENERATED, "smufl_glyphnames.json")


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def upstream(name: str) -> Any:
    return load_json(os.path.join(UPSTREAM, name))


def write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json(path: str, obj: Any) -> None:
    write_text(path, json.dumps(obj, ensure_ascii=False, indent=1) + "\n")


def codepoint_to_int(value: Any) -> int | None:
    """Accept "U+E06E", "E06E", "0xE06E" or an int; return None if unusable."""
    if isinstance(value, int):
        return value
    if not isinstance(value, str):
        return None
    text = value.strip()
    if text.upper().startswith("U+"):
        text = text[2:]
    elif text.lower().startswith("0X"):
        text = text[2:]
    text = text.replace(" ", "")
    if not re.fullmatch(r"[0-9A-Fa-f]{4,6}", text):
        return None
    return int(text, 16)


def codepoint_hex(value: Any) -> str | None:
    number = codepoint_to_int(value)
    return None if number is None else "%04X" % number


# Glyphs rejects glyph names that start with a digit.  SMuFL has two of them,
# so the GlyphData table spells them out.  This is a Glyphs compatibility
# rule, not something inherited from another SMuFL package.
GLYPHS_SAFE_NAMES = {
    "4stringTabClef": "fourStringTabClef",
    "6stringTabClef": "sixStringTabClef",
}


def glyphs_name(smufl_name: str) -> str:
    return GLYPHS_SAFE_NAMES.get(smufl_name, smufl_name)


def xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def sort_names_by_codepoint(names: Iterable[str], codepoints: Dict[str, int]) -> List[str]:
    unique = dict.fromkeys(names)
    return sorted(unique, key=lambda name: (codepoints.get(name, 1 << 32), name))


def icon_exists(value: str | None) -> bool:
    """True if icons/<value><ext> exists; `value` already ends in "Template"."""
    if not value:
        return False
    for ext in (".svg", ".pdf", ".png"):
        if os.path.isfile(os.path.join(ICONS, value + ext)):
            return True
    return False


def fail(message: str) -> "NoReturn":  # noqa: F821 - typing only
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)
