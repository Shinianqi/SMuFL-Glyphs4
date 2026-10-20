# Changelog

> 中文为准。[English](CHANGELOG.en.md) · [日本語](CHANGELOG.ja.md)

## 1.0.0 — 2026-10-20

### 分类表

- 从 SMuFL 1.5 (draft) 官方元数据（`w3c-cg/smufl`，commit `f9d12b2`）生成：
  `GlyphData-SMuFL.xml`（2,940 字形）、`Groups-SMuFL.plist`。
- 侧边栏：`SMuFL Glyphs`（Classes A-Z 85 + Ranges A-Z 132）、
  `SMuFL Common Glyphs`（12 组，969 字形）。
- `Ornaments & Lines` 下含 Trills、Arpeggios、Glissando、Combining Strokes。
- 启动窗口 5 个入口：`SMuFL Common Glyphs`、`SMuFL Glyphs`、`Clefs`、
  `Time Signatures`、`Notes & Rests`。
- 字形按 Unicode 码位排序；两个数字开头的字形名改为 Glyphs 可接受的拼写。
- 3 个自定义筛选器（Core / Optional / Unicode Music Symbols）。
- 分组结构在 `data/layout/legacy.json`，只存名字和 range/class 引用。

### 锚点

- 执行 ⌘U 时写入。
- 1,016 个字形带锚点：
  - `data/layout/anchors.glyphs.json`：从 Bravura 1.482 的
    `glyphsWithAnchors`/`glyphBBoxes` 归一化的逐字形锚点（586 个）；
  - `data/layout/anchors.json`：按 range 的兜底（Dynamics、音符类、变音记号、
    多段线）。

### 导出器

- 生成 SMuFL 字体元数据 JSON：`engravingDefaults`、`glyphAdvanceWidths`、
  `glyphsWithAnchors`、`glyphBBoxes`、`glyphsWithAlternates`、`ligatures`、
  `sets`、`optionalGlyphs`。
- 插件版和脚本版共用同一套导出核心。

### 发布

- `release/pkg/`：`SMuFL Glyphs`、`SMuFL Metadata` 及各自的 `Uninstall` 共 4 个 pkg。
- `release/manual/`：两个组件的免 pkg 安装文件。
- 生成命令 `./install/build-release.sh`。

### 工程

- 生成、校验、发布构建脚本；13 个来自 Naruto 字体的图标。
- Apache-2.0；Bravura 参考数据为 OFL-1.1。
