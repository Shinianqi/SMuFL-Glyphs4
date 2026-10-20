#!/bin/bash
# Development-only installer. End users should use release/pkg/SMuFL Glyphs.pkg
# or release/manual/SMuFL Glyphs/.
#
# Install the SMuFL data files into Glyphs' Application Support folder.
#
#   ./install/install.sh              install into Glyphs 4 (and Glyphs 3 if present)
#   ./install/install.sh --uninstall  remove the files again
#
# Nothing is written outside ~/Library/Application Support/Glyphs */.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA="$ROOT/data/generated"
ICONS="$ROOT/icons"
FILTER="$ROOT/templates/CustomFilterSMuFL.plist"
STAMP="$(date +%Y%m%d%H%M%S)"

DATA_FILES=(GlyphData-SMuFL.xml Groups-SMuFL.plist)
# Left behind by older installations of this data set; removed on uninstall.
LEGACY_FILES=(Groups-SMuFL_Basics.plist)

apps() {
  echo "Glyphs 4"
  if [ -d "$HOME/Library/Application Support/Glyphs 3" ]; then
    echo "Glyphs 3"
  fi
}

if [ "${1:-}" = "--uninstall" ]; then
  while IFS= read -r app; do
    dest="$HOME/Library/Application Support/$app"
    for file in "${DATA_FILES[@]}" "${LEGACY_FILES[@]}"; do
      rm -f "$dest/Info/$file"
    done
    rm -f "$dest/Filters/CustomFilterSMuFL.plist"
    rm -f "$dest/Info/"*.legacy-* 2>/dev/null || true
    rm -f "$dest/Info/Icons/"*Template.svg 2>/dev/null || true
    rmdir "$dest/Info/Icons" "$dest/Info" "$dest/Filters" 2>/dev/null || true
    echo "removed from $app"
  done < <(apps)
  echo "Done. Restart Glyphs."
  exit 0
fi

for file in "${DATA_FILES[@]}"; do
  if [ ! -f "$DATA/$file" ]; then
    echo "missing $DATA/$file - run: python3 tools/build_all.py" >&2
    exit 1
  fi
done

while IFS= read -r app; do
  dest="$HOME/Library/Application Support/$app"
  mkdir -p "$dest/Info/Icons" "$dest/Filters"

  # Older releases shipped a second, hand-curated group file.  Move it out of
  # the way (a ".legacy-" suffix stops Glyphs from loading it) so the sidebar
  # does not show two competing SMuFL entries.
  for file in "${LEGACY_FILES[@]}"; do
    if [ -f "$dest/Info/$file" ]; then
      mv "$dest/Info/$file" "$dest/Info/$file.legacy-$STAMP"
      echo "  moved legacy $file aside ($file.legacy-$STAMP)"
    fi
  done

  for file in "${DATA_FILES[@]}"; do
    if [ -f "$dest/Info/$file" ] && ! cmp -s "$DATA/$file" "$dest/Info/$file"; then
      cp "$dest/Info/$file" "$dest/Info/$file.bak-$STAMP"
    fi
    cp "$DATA/$file" "$dest/Info/$file"
  done

  # Refresh only the icons we ship; leave any other artwork alone.
  for icon in "$ICONS"/*Template.*; do
    [ -e "$icon" ] && cp "$icon" "$dest/Info/Icons/"
  done
  cp "$FILTER" "$dest/Filters/CustomFilterSMuFL.plist"

  echo "installed into $dest"
done < <(apps)

echo
echo "Done. Quit Glyphs completely (Cmd-Q) and reopen it."
