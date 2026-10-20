#!/usr/bin/env python3
"""Build GlyphData-SMuFL.xml from the official SMuFL metadata.

Input : data/upstream/glyphnames.json, data/upstream/ranges.json
Output: data/generated/GlyphData-SMuFL.xml

The output is a Glyphs "GlyphData" XML file.  Every value in it comes from
the SMuFL specification metadata; the only transformations are:

  * SMuFL codepoints become Glyphs `unicode`/`production` values,
  * `sortName` is rewritten to SMuFL.<codepoint> so Glyphs sorts by codepoint,
  * the two digit-leading SMuFL names get a Glyphs-safe spelling,
  * `category`/`subCategory` are derived from the SMuFL ranges,
  * `anchors` comes from data/layout/anchors.glyphs.json (per glyph) or
    data/layout/anchors.json (per range).

The DOCTYPE block below is the Glyphs GlyphData file format (a functional
interface definition), not content taken from another SMuFL package.
"""
from __future__ import annotations

import os
import sys
from typing import Dict, Tuple

import smufl_common as common

HEADER = """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE glyphData [
<!ELEMENT glyphData (glyph)+>
<!ATTLIST glyphData
\tformat\t\t\tCDATA\t\t#IMPLIED>
<!ELEMENT glyph EMPTY>
<!ATTLIST glyph
\tunicode\t\t\tCDATA\t\t#IMPLIED
\tunicodeLegacy\tCDATA\t\t#IMPLIED
\tname\t\t\tCDATA\t\t#REQUIRED
\tsortName\t\tCDATA\t\t#IMPLIED
\tsortNameKeep\t\tCDATA\t\t#IMPLIED
\tcategory\t\tCDATA\t\t#REQUIRED
\tsubCategory\t\tCDATA\t\t#IMPLIED
\tcase\t\t\tCDATA\t\t#IMPLIED
\tdirection\t\tCDATA\t\t#IMPLIED
\tscript\t\t\tCDATA\t\t#IMPLIED
\tdescription\t\tCDATA\t\t#IMPLIED
\tproduction\t\tCDATA\t\t#IMPLIED
\taltNames\t\tCDATA\t\t#IMPLIED
\tdecompose\t\tCDATA\t\t#IMPLIED
\tanchors\t\t\tCDATA\t\t#IMPLIED
\tmarks\t\t\tCDATA\t\t#IMPLIED>
]>
"""


def range_index(ranges: Dict[str, dict]) -> Dict[str, Tuple[str, str]]:
    """SMuFL glyph name -> (range key, range description)."""
    index: Dict[str, Tuple[str, str]] = {}
    for key, value in ranges.items():
        description = value.get("description") or key
        for name in value.get("glyphs", []):
            if name in index:
                common.fail(
                    "%s appears in both %r and %r; GlyphData only has one "
                    "subCategory" % (name, index[name][0], key)
                )
            index[name] = (key, description)
    return index


def build() -> str:
    glyphnames = common.upstream("glyphnames.json")
    ranges = common.upstream("ranges.json")
    by_range = range_index(ranges)

    # Optional anchors: see data/layout/anchors.json.  Kept separate so the
    # positions can be tuned without touching the generator.
    anchor_rules: Dict[str, str] = {}
    anchors_path = os.path.join(common.LAYOUT, "anchors.json")
    if os.path.isfile(anchors_path):
        for rule in common.load_json(anchors_path).get("rules", []):
            for key in rule.get("ranges") or [rule["range"]]:
                anchor_rules[key] = rule["anchors"]

    # Per-glyph anchors imported from Bravura (data/layout/anchors.glyphs.json).
    # They take precedence over the range defaults because they carry the
    # reference positions for each individual glyph.
    anchor_glyphs: Dict[str, str] = {}
    glyph_anchors_path = os.path.join(common.LAYOUT, "anchors.glyphs.json")
    if os.path.isfile(glyph_anchors_path):
        anchor_glyphs = common.load_json(glyph_anchors_path).get("glyphs", {})

    codepoints = {}
    for name, entry in glyphnames.items():
        number = common.codepoint_to_int(entry.get("codepoint"))
        if number is None:
            common.fail("no usable codepoint for %r" % name)
        codepoints[name] = number

    lines = []
    for name in sorted(glyphnames, key=lambda n: (codepoints[n], n)):
        entry = glyphnames[name]
        number = codepoints[name]
        if number > 0xFFFF:
            common.fail("%s is outside the BMP; Glyphs production naming " % name
                        + "for this case has not been verified")
        description = (entry.get("description") or "").strip()
        out_name = common.glyphs_name(name)
        range_info = by_range.get(name)
        attributes = [
            'name="%s"' % common.xml_escape(out_name),
            'sortName="SMuFL.%05X"' % number,
        ]
        if description:
            attributes.append('description="%s"' % common.xml_escape(description))
        attributes.append('category="SMuFL"')
        if range_info:
            attributes.append('subCategory="%s"' % common.xml_escape(range_info[1]))
        else:
            print("warning: %s is in no SMuFL range; no subCategory" % name,
                  file=sys.stderr)
        attributes.append('unicode="%04X"' % number)
        attributes.append('production="uni%04X"' % number)
        anchor_value = anchor_glyphs.get(name)
        if not anchor_value and range_info:
            anchor_value = anchor_rules.get(range_info[0])
        if anchor_value:
            attributes.append('anchors="%s"' % common.xml_escape(anchor_value))
        attributes.append('script="musical"')
        lines.append("\t<glyph %s/>" % " ".join(attributes))

    if len(lines) != len(glyphnames):
        common.fail("expected %d glyphs, wrote %d" % (len(glyphnames), len(lines)))

    return HEADER + '<glyphData format="2">\n' + "\n".join(lines) + "\n</glyphData>\n"


def main() -> int:
    text = build()
    common.write_text(common.GLYPH_DATA_XML, text)
    print("wrote %s (%d glyphs, %d bytes)"
          % (common.GLYPH_DATA_XML, text.count("<glyph "), len(text.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
