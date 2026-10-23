#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for the SMuFL metadata exporter.

These tests use a small fake of the Glyphs 4 object model, so they run in any
Python 3.9+ environment without Glyphs installed.  The fake mirrors only the
properties the exporter reads: font.familyName, versionMajor/versionMinor,
upm, masters, glyphs, glyph.layerForId_(), layer.anchors, layer.width and
layer.bounds.

Run:
    cd plugin
    SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
"""
import json
import math
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

# In the repository the generated snapshot lives under data/generated/.
_snapshot = os.path.join(os.path.dirname(ROOT), "data", "generated", "smufl_glyphnames.json")
if os.path.isfile(_snapshot):
    os.environ.setdefault("SMUFL_GLYPHNAMES_PATH", _snapshot)
os.environ.setdefault("SMUFL_EXPORTER_NO_MAIN", "1")
os.environ.setdefault("SMUFL_DEBUG_LOG", "0")

import smufl_metadata_exporter as exporter  # noqa: E402


# ---------------------------------------------------------------------------
# Minimal Glyphs 4 object model
# ---------------------------------------------------------------------------

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Rect:
    def __init__(self, x, y, w, h):
        self.origin = Point(x, y)
        self.size = Size(w, h)


class Anchor:
    def __init__(self, name, x, y):
        self.name = name
        self.position = Point(x, y)


class Anchors(dict):
    """Mimics Glyphs 4's LayerAnchorsProxy: items() is the safe API."""

    def __iter__(self):
        return iter(self.values())


class Node:
    def __init__(self, x, y, node_type="line"):
        self.x = x
        self.y = y
        self.type = node_type


class Path:
    def __init__(self, nodes, closed=True):
        self.nodes = nodes
        self.closed = closed


class Layer:
    def __init__(self, anchors=None, width=500.0, bounds=None, paths=None):
        self.anchors = Anchors(anchors or {})
        self.width = width
        self.bounds = bounds or Rect(0.0, 0.0, width, 500.0)
        self.paths = paths or []

    def copyDecomposedLayer(self):
        return self


class Glyph:
    def __init__(self, name, unicode_value=None, anchors=None, width=500.0,
                 bounds=None, export=True, master_id="M1", unicodes=None, note="", paths=None):
        self.name = name
        self.unicode = unicode_value
        self.unicodes = unicodes if unicodes is not None else ([unicode_value] if unicode_value else [])
        self.export = export
        self.note = note
        self.layers = {master_id: Layer(anchors, width, bounds, paths)}

    def layerForId_(self, master_id):
        return self.layers.get(master_id)


class Master:
    def __init__(self, master_id, name):
        self.id = master_id
        self.name = name


class Feature:
    def __init__(self, name, code, active=True, automatic=False, notes=""):
        self.name = name
        self.code = code
        self.active = active
        self.automatic = automatic
        self.notes = notes


class Font:
    def __init__(self, glyphs, family_name="Test Music", version_major=1,
                 version_minor=234, upm=1000, masters=None, filepath="",
                 custom_parameters=None, features=None, classes=None):
        self.glyphs = glyphs
        self.familyName = family_name
        self.versionMajor = version_major
        self.versionMinor = version_minor
        self.upm = upm
        self.masters = masters or [Master("M1", "Regular")]
        self.filepath = filepath
        self.customParameters = custom_parameters or {}
        self.features = features or []
        self.classes = classes or []


def make_font(**kwargs):
    return Font(**kwargs)


def run_export(font, tmpdir, config=None, write=False, name="out.json"):
    config_path = None
    if config is not None:
        config_path = os.path.join(tmpdir, "test.smufl-config.json")
        with open(config_path, "w", encoding="utf-8") as handle:
            json.dump(config, handle)
    output = os.path.join(tmpdir, name)
    report = exporter.Report()
    result = exporter.run_export(
        font, output, config_path=config_path, script_dir=ROOT,
        report=report, write=write,
    )
    return result


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="smufl-test-")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Extraction and conversion
# ---------------------------------------------------------------------------

class TestExtraction(BaseCase):
    def test_basic_anchor_conversion_1000_upm(self):
        glyph = Glyph("noteheadBlack", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 304, 55),
            "stemDownNW": Anchor("stemDownNW", 0, -55),
            "top": Anchor("top", 100, 200),  # not SMuFL
        })
        font = make_font(glyphs=[glyph])
        result = run_export(font, self.tmpdir)
        self.assertTrue(result.report.ok, exporter.format_report(result))
        anchors = result.metadata["glyphsWithAnchors"]["noteheadBlack"]
        self.assertEqual(anchors["stemUpSE"], [1.216, 0.22])
        self.assertEqual(anchors["stemDownNW"], [0.0, -0.22])
        self.assertNotIn("top", anchors)

    def test_anchor_conversion_2048_upm(self):
        glyph = Glyph("noteheadBlack", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 304, 55),
        })
        font = make_font(glyphs=[glyph], upm=2048)
        result = run_export(font, self.tmpdir)
        anchors = result.metadata["glyphsWithAnchors"]["noteheadBlack"]
        self.assertEqual(anchors["stemUpSE"], [0.59375, 0.107422])

    def test_staff_space_is_upm_over_four(self):
        report = exporter.Report()
        font = make_font(glyphs=[], upm=2048)
        self.assertEqual(exporter._staff_space(font, report), 512.0)

    def test_alias_four_string_tab_clef(self):
        glyph = Glyph("fourStringTabClef", "E06E", {
            "cutOutNE": Anchor("cutOutNE", 100, 100),
        })
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir)
        self.assertIn("4stringTabClef", result.metadata["glyphsWithAnchors"])
        self.assertNotIn("fourStringTabClef", result.metadata["glyphsWithAnchors"])
        self.assertTrue(any(i.code == "glyph-alias" for i in result.report.warnings))

    def test_unicode_fallback_for_generic_name(self):
        glyph = Glyph("uniE0A4", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 250, 0),
        })
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir)
        self.assertIn("noteheadBlack", result.metadata["glyphsWithAnchors"])
        self.assertTrue(any(i.code == "glyph-unicode" for i in result.report.warnings))

    def test_non_generic_non_canonical_is_not_guessed(self):
        glyph = Glyph("myNotehead", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 250, 0),
        })
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir)
        self.assertNotIn("glyphsWithAnchors", result.metadata)
        self.assertTrue(any(i.code == "glyph-unmapped" for i in result.report.warnings))

    def test_config_alias_allows_explicit_mapping(self):
        glyph = Glyph("myNotehead", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 250, 0),
        })
        result = run_export(
            make_font(glyphs=[glyph]), self.tmpdir,
            config={"glyphNameAliases": {"myNotehead": "noteheadBlack"}},
        )
        self.assertIn("noteheadBlack", result.metadata["glyphsWithAnchors"])
        self.assertTrue(result.report.ok)

    def test_multi_master_default_and_explicit(self):
        glyph = Glyph("noteheadBlack", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 250, 0),
        }, master_id="M1")
        glyph.layers["M2"] = Layer({"stemUpSE": Anchor("stemUpSE", 500, 50)})
        font = make_font(glyphs=[glyph], masters=[Master("M1", "Regular"), Master("M2", "Bold")])

        result = run_export(font, self.tmpdir)
        self.assertEqual(result.metadata["glyphsWithAnchors"]["noteheadBlack"]["stemUpSE"], [1.0, 0.0])
        self.assertTrue(any(i.code == "master-default" for i in result.report.warnings))

        result = run_export(font, self.tmpdir, config={"master": "Bold"})
        self.assertEqual(result.metadata["glyphsWithAnchors"]["noteheadBlack"]["stemUpSE"], [2.0, 0.2])

    def test_master_not_found_is_an_error(self):
        glyph = Glyph("noteheadBlack", "E0A4", {"stemUpSE": Anchor("stemUpSE", 250, 0)})
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir, config={"master": "Nope"})
        self.assertFalse(result.report.ok)
        self.assertIsNone(result.output_path)

    def test_case_mismatch_anchor_warns_and_is_not_exported(self):
        glyph = Glyph("noteheadBlack", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 250, 0),
            "stemupse": Anchor("stemupse", 100, 100),
        })
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir)
        anchors = result.metadata["glyphsWithAnchors"]["noteheadBlack"]
        self.assertIn("stemUpSE", anchors)
        self.assertNotIn("stemupse", anchors)
        self.assertTrue(any(i.code == "anchor-case" for i in result.report.warnings))

    def test_nominal_width_point_anchor_is_not_exported(self):
        glyph = Glyph("gClef", "E050", {
            "nominalWidth": Anchor("nominalWidth", 300, 0),
            "cutOutNE": Anchor("cutOutNE", 100, 100),
        })
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir)
        anchors = result.metadata["glyphsWithAnchors"]["gClef"]
        self.assertNotIn("nominalWidth", anchors)
        self.assertIn("cutOutNE", anchors)
        self.assertTrue(any(i.code == "anchor-scalar" for i in result.report.warnings))

    def test_optional_glyph_and_optional_anchor(self):
        glyph = Glyph("accidentalSharpSmall", "F429", {
            "cutOutNE": Anchor("cutOutNE", 100, 200),
            "cutOutSW": Anchor("cutOutSW", 50, -200),
        })
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir)
        entry = result.metadata["optionalGlyphs"]["accidentalSharpSmall"]
        self.assertEqual(entry["codepoint"], "U+F429")
        self.assertIsInstance(entry.get("classes", []), list)
        self.assertIn("accidentalSharpSmall", result.metadata["glyphsWithAnchors"])
        self.assertTrue(result.report.ok, exporter.format_report(result))

    def test_optional_glyphs_can_be_disabled(self):
        glyph = Glyph("accidentalSharpSmall", "F429", {
            "cutOutNE": Anchor("cutOutNE", 100, 200),
        })
        result = run_export(
            make_font(glyphs=[glyph]), self.tmpdir,
            config={"includeOptionalGlyphs": False},
        )
        self.assertNotIn("optionalGlyphs", result.metadata)
        self.assertNotIn("glyphsWithAnchors", result.metadata)
        self.assertTrue(any(i.code == "optional-anchor-skipped" for i in result.report.warnings))

    def test_canonical_name_unicode_mismatch_warns(self):
        glyph = Glyph("noteheadBlack", "E0A3", {
            "stemUpSE": Anchor("stemUpSE", 250, 0),
        })
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir)
        self.assertTrue(any(i.code == "glyph-codepoint-mismatch" for i in result.report.warnings))
        self.assertIn("noteheadBlack", result.metadata["glyphsWithAnchors"])

    def test_duplicate_mapping_is_an_error(self):
        a = Glyph("noteheadBlack", "E0A4", {"stemUpSE": Anchor("stemUpSE", 250, 0)})
        b = Glyph("myNotehead", "E0A4", {"stemUpSE": Anchor("stemUpSE", 250, 0)})
        result = run_export(
            make_font(glyphs=[a, b]), self.tmpdir,
            config={"glyphNameAliases": {"myNotehead": "noteheadBlack"}},
        )
        self.assertFalse(result.report.ok)
        self.assertTrue(any(i.code == "glyph-duplicate" for i in result.report.errors))
        self.assertIsNone(result.output_path)


# ---------------------------------------------------------------------------
# Font metadata, config, validation and output
# ---------------------------------------------------------------------------

class TestMetadataAndConfig(BaseCase):
    def test_version_conversion_decimal(self):
        font = make_font(glyphs=[], version_major=2, version_minor=1)
        result = run_export(font, self.tmpdir)
        self.assertEqual(result.metadata["fontVersion"], 2.001)

    def test_version_conversion_zero_pads_minor(self):
        font = make_font(glyphs=[], version_major=1, version_minor=5)
        result = run_export(font, self.tmpdir)
        self.assertEqual(result.metadata["fontVersion"], 1.005)

        font = make_font(glyphs=[], version_major=1, version_minor=50)
        result = run_export(font, self.tmpdir)
        self.assertEqual(result.metadata["fontVersion"], 1.05)

    def test_version_conversion_482(self):
        font = make_font(glyphs=[], version_major=1, version_minor=482)
        result = run_export(font, self.tmpdir)
        self.assertEqual(result.metadata["fontVersion"], 1.482)

    def test_canonical_glyph_without_unicode_exports_geometry(self):
        glyph = Glyph("noteheadBlack", None, width=600, bounds=Rect(0, 0, 600, 500))
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir)
        self.assertIn("noteheadBlack", result.metadata["glyphBBoxes"])
        self.assertIn("noteheadBlack", result.metadata["glyphAdvanceWidths"])

    def test_missing_font_name_and_version_aborts(self):
        font = make_font(glyphs=[], family_name="", version_major=None, version_minor=None)
        result = run_export(font, self.tmpdir, write=True)
        self.assertFalse(result.report.ok)
        self.assertIsNone(result.output_path)
        self.assertFalse(os.path.exists(os.path.join(self.tmpdir, "out.json")))
        codes = {i.code for i in result.report.errors}
        self.assertIn("fontName-missing", codes)
        self.assertIn("fontVersion-missing", codes)

    def test_design_size_and_size_range_from_config(self):
        result = run_export(
            make_font(glyphs=[]), self.tmpdir,
            config={"designSize": 120, "sizeRange": [80, 240]},
        )
        self.assertEqual(result.metadata["designSize"], 120)
        self.assertEqual(result.metadata["sizeRange"], [80, 240])
        self.assertTrue(result.report.ok)

    def test_design_size_and_size_range_from_custom_parameters(self):
        font = make_font(glyphs=[], custom_parameters={
            "SMuFL Design Size": 100,
            "SMuFL Size Range": "70 200",
        })
        result = run_export(font, self.tmpdir)
        self.assertEqual(result.metadata["designSize"], 100)
        self.assertEqual(result.metadata["sizeRange"], [70, 200])

    def test_invalid_size_range_aborts(self):
        result = run_export(
            make_font(glyphs=[]), self.tmpdir,
            config={"sizeRange": [240, 80]},
        )
        self.assertFalse(result.report.ok)
        self.assertTrue(any(i.code == "sizeRange-order" for i in result.report.errors))

    def test_engraving_defaults_config(self):
        config = {
            "engravingDefaults": {
                "staffLineThickness": 0.13,
                "stemThickness": 0.12,
                "textFontFamily": ["Academico", "serif"],
            }
        }
        result = run_export(make_font(glyphs=[]), self.tmpdir, config=config)
        self.assertEqual(result.metadata["engravingDefaults"], config["engravingDefaults"])
        self.assertTrue(result.report.ok)

    def test_include_engraving_defaults_can_be_disabled(self):
        result = run_export(
            make_font(glyphs=[]), self.tmpdir,
            config={
                "engravingDefaults": {"stemThickness": 0.1},
                "includeEngravingDefaults": False,
            },
        )
        self.assertTrue(result.report.ok, exporter.format_report(result))
        self.assertNotIn("engravingDefaults", result.metadata)

    def test_unknown_engraving_key_is_an_error(self):
        result = run_export(
            make_font(glyphs=[]), self.tmpdir,
            config={"engravingDefaults": {"notAnEngravingDefault": 1.0}},
        )
        self.assertFalse(result.report.ok)
        self.assertTrue(any(i.code == "schema-engraving-key" for i in result.report.errors))

    def test_text_font_family_must_be_non_empty_strings(self):
        result = run_export(
            make_font(glyphs=[]), self.tmpdir,
            config={"engravingDefaults": {"textFontFamily": ["", 3]}},
        )
        self.assertFalse(result.report.ok)

    def test_unknown_config_key_is_an_error(self):
        result = run_export(
            make_font(glyphs=[]), self.tmpdir,
            config={"engravingDefault": {"stemThickness": 0.1}},
        )
        self.assertFalse(result.report.ok)
        self.assertTrue(any(i.code == "config-keys" for i in result.report.errors))

    def test_manual_anchor_override_and_addition(self):
        glyph = Glyph("noteheadBlack", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 250, 0),
        })
        config = {
            "glyphsWithAnchors": {
                "noteheadBlack": {
                    "stemUpSE": [9.0, 9.0],
                    "opticalCenter": [1.0, 2.0],
                    "nominalWidth": 1.25,
                }
            }
        }
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir, config=config)
        anchors = result.metadata["glyphsWithAnchors"]["noteheadBlack"]
        self.assertEqual(anchors["stemUpSE"], [9.0, 9.0])
        self.assertEqual(anchors["opticalCenter"], [1.0, 2.0])
        self.assertEqual(anchors["nominalWidth"], 1.25)
        self.assertTrue(result.report.ok)

    def test_manual_anchor_for_missing_glyph_is_an_error(self):
        result = run_export(
            make_font(glyphs=[]), self.tmpdir,
            config={"glyphsWithAnchors": {"noteheadBlack": {"stemUpSE": [1.0, 1.0]}}},
        )
        self.assertFalse(result.report.ok)
        self.assertTrue(any(i.code == "manual-anchors-missing" for i in result.report.errors))

    def test_invalid_manual_anchor_value_is_an_error(self):
        glyph = Glyph("noteheadBlack", "E0A4", {"stemUpSE": Anchor("stemUpSE", 250, 0)})
        result = run_export(
            make_font(glyphs=[glyph]), self.tmpdir,
            config={"glyphsWithAnchors": {"noteheadBlack": {"stemUpSE": "nope"}}},
        )
        self.assertFalse(result.report.ok)

    def test_bbox_and_advance_width_opt_in(self):
        glyph = Glyph("noteheadBlack", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 250, 0),
        }, width=600, bounds=Rect(-50, -100, 700, 300))
        result = run_export(
            make_font(glyphs=[glyph]), self.tmpdir,
            config={"includeGlyphBBoxes": True, "includeGlyphAdvanceWidths": True},
        )
        self.assertEqual(result.metadata["glyphBBoxes"]["noteheadBlack"], {
            "bBoxSW": [-0.2, -0.4],
            "bBoxNE": [2.6, 0.8],
        })
        self.assertEqual(result.metadata["glyphAdvanceWidths"]["noteheadBlack"], 2.4)
        self.assertTrue(result.report.ok)

    def test_bbox_and_advance_width_are_on_by_default(self):
        glyph = Glyph("noteheadBlack", "E0A4", {"stemUpSE": Anchor("stemUpSE", 250, 0)})
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir)
        self.assertIn("glyphBBoxes", result.metadata)
        self.assertIn("glyphAdvanceWidths", result.metadata)
        self.assertIn("noteheadBlack", result.metadata["glyphBBoxes"])

    def test_bbox_and_advance_width_can_be_disabled(self):
        glyph = Glyph("noteheadBlack", "E0A4", {"stemUpSE": Anchor("stemUpSE", 250, 0)})
        result = run_export(
            make_font(glyphs=[glyph]), self.tmpdir,
            config={"includeGlyphBBoxes": False, "includeGlyphAdvanceWidths": False},
        )
        self.assertNotIn("glyphBBoxes", result.metadata)
        self.assertNotIn("glyphAdvanceWidths", result.metadata)


class TestValidation(BaseCase):
    def _base(self):
        return {
            "fontName": "Test",
            "fontVersion": 1.0,
            "glyphsWithAnchors": {"noteheadBlack": {"stemUpSE": [1.0, 0.0]}},
        }

    def test_valid_metadata_passes(self):
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        self.assertIsNotNone(names)
        self.assertTrue(exporter.validate_metadata(self._base(), names, set(), report), report.issues)

    def test_bad_anchor_name(self):
        data = self._base()
        data["glyphsWithAnchors"]["noteheadBlack"]["notAnAnchor"] = [1.0, 2.0]
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        exporter.validate_metadata(data, names, set(), report)
        self.assertTrue(any(i.code == "schema-anchor-name" for i in report.errors))

    def test_bad_point(self):
        data = self._base()
        data["glyphsWithAnchors"]["noteheadBlack"]["stemUpSE"] = [1.0]
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        exporter.validate_metadata(data, names, set(), report)
        self.assertTrue(any(i.code == "schema-point" for i in report.errors))

    def test_nan_is_rejected(self):
        data = self._base()
        data["glyphsWithAnchors"]["noteheadBlack"]["stemUpSE"] = [float("nan"), 0.0]
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        exporter.validate_metadata(data, names, set(), report)
        self.assertTrue(any(i.code in ("schema-point", "schema-json") for i in report.errors))

    def test_optional_anchor_requires_declaration(self):
        data = self._base()
        data["glyphsWithAnchors"]["accidentalSharpSmall"] = {"cutOutNE": [1.0, 1.0]}
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        exporter.validate_metadata(data, names, set(), report)
        self.assertTrue(any(i.code == "schema-glyph-name" for i in report.errors))

    def test_optional_glyph_validation(self):
        data = self._base()
        data["optionalGlyphs"] = {
            "accidentalSharpSmall": {"codepoint": "U+F429"},
        }
        data["glyphsWithAnchors"]["accidentalSharpSmall"] = {"cutOutNE": [1.0, 1.0]}
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        self.assertTrue(exporter.validate_metadata(data, names, {"accidentalSharpSmall"}, report), report.issues)

    def test_optional_codepoint_out_of_range(self):
        data = self._base()
        data["optionalGlyphs"] = {"foo": {"codepoint": "U+E000"}}
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        exporter.validate_metadata(data, names, {"foo"}, report)
        self.assertTrue(any(i.code == "schema-optional-range" for i in report.errors))

    def test_bbox_order(self):
        data = self._base()
        data["glyphBBoxes"] = {"noteheadBlack": {"bBoxSW": [2.0, 0.0], "bBoxNE": [1.0, 1.0]}}
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        exporter.validate_metadata(data, names, set(), report)
        self.assertTrue(any(i.code == "schema-bbox-order" for i in report.errors))

    def test_unknown_top_level_key(self):
        data = self._base()
        data["surprise"] = 1
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        exporter.validate_metadata(data, names, set(), report)
        self.assertTrue(any(i.code == "schema-keys" for i in report.errors))


class TestFeatureMetadata(BaseCase):
    def test_alternates_ligatures_and_sets(self):
        base = Glyph("accidentalFlat", "E260", {
            "cutOutNE": Anchor("cutOutNE", 100, 100),
        })
        small = Glyph("accidentalFlatSmall", "F427", width=400)
        left = Glyph("accidentalParensLeft", "E26A", width=200)
        flat = base
        right = Glyph("accidentalParensRight", "E26B", width=200)
        ligature = Glyph("accidentalFlatParens", "F5EA", width=700)
        features = [
            Feature("ss01", "sub accidentalFlat from [accidentalFlatSmall];"),
            Feature("liga", "sub accidentalParensLeft accidentalFlat accidentalParensRight by accidentalFlatParens;"),
        ]
        result = run_export(
            make_font(glyphs=[base, small, left, right, ligature], features=features),
            self.tmpdir,
        )
        self.assertTrue(result.report.ok, exporter.format_report(result))
        self.assertIn("accidentalFlat", result.metadata["glyphsWithAlternates"])
        alt = result.metadata["glyphsWithAlternates"]["accidentalFlat"]["alternates"][0]
        self.assertEqual(alt, {"codepoint": "U+F427", "name": "accidentalFlatSmall"})
        self.assertIn("ss01", result.metadata["sets"])
        self.assertEqual(result.metadata["sets"]["ss01"]["type"], "opticalVariantsSmall")
        self.assertEqual(result.metadata["sets"]["ss01"]["glyphs"][0]["alternateFor"], "accidentalFlat")
        self.assertIn("accidentalFlatParens", result.metadata["ligatures"])
        self.assertEqual(
            result.metadata["ligatures"]["accidentalFlatParens"]["componentGlyphs"],
            ["accidentalParensLeft", "accidentalFlat", "accidentalParensRight"],
        )

    def test_optional_alternate_gets_base_classes(self):
        base = Glyph("accidentalFlat", "E260")
        small = Glyph("accidentalFlatSmall", "F427")
        feature = Feature("ss01", "sub accidentalFlat from [accidentalFlatSmall];")
        result = run_export(make_font(glyphs=[base, small], features=[feature]), self.tmpdir)
        self.assertTrue(result.report.ok, exporter.format_report(result))
        classes = result.metadata["optionalGlyphs"]["accidentalFlatSmall"]["classes"]
        self.assertIn("accidentals", classes)

    def test_sets_template_can_be_overridden(self):
        base = Glyph("accidentalFlat", "E260")
        small = Glyph("accidentalFlatSmall", "F427")
        feature = Feature("ss09", "sub accidentalFlat from [accidentalFlatSmall];")
        result = run_export(
            make_font(glyphs=[base, small], features=[feature]), self.tmpdir,
            config={"setsTemplate": {"ss09": {"type": "timeSigsLargeNarrow", "description": "Test set"}}},
        )
        self.assertTrue(result.report.ok, exporter.format_report(result))
        self.assertEqual(result.metadata["sets"]["ss09"]["type"], "timeSigsLargeNarrow")

    def test_metadata_source_supplies_engraving_defaults(self):
        source_path = os.path.join(self.tmpdir, "source.json")
        with open(source_path, "w", encoding="utf-8") as handle:
            json.dump({
                "engravingDefaults": {
                    "staffLineThickness": 0.1,
                    "textFontFamily": "serif",
                }
            }, handle)
        glyph = Glyph("noteheadBlack", "E0A4", {"stemUpSE": Anchor("stemUpSE", 250, 0)})
        result = run_export(
            make_font(glyphs=[glyph]), self.tmpdir,
            config={"metadataSource": source_path},
        )
        self.assertTrue(result.report.ok, exporter.format_report(result))
        self.assertEqual(result.metadata["engravingDefaults"]["staffLineThickness"], 0.1)
        self.assertEqual(result.metadata["engravingDefaults"]["textFontFamily"], ["serif"])

    def test_unknown_set_template_adds_alternates_without_set(self):
        base = Glyph("accidentalFlat", "E260")
        small = Glyph("accidentalFlatSmall", "F427")
        feature = Feature("ss19", "sub accidentalFlat from [accidentalFlatSmall];")
        result = run_export(make_font(glyphs=[base, small], features=[feature]), self.tmpdir)
        self.assertTrue(result.report.ok, exporter.format_report(result))
        self.assertIn("accidentalFlat", result.metadata["glyphsWithAlternates"])
        self.assertNotIn("sets", result.metadata)
        self.assertTrue(any(i.code == "set-template-missing" for i in result.report.warnings))


class TestNewValidation(BaseCase):
    def _base(self):
        return {
            "fontName": "Test",
            "fontVersion": 1.0,
            "optionalGlyphs": {
                "accidentalFlatSmall": {"codepoint": "U+F427", "classes": []},
                "accidentalFlatParens": {"codepoint": "U+F5EA", "classes": []},
            },
            "glyphsWithAlternates": {
                "accidentalFlat": {"alternates": [{"codepoint": "U+F427", "name": "accidentalFlatSmall"}]}
            },
            "ligatures": {
                "accidentalFlatParens": {
                    "codepoint": "U+F5EA",
                    "componentGlyphs": ["accidentalParensLeft", "accidentalFlat", "accidentalParensRight"],
                }
            },
            "sets": {
                "ss01": {
                    "type": "opticalVariantsSmall",
                    "description": "Small",
                    "glyphs": [{"alternateFor": "accidentalFlat", "codepoint": "U+F427", "name": "accidentalFlatSmall"}],
                }
            },
        }

    def test_valid_new_sections(self):
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        self.assertTrue(exporter.validate_metadata(self._base(), names, set(), report), report.issues)

    def test_bad_alternate_reference(self):
        data = self._base()
        data["glyphsWithAlternates"]["accidentalFlat"]["alternates"][0]["name"] = "notARealGlyph"
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        exporter.validate_metadata(data, names, set(), report)
        self.assertTrue(any(i.code == "schema-alternate-name" for i in report.errors))

    def test_bad_ligature_component(self):
        data = self._base()
        data["ligatures"]["accidentalFlatParens"]["componentGlyphs"] = ["notARealGlyph"]
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        exporter.validate_metadata(data, names, set(), report)
        self.assertTrue(any(i.code == "schema-ligature-component" for i in report.errors))

    def test_bad_set_glyph(self):
        data = self._base()
        data["sets"]["ss01"]["glyphs"][0]["alternateFor"] = "notARealGlyph"
        report = exporter.Report()
        names = exporter.load_glyphnames(ROOT, report=exporter.Report())
        exporter.validate_metadata(data, names, set(), report)
        self.assertTrue(any(i.code == "schema-set-alternateFor" for i in report.errors))


class TestEngravingDefaults(BaseCase):
    def test_staff_line_thickness_is_measured(self):
        # A single staff-line rectangle: 25 font units high, UPM 1000 ->
        # 25 / 250 = 0.1 staff space.
        path = Path([
            Node(0, 0), Node(0, 25), Node(500, 25), Node(500, 0),
        ])
        glyph = Glyph(
            "staff1Line", "E010", width=500,
            bounds=Rect(0, 0, 500, 25), paths=[path],
        )
        result = run_export(make_font(glyphs=[glyph]), self.tmpdir)
        self.assertTrue(result.report.ok, exporter.format_report(result))
        defaults = result.metadata["engravingDefaults"]
        self.assertEqual(defaults["staffLineThickness"], 0.1)
        self.assertEqual(defaults["lyricLineThickness"], 0.1)
        self.assertNotIn("textFontFamily", defaults)


class TestOutput(BaseCase):
    def test_repeatable_output_and_atomic_write(self):
        glyph = Glyph("noteheadBlack", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 304, 55),
        })
        font = make_font(glyphs=[glyph])
        path = os.path.join(self.tmpdir, "out.json")

        first = exporter.run_export(font, path, config_path=None, script_dir=ROOT, report=exporter.Report())
        self.assertTrue(first.report.ok)
        with open(path, "rb") as handle:
            first_bytes = handle.read()

        second = exporter.run_export(font, path, config_path=None, script_dir=ROOT, report=exporter.Report())
        self.assertTrue(second.report.ok)
        with open(path, "rb") as handle:
            second_bytes = handle.read()

        self.assertEqual(first_bytes, second_bytes)
        self.assertTrue(first_bytes.endswith(b"\n"))
        first_bytes.decode("utf-8")
        leftovers = [f for f in os.listdir(self.tmpdir) if f.endswith(".tmp")]
        self.assertEqual(leftovers, [])

    def test_invalid_metadata_does_not_touch_existing_file(self):
        path = os.path.join(self.tmpdir, "out.json")
        with open(path, "wb") as handle:
            handle.write(b"PREVIOUS")
        font = make_font(glyphs=[], family_name="", version_major=None)
        result = exporter.run_export(font, path, config_path=None, script_dir=ROOT, report=exporter.Report())
        self.assertFalse(result.report.ok)
        with open(path, "rb") as handle:
            self.assertEqual(handle.read(), b"PREVIOUS")

    def test_output_is_sorted_and_strict_json(self):
        glyph = Glyph("noteheadBlack", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 304, 55),
        })
        path = os.path.join(self.tmpdir, "out.json")
        result = exporter.run_export(make_font(glyphs=[glyph]), path, config_path=None,
                                     script_dir=ROOT, report=exporter.Report())
        self.assertTrue(result.report.ok)
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        data = json.loads(text)
        expected = [key for key in exporter.TOP_LEVEL_ORDER if key in data]
        self.assertEqual(list(data), expected)
        self.assertEqual(list(data["glyphsWithAnchors"]), sorted(data["glyphsWithAnchors"]))
        self.assertIn('\n  "fontName"', text)


class TestGlyphsEntryPoint(BaseCase):
    def test_main_writes_with_fake_glyphs_module(self):
        import types
        glyph = Glyph("noteheadBlack", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 304, 55),
        })
        font = make_font(glyphs=[glyph])
        path = os.path.join(self.tmpdir, "main-out.json")
        old_module = sys.modules.get("Glyphs")
        old_alert = exporter._show_alert
        old_output = os.environ.get("SMUFL_OUTPUT_PATH")
        sys.modules["Glyphs"] = types.SimpleNamespace(font=font)
        exporter._show_alert = lambda *args, **kwargs: None
        os.environ["SMUFL_OUTPUT_PATH"] = path
        import contextlib
        import io
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exporter.main()
        finally:
            exporter._show_alert = old_alert
            if old_output is None:
                os.environ.pop("SMUFL_OUTPUT_PATH", None)
            else:
                os.environ["SMUFL_OUTPUT_PATH"] = old_output
            if old_module is None:
                sys.modules.pop("Glyphs", None)
            else:
                sys.modules["Glyphs"] = old_module
        self.assertTrue(os.path.isfile(path))
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        self.assertEqual(data["fontName"], "Test Music")
        self.assertIn("noteheadBlack", data["glyphsWithAnchors"])

    def test_main_uses_glyphsapp_application_object(self):
        import types
        glyph = Glyph("noteheadBlack", "E0A4", {
            "stemUpSE": Anchor("stemUpSE", 304, 55),
        })
        font = make_font(glyphs=[glyph])
        path = os.path.join(self.tmpdir, "main-glyphsapp-out.json")
        old_app = sys.modules.get("GlyphsApp")
        old_glyphs = sys.modules.get("Glyphs")
        old_alert = exporter._show_alert
        old_output = os.environ.get("SMUFL_OUTPUT_PATH")
        app_module = types.ModuleType("GlyphsApp")
        app_module.Glyphs = types.SimpleNamespace(font=font)
        sys.modules["GlyphsApp"] = app_module
        sys.modules.pop("Glyphs", None)
        exporter._show_alert = lambda *args, **kwargs: None
        os.environ["SMUFL_OUTPUT_PATH"] = path
        import contextlib
        import io
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exporter.main()
        finally:
            exporter._show_alert = old_alert
            if old_output is None:
                os.environ.pop("SMUFL_OUTPUT_PATH", None)
            else:
                os.environ["SMUFL_OUTPUT_PATH"] = old_output
            if old_app is None:
                sys.modules.pop("GlyphsApp", None)
            else:
                sys.modules["GlyphsApp"] = old_app
            if old_glyphs is not None:
                sys.modules["Glyphs"] = old_glyphs
        self.assertTrue(os.path.isfile(path))
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        self.assertIn("noteheadBlack", data["glyphsWithAnchors"])

    def test_main_handles_no_open_font(self):
        import types
        old_module = sys.modules.get("Glyphs")
        old_alert = exporter._show_alert
        calls = []
        sys.modules["Glyphs"] = types.SimpleNamespace(font=None)
        exporter._show_alert = lambda *args, **kwargs: calls.append(args)
        try:
            exporter.main()
        finally:
            exporter._show_alert = old_alert
            if old_module is None:
                sys.modules.pop("Glyphs", None)
            else:
                sys.modules["Glyphs"] = old_module
        self.assertTrue(calls)


if __name__ == "__main__":
    unittest.main(verbosity=2)
