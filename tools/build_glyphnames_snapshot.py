#!/usr/bin/env python3
"""Build the compact glyph-name snapshot consumed by the Glyphs plugin.

Inputs : data/upstream/glyphnames.json, data/upstream/classes.json
Outputs: data/generated/smufl_glyphnames.json

The plugin loader also accepts the raw official glyphnames.json, but the
official file does not carry class membership.  This snapshot merges the
inverted classes.json into each glyph so `optionalGlyphs[].classes` can be
filled in without a second lookup table.
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List

import smufl_common as common


def build() -> dict:
    glyphnames = common.upstream("glyphnames.json")
    classes = common.upstream("classes.json")
    version = common.load_json(os.path.join(common.UPSTREAM, "VERSION.json"))

    membership: Dict[str, List[str]] = {}
    for class_name, members in classes.items():
        for name in members:
            membership.setdefault(name, []).append(class_name)

    glyphs = {}
    for name in glyphnames:
        entry = glyphnames[name]
        item = {
            "codepoint": "U+" + common.codepoint_hex(entry.get("codepoint")),
            "classes": sorted(membership.get(name, [])),
        }
        description = (entry.get("description") or "").strip()
        if description:
            item["description"] = description
        glyphs[name] = item

    return {
        "_source": "https://github.com/w3c-cg/smufl/blob/gh-pages/metadata/glyphnames.json",
        "_classesSource": "https://github.com/w3c-cg/smufl/blob/gh-pages/metadata/classes.json (inverted)",
        "_commit": version.get("commit"),
        "_specVersion": version.get("specVersion"),
        "_retrieved": version.get("retrieved"),
        "_note": "Compact snapshot: canonical names, codepoints, descriptions and classes.",
        "glyphCount": len(glyphs),
        "glyphs": glyphs,
    }


def main() -> int:
    document = build()
    common.write_json(common.GLYPHNAMES_JSON, document)
    print("wrote %s (%d names)" % (common.GLYPHNAMES_JSON, document["glyphCount"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
