#!/usr/bin/env python3
"""Consistency checks for the generated SMuFL data.

Run after `python3 tools/build_all.py`:

    python3 tools/verify.py

Exits non-zero on the first failed check and prints what was expected.
"""
from __future__ import annotations

import hashlib
import os
import plistlib
import re
import sys
from typing import Dict, List

import smufl_common as common

FAILURES: List[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def main() -> int:
    # ---- upstream snapshot integrity -----------------------------------------
    sums_path = os.path.join(common.UPSTREAM, "SHA256SUMS")
    check(os.path.isfile(sums_path), "data/upstream/SHA256SUMS is missing")
    if os.path.isfile(sums_path):
        with open(sums_path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                digest, filename = line.split(None, 1)
                path = os.path.join(common.UPSTREAM, filename.strip())
                check(os.path.isfile(path), "missing upstream file %r" % filename)
                if os.path.isfile(path):
                    with open(path, "rb") as fh:
                        actual = hashlib.sha256(fh.read()).hexdigest()
                    check(actual == digest,
                          "upstream %r sha256 is %s, expected %s"
                          % (filename, actual, digest))

    glyphnames = common.upstream("glyphnames.json")
    classes = common.upstream("classes.json")
    ranges = common.upstream("ranges.json")

    # ---- GlyphData-SMuFL.xml --------------------------------------------------
    check(os.path.isfile(common.GLYPH_DATA_XML), "GlyphData-SMuFL.xml is missing")
    xml = open(common.GLYPH_DATA_XML, encoding="utf-8").read() \
        if os.path.isfile(common.GLYPH_DATA_XML) else ""
    rows = re.findall(r"<glyph\b[^>]*/>", xml)
    table = {}
    for row in rows:
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', row))
        table[attrs["name"]] = attrs

    check(len(rows) == len(glyphnames),
          "GlyphData has %d glyphs, SMuFL has %d" % (len(rows), len(glyphnames)))
    expected_names = {common.glyphs_name(n) for n in glyphnames}
    check(set(table) == expected_names,
          "GlyphData names differ: missing=%s extra=%s"
          % (sorted(expected_names - set(table))[:8],
             sorted(set(table) - expected_names)[:8]))

    for name, attrs in table.items():
        for key in ("sortName", "unicode", "production", "category", "script"):
            check(key in attrs, "%s has no %s" % (name, key))
        check(attrs.get("category") == "SMuFL", "%s category is not SMuFL" % name)
        check(attrs.get("script") == "musical", "%s script is not musical" % name)
        check(re.fullmatch(r"SMuFL\.[0-9A-F]{5}", attrs.get("sortName", "")),
              "%s has unexpected sortName %r" % (name, attrs.get("sortName")))
        seen_names = set()
        seen_positions = set()
        for anchor in [a.strip() for a in attrs.get("anchors", "").split(",") if a.strip()]:
            check("@" in anchor and ";" in anchor,
                  "%s has an anchor without a position: %r" % (name, anchor))
            if "@" not in anchor or ";" not in anchor:
                continue
            anchor_name, position = anchor.split("@", 1)
            x, y = position.split(";", 1)
            check(anchor_name not in seen_names,
                  "%s has duplicate anchor %r" % (name, anchor_name))
            check((x, y) not in seen_positions,
                  "%s has two anchors at the same position" % name)
            seen_names.add(anchor_name)
            seen_positions.add((x, y))

    # ---- Groups-SMuFL.plist ---------------------------------------------------
    check(os.path.isfile(common.GROUPS_PLIST), "Groups-SMuFL.plist is missing")
    document = plistlib.load(open(common.GROUPS_PLIST, "rb")) \
        if os.path.isfile(common.GROUPS_PLIST) else {}
    known = set(table)
    seen_lists = 0

    def walk(node, path):
        nonlocal seen_lists
        if isinstance(node, list):
            for child in node:
                walk(child, path)
        elif isinstance(node, dict):
            if "list" in node:
                seen_lists += 1
                names = node["list"]
                check(bool(names), "%s / %s is empty" % (path, node.get("name")))
                unknown = [n for n in names if n not in known]
                check(not unknown,
                      "%s / %s references unknown glyphs: %s"
                      % (path, node.get("name"), unknown[:5]))
                duplicates = {n for n in names if names.count(n) > 1}
                check(not duplicates,
                      "%s / %s has duplicates: %s"
                      % (path, node.get("name"), sorted(duplicates)[:5]))
            for key in ("subGroup", "categories", "languages"):
                if key in node:
                    walk(node[key], path + "/" + str(node.get("name")))

    walk(document, "")
    check(seen_lists > 100, "only %d groups were written" % seen_lists)

    # The "Flags" leaf carries a zero-width space so Glyphs' categories.strings
    # does not localize it. Guard against accidentally dropping it.
    def collect_names(node, out):
        if isinstance(node, list):
            for child in node:
                collect_names(child, out)
        elif isinstance(node, dict):
            if node.get("name"):
                out.append(node["name"])
            for value in node.values():
                if isinstance(value, (list, dict)):
                    collect_names(value, out)

    all_group_names = []
    collect_names(document, all_group_names)
    check("Flags\u200b" in all_group_names,
          "the 'Flags' group lost its zero-width space")
    check("Flags" not in all_group_names,
          "a plain 'Flags' group would be localized by Glyphs")

    categories = document.get("categories", [])
    names = [c.get("name") for c in categories]
    check(names == ["SMuFL Glyphs", "SMuFL Common Glyphs"],
          "unexpected top-level categories: %s" % names)
    for category in categories:
        check(bool(category.get("subGroup", [])),
              "%s has no groups" % category.get("name"))
        for group in category.get("subGroup", []):
            check("list" in group or bool(group.get("subGroup")),
                  "%s / %s is empty" % (category.get("name"), group.get("name")))

    languages = document.get("languages", [])
    check(len(languages) == 1, "expected exactly one language entry")
    precreate = [e for e in (languages[0].get("subGroup", []) if languages else [])
                 if "list" in e]
    expected = ["SMuFL Common Glyphs", "SMuFL Glyphs", "Clefs",
                "Time Signatures", "Notes & Rests"]
    check([e.get("name") for e in precreate] == expected,
          "unexpected precreate entries: %s" % [e.get("name") for e in precreate])
    all_names = {n for n in table}
    for entry in precreate:
        check(set(entry.get("list", [])) <= all_names,
              "precreate %r contains unknown names" % entry.get("name"))
    check(any(len(entry.get("list", [])) == len(glyphnames) for entry in precreate),
          "'SMuFL Glyphs' does not contain every glyph")

    # ---- plugin snapshot ------------------------------------------------------
    check(os.path.isfile(common.GLYPHNAMES_JSON),
          "data/generated/smufl_glyphnames.json is missing")
    if os.path.isfile(common.GLYPHNAMES_JSON):
        snapshot = common.load_json(common.GLYPHNAMES_JSON)
        glyphs = snapshot.get("glyphs", {})
        check(set(glyphs) == set(glyphnames),
              "snapshot names differ from SMuFL glyphnames.json")
        check(snapshot.get("glyphCount") == len(glyphnames),
              "snapshot glyphCount is wrong")
        class_names = set(classes)
        for name, entry in glyphs.items():
            check(set(entry.get("classes", [])) <= class_names,
                  "snapshot %s has unknown classes" % name)

    if FAILURES:
        print("FAILED (%d)" % len(FAILURES))
        for message in FAILURES:
            print("  - " + message)
        return 1

    print("OK  %d glyphs, %d classes, %d ranges, %d lists checked"
          % (len(glyphnames), len(classes), len(ranges), seen_lists))
    return 0


if __name__ == "__main__":
    sys.exit(main())
