#!/usr/bin/env python3
"""Build Groups-SMuFL.plist from the official SMuFL metadata + the layout file.

Inputs : data/upstream/{glyphnames,classes,ranges}.json
         data/layout/legacy.json
Outputs: data/generated/Groups-SMuFL.plist

The layout file describes *structure only*: group names, nesting and which
SMuFL range/class feeds each leaf.  Every glyph list is looked up in the
official metadata, so no glyph list is stored in this repository.

Layout node kinds:
    {"name": ..., "children": [...]}      a group
    {"name": ..., "range": "<key>"}       leaf fed by ranges.json
    {"name": ..., "class": "<key>"}       leaf fed by classes.json
    {"name": ..., "list": [...]}          leaf with an explicit list (unused)

Optional keys: "icon" (file stem in icons/), "predicate", "hidden".
"""
from __future__ import annotations

import os
import plistlib
import sys
from typing import Dict, List

import smufl_common as common


def build():
    glyphnames = common.upstream("glyphnames.json")
    classes = common.upstream("classes.json")
    ranges = common.upstream("ranges.json")
    layout = common.load_json(os.path.join(common.LAYOUT, "legacy.json"))

    codepoints: Dict[str, int] = {}
    for name, entry in glyphnames.items():
        number = common.codepoint_to_int(entry.get("codepoint"))
        if number is not None:
            codepoints[common.glyphs_name(name)] = number

    def glyphs(names) -> List[str]:
        known = [common.glyphs_name(n) for n in names if n in glyphnames]
        return common.sort_names_by_codepoint(known, codepoints)

    def resolve(node) -> List[str]:
        if "range" in node:
            key = node["range"]
            if key not in ranges:
                common.fail("layout references unknown range %r" % key)
            return glyphs(ranges[key].get("glyphs", []))
        if "class" in node:
            key = node["class"]
            if key not in classes:
                common.fail("layout references unknown class %r" % key)
            return glyphs(classes[key])
        if "list" in node:
            return glyphs(node["list"])
        collected: List[str] = []
        for child in node.get("children", []):
            collected.extend(resolve(child))
        return common.sort_names_by_codepoint(collected, codepoints)

    def convert(node) -> dict:
        out: Dict[str, object] = {"name": node["name"]}
        icon = node.get("icon")
        if icon and common.icon_exists(icon):
            out["icon"] = icon
        for key in ("predicate", "hidden"):
            if key in node:
                out[key] = node[key]
        if "children" in node:
            out["subGroup"] = [convert(child) for child in node["children"]]
        else:
            out["list"] = resolve(node)
        return out

    categories = [convert(category) for category in layout["categories"]]

    def leaf(name: str, names: List[str]) -> dict:
        return {"name": name, "list": common.sort_names_by_codepoint(names, codepoints)}

    def find_named(node, name: str) -> List[dict]:
        found = []
        if node.get("name") == name:
            found.append(node)
        for child in node.get("children", []):
            found.extend(find_named(child, name))
        return found

    def collect_named(node, name: str) -> List[str]:
        """Union of every leaf called `name` anywhere below `node`.

        A group that happens to have the same name is not itself a leaf, so it
        is only descended into; this mirrors how the sidebar lists are built.
        """
        collected: List[str] = []
        for child in node.get("children", []):
            if child.get("name") == name and "children" not in child:
                collected.extend(resolve(child))
            collected.extend(collect_named(child, name))
        return collected

    by_name = {category["name"]: category for category in layout["categories"]}
    precreate = []
    for spec in layout["languages"][0]["precreate"]:
        source = spec["from"]
        if source == "all":
            names = glyphs(list(glyphnames))
        elif source.startswith("category:"):
            category = by_name.get(source.split(":", 1)[1])
            if category is None:
                common.fail("unknown category %r" % source)
            names = resolve(category)
        elif source.startswith("basics:"):
            basics = by_name.get("SMuFL Common Glyphs")
            matches = find_named(basics, source.split(":", 1)[1])
            if not matches:
                common.fail("no %r group under SMuFL Common Glyphs" % source)
            names = resolve(matches[0])
        elif source.startswith("name:"):
            needle = source.split(":", 1)[1]
            names = []
            for category in layout["categories"]:
                names.extend(collect_named(category, needle))
            # The language tree repeats a few groups (e.g. medieval clefs).
            for child in layout["languages"][0].get("children", []):
                names.extend(collect_named(child, needle))
        else:
            common.fail("unknown precreate source %r" % source)
        precreate.append(leaf(spec["name"], names))

    language_layout = layout["languages"][0]
    language: Dict[str, object] = {"name": language_layout["name"]}
    for key in ("icon", "predicate", "hidden"):
        if key in language_layout:
            if key == "icon" and not common.icon_exists(language_layout[key]):
                continue
            language[key] = language_layout[key]
    language["subGroup"] = precreate + [convert(child)
                                        for child in language_layout.get("children", [])]

    return {"categories": categories, "languages": [language]}, len(codepoints)


def main() -> int:
    document, total = build()
    os.makedirs(os.path.dirname(common.GROUPS_PLIST), exist_ok=True)
    with open(common.GROUPS_PLIST, "wb") as handle:
        plistlib.dump(document, handle, fmt=plistlib.FMT_XML, sort_keys=False)
    print("wrote %s (%d glyph names, %d bytes)"
          % (common.GROUPS_PLIST, total, os.path.getsize(common.GROUPS_PLIST)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
