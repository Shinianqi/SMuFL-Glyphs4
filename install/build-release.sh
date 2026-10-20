#!/bin/bash
# Build release/pkg/*.pkg and release/manual/*.
#
#   ./install/build-release.sh
#
# Requires macOS pkgbuild/productbuild and the generated data.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(cat "$ROOT/VERSION")"
REL="$ROOT/release"
PKG="$REL/pkg"
MAN="$REL/manual"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

DATA_ID="com.shinianqi.smuflglyphs"
PLUGIN_ID="com.shinianqi.smuflmetadata"

if [ ! -f "$ROOT/data/generated/Groups-SMuFL.plist" ]; then
  echo "missing generated data - run: python3 tools/build_all.py" >&2
  exit 1
fi

rm -rf "$PKG" "$MAN"
mkdir -p "$PKG" "$MAN/SMuFL Glyphs" "$MAN/SMuFL Metadata"

# ---------------------------------------------------------------- manual data
cp -R "$ROOT/data/generated" "$MAN/SMuFL Glyphs/Info"
rm -f "$MAN/SMuFL Glyphs/Info/smufl_glyphnames.json"
mkdir -p "$MAN/SMuFL Glyphs/Info/Icons" "$MAN/SMuFL Glyphs/Filters"
cp "$ROOT"/icons/*Template.svg "$MAN/SMuFL Glyphs/Info/Icons/"
cp "$ROOT/templates/CustomFilterSMuFL.plist" "$MAN/SMuFL Glyphs/Filters/"
cp "$ROOT/install/templates/manual-glyphs/"README*.md "$MAN/SMuFL Glyphs/"

# -------------------------------------------------------------- manual plugin
bash "$ROOT/plugin/build.sh" >/dev/null
cp -R "$ROOT/build/SMuFL Metadata.glyphsPlugin" "$MAN/SMuFL Metadata/"
cp "$ROOT/plugin/smufl-config.example.json" "$MAN/SMuFL Metadata/"
cp "$ROOT/plugin/install_pyobjc.command" "$MAN/SMuFL Metadata/"
cp "$ROOT/install/templates/manual-metadata/"README*.md "$MAN/SMuFL Metadata/"

USER_HOME_SNIPPET='USER_NAME="$(stat -f%Su /dev/console)"
[ "$USER_NAME" = "root" ] && USER_NAME="$(ls -l /dev/console | awk "{print \$3}")"
HOME_DIR="$(dscl . -read "/Users/$USER_NAME" NFSHomeDirectory 2>/dev/null | awk "{print \$2}")"
[ -n "$HOME_DIR" ] || HOME_DIR="/Users/$USER_NAME"'

# ------------------------------------------------------- SMuFL-Glyphs.pkg
mkdir -p "$WORK/glyphs/private/tmp/smufl-glyphs-payload"
cp -R "$MAN/SMuFL Glyphs/Info" "$WORK/glyphs/private/tmp/smufl-glyphs-payload/Info"
cp -R "$MAN/SMuFL Glyphs/Filters" "$WORK/glyphs/private/tmp/smufl-glyphs-payload/Filters"

mkdir -p "$WORK/glyphs-scripts"
cat > "$WORK/glyphs-scripts/postinstall" <<EOF
#!/bin/bash
set -e
PAYLOAD="/private/tmp/smufl-glyphs-payload"
$USER_HOME_SNIPPET
for APP in "Glyphs 4" "Glyphs 3"; do
  DEST="\$HOME_DIR/Library/Application Support/\$APP"
  if [ "\$APP" = "Glyphs 3" ] && [ ! -d "\$DEST" ]; then continue; fi
  mkdir -p "\$DEST/Info/Icons" "\$DEST/Filters"
  if [ -e "\$DEST/Info/Groups-SMuFL_Basics.plist" ]; then
    mv "\$DEST/Info/Groups-SMuFL_Basics.plist" \\
       "\$DEST/Info/Groups-SMuFL_Basics.plist.legacy-\$(date +%Y%m%d%H%M%S)"
  fi
  cp -R "\$PAYLOAD/Info/." "\$DEST/Info/"
  cp -R "\$PAYLOAD/Filters/." "\$DEST/Filters/"
  chown -R "\$USER_NAME" "\$DEST/Info" "\$DEST/Filters" 2>/dev/null || true
  echo "installed to \$DEST"
done
rm -rf "\$PAYLOAD"
exit 0
EOF
chmod +x "$WORK/glyphs-scripts/postinstall"

pkgbuild --root "$WORK/glyphs" \
         --identifier "$DATA_ID" \
         --version "$VERSION" \
         --scripts "$WORK/glyphs-scripts" \
         --install-location "/" \
         --ownership recommended \
         "$WORK/glyphs.pkg" >/dev/null
productbuild --package "$WORK/glyphs.pkg" "$PKG/SMuFL-Glyphs.pkg" >/dev/null
echo "built release/pkg/SMuFL-Glyphs.pkg"

# --------------------------------------------- SMuFL-Glyphs-Uninstall.pkg
ICON_LIST="$(cd "$ROOT/icons" && ls *Template.svg | tr '\n' ' ')"
mkdir -p "$WORK/glyphs-uninstall"
cat > "$WORK/glyphs-uninstall/postinstall" <<EOF
#!/bin/bash
set -e
$USER_HOME_SNIPPET
for APP in "Glyphs 4" "Glyphs 3"; do
  DEST="\$HOME_DIR/Library/Application Support/\$APP"
  [ -d "\$DEST" ] || continue
  rm -f "\$DEST/Info/GlyphData-SMuFL.xml"
  rm -f "\$DEST/Info/Groups-SMuFL.plist"
  rm -f "\$DEST/Info/Groups-SMuFL_Basics.plist"
  rm -f "\$DEST/Info/Groups-SMuFL_Basics.plist.legacy-"*
  rm -f "\$DEST/Filters/CustomFilterSMuFL.plist"
  for icon in $ICON_LIST; do
    rm -f "\$DEST/Info/Icons/\$icon"
  done
  rmdir "\$DEST/Info/Icons" "\$DEST/Info" "\$DEST/Filters" 2>/dev/null || true
  echo "removed from \$DEST"
done
exit 0
EOF
chmod +x "$WORK/glyphs-uninstall/postinstall"
pkgbuild --nopayload \
         --identifier "$DATA_ID.uninstall" \
         --version "$VERSION" \
         --scripts "$WORK/glyphs-uninstall" \
         "$WORK/glyphs-uninstall.pkg" >/dev/null
mkdir -p "$WORK/uninstall-glyphs-res"
cat > "$WORK/uninstall-glyphs-res/conclusion.html" <<'HTML'
<html><head><meta charset="utf-8"></head><body>
<h2>卸载完成</h2>
<p>SMuFL Glyphs 已从 Glyphs 的 Application Support 目录移除。</p>
<p>请完全退出 Glyphs（⌘Q）后重新打开。</p>
</body></html>
HTML
cat > "$WORK/glyphs-uninstall/Distribution" <<EOF
<?xml version="1.0" encoding="utf-8"?>
<installer-gui-script minSpecVersion="2">
    <title>卸载 SMuFL Glyphs</title>
    <organization>com.shinianqi</organization>
    <domains enable_localSystem="true" enable_currentUserHome="false" enable_anywhere="false"/>
    <options customize="never" require-scripts="true"/>
    <conclusion file="conclusion.html" mime-type="text/html"/>
    <choices-outline><line choice="default"/></choices-outline>
    <choice id="default" title="卸载 SMuFL Glyphs" visible="false">
        <pkg-ref id="$DATA_ID.uninstall"/>
    </choice>
    <pkg-ref id="$DATA_ID.uninstall" version="$VERSION">glyphs-uninstall.pkg</pkg-ref>
</installer-gui-script>
EOF
productbuild --distribution "$WORK/glyphs-uninstall/Distribution" \
             --resources "$WORK/uninstall-glyphs-res" \
             --package-path "$WORK" \
             "$PKG/SMuFL-Glyphs-Uninstall.pkg" >/dev/null
echo "built release/pkg/SMuFL-Glyphs-Uninstall.pkg"

# ----------------------------------------------------- SMuFL-Metadata.pkg
mkdir -p "$WORK/plugin/private/tmp/smufl-metadata-payload"
cp -R "$ROOT/build/SMuFL Metadata.glyphsPlugin" \
      "$WORK/plugin/private/tmp/smufl-metadata-payload/"
mkdir -p "$WORK/plugin-scripts"
cat > "$WORK/plugin-scripts/postinstall" <<EOF
#!/bin/bash
set -e
PAYLOAD="/private/tmp/smufl-metadata-payload"
$USER_HOME_SNIPPET
DEST="\$HOME_DIR/Library/Application Support/Glyphs 4/Plugins"
mkdir -p "\$DEST"
rm -rf "\$DEST/SMuFL Metadata.glyphsPlugin"
cp -R "\$PAYLOAD/SMuFL Metadata.glyphsPlugin" "\$DEST/"
chown -R "\$USER_NAME" "\$DEST" 2>/dev/null || true
rm -rf "\$PAYLOAD"
echo "installed to \$DEST"
exit 0
EOF
chmod +x "$WORK/plugin-scripts/postinstall"
pkgbuild --root "$WORK/plugin" \
         --identifier "$PLUGIN_ID" \
         --version "$VERSION" \
         --scripts "$WORK/plugin-scripts" \
         --install-location "/" \
         --ownership recommended \
         "$WORK/plugin.pkg" >/dev/null
productbuild --package "$WORK/plugin.pkg" "$PKG/SMuFL-Metadata.pkg" >/dev/null
echo "built release/pkg/SMuFL-Metadata.pkg"

# ------------------------------------------- SMuFL-Metadata-Uninstall.pkg
mkdir -p "$WORK/plugin-uninstall"
cat > "$WORK/plugin-uninstall/postinstall" <<EOF
#!/bin/bash
set -e
$USER_HOME_SNIPPET
DEST="\$HOME_DIR/Library/Application Support/Glyphs 4/Plugins/SMuFL Metadata.glyphsPlugin"
rm -rf "\$DEST"
echo "removed \$DEST"
exit 0
EOF
chmod +x "$WORK/plugin-uninstall/postinstall"
pkgbuild --nopayload \
         --identifier "$PLUGIN_ID.uninstall" \
         --version "$VERSION" \
         --scripts "$WORK/plugin-uninstall" \
         "$WORK/plugin-uninstall.pkg" >/dev/null
mkdir -p "$WORK/uninstall-plugin-res"
cat > "$WORK/uninstall-plugin-res/conclusion.html" <<'HTML'
<html><head><meta charset="utf-8"></head><body>
<h2>卸载完成</h2>
<p>SMuFL Metadata 插件已从 Glyphs 的 Plugins 目录移除。</p>
<p>请完全退出 Glyphs（⌘Q）后重新打开。</p>
</body></html>
HTML
cat > "$WORK/plugin-uninstall/Distribution" <<EOF
<?xml version="1.0" encoding="utf-8"?>
<installer-gui-script minSpecVersion="2">
    <title>卸载 SMuFL Metadata</title>
    <organization>com.shinianqi</organization>
    <domains enable_localSystem="true" enable_currentUserHome="false" enable_anywhere="false"/>
    <options customize="never" require-scripts="true"/>
    <conclusion file="conclusion.html" mime-type="text/html"/>
    <choices-outline><line choice="default"/></choices-outline>
    <choice id="default" title="卸载 SMuFL Metadata" visible="false">
        <pkg-ref id="$PLUGIN_ID.uninstall"/>
    </choice>
    <pkg-ref id="$PLUGIN_ID.uninstall" version="$VERSION">plugin-uninstall.pkg</pkg-ref>
</installer-gui-script>
EOF
productbuild --distribution "$WORK/plugin-uninstall/Distribution" \
             --resources "$WORK/uninstall-plugin-res" \
             --package-path "$WORK" \
             "$PKG/SMuFL-Metadata-Uninstall.pkg" >/dev/null
echo "built release/pkg/SMuFL-Metadata-Uninstall.pkg"

echo
echo "release/"
ls -1 "$PKG"
ls -1 "$MAN"
