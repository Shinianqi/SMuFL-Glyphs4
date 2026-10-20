#!/bin/bash
# Assemble the Glyphs 4 plugin bundle in build/.
#
#   ./plugin/build.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(cat "$ROOT/VERSION")"
OUT="$ROOT/build/SMuFL Metadata.glyphsPlugin"

if [ ! -f "$ROOT/data/generated/smufl_glyphnames.json" ]; then
  echo "missing generated data - run: python3 tools/build_all.py" >&2
  exit 1
fi

rm -rf "$OUT"
mkdir -p "$OUT"
cp -R "$ROOT/plugin/bundle/Contents" "$OUT/Contents"

RES="$OUT/Contents/Resources"
cp "$ROOT/plugin/smufl_metadata_exporter.py" "$RES/"
cp "$ROOT/data/generated/smufl_glyphnames.json" "$RES/"
cp "$ROOT/plugin/smufl_optional_reference.json" "$RES/"
cp "$ROOT/plugin/smufl_sets_template.json" "$RES/"

/usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString $VERSION" \
  "$OUT/Contents/Info.plist" >/dev/null

xattr -cr "$OUT" 2>/dev/null || true
find "$OUT" -name '._*' -delete
echo "built $OUT"
