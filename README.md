# SMuFL for Glyphs 4

> 文档以中文为准。[English](README.en.md) · [日本語](README.ja.md)

Glyphs 4 是一款 macOS 应用。本仓库提供它的 SMuFL 分类表和字体元数据导出插件；数据来自 SMuFL 1.5 (draft) 官方元数据。安装器同时兼容 Glyphs 3 的目录结构。

## 截图

启动窗口（5 个预创建入口）：

![启动窗口](docs/images/startup.png)

侧边栏（两个分类）：

![侧边栏](docs/images/sidebar.png)

## 分类表

| 项目 | 数量 |
|---|---|
| 字形 | 2,940 |
| classes | 85 |
| ranges | 132 |
| 侧边栏分类 | `SMuFL Glyphs`、`SMuFL Common Glyphs` |
| 启动窗口入口 | 5 |

```text
SMuFL Glyphs
├── Classes A-Z
└── Ranges A-Z

SMuFL Common Glyphs
├── Staff Structure
├── Clefs & Octaves
├── Notes & Rests
├── Accidentals
├── Time Signatures
├── Repetitions
├── Dynamics
├── Articulations
├── Holds & Pauses
├── Ornaments & Lines
├── Techniques
└── Signs & Texts
```

启动窗口：`SMuFL Common Glyphs`（969）、`SMuFL Glyphs`（2,940）、`Clefs`（61）、
`Time Signatures`（32）、`Notes & Rests`（212）。字形按 Unicode 码位排序。

锚点：选中字形后执行 **Glyph > Set Anchors（⌘U）**，会写入
`opticalCenter`（Dynamics）以及 `stemUpSE`、`stemDownNW` 等（音符类）。
详见 [`docs/ANCHORS.md`](docs/ANCHORS.md)。

### 安装

用 `release/pkg/` 里的安装包：

| 包 | 作用 |
|---|---|
| `SMuFL Glyphs.pkg` | 安装分类表 |
| `SMuFL Glyphs Uninstall.pkg` | 卸载分类表 |
| `SMuFL Metadata.pkg` | 安装导出插件 |
| `SMuFL Metadata Uninstall.pkg` | 卸载导出插件 |

装完 ⌘Q 退出 Glyphs 再打开。手动安装和详细说明见 [`release/README.md`](release/README.md)。

## 导出器

从 Glyphs 4 的 Script 菜单运行，生成 SMuFL 字体元数据 JSON：
`fontName`、`fontVersion`、`designSize`、`sizeRange`、`engravingDefaults`、
`glyphAdvanceWidths`、`glyphsWithAnchors`、`glyphBBoxes`、`glyphsWithAlternates`、
`ligatures`、`sets`、`optionalGlyphs`。不修改 `.glyphs` 工程。

安装：双击 `release/pkg/SMuFL Metadata.pkg`，或把
`release/manual/SMuFL Metadata/SMuFL Metadata.glyphsPlugin` 复制到：

```text
~/Library/Application Support/Glyphs 4/Plugins/
```

配置见 [`plugin/README.md`](plugin/README.md)。

## 重建

```bash
python3 tools/build_all.py
./install/build-release.sh
```

只依赖 Python 标准库。侧边栏结构在
[`data/layout/legacy.json`](data/layout/legacy.json)，只存分组名和 range/class 引用；
锚点规则在 [`data/layout/anchors.json`](data/layout/anchors.json)。
详见 [`docs/BUILD.md`](docs/BUILD.md)。

## 许可

Apache-2.0，见 [`LICENSE`](LICENSE)。第三方署名在 [`NOTICE`](NOTICE)：
SMuFL 规范（FSA）、GlyphsSDK（Apache-2.0）、Bravura（OFL-1.1，仅两个参考 JSON）。

## 致谢

[SMuFL](https://www.w3.org/community/music-notation/)、
[GlyphsSDK](https://github.com/schriftgestalt/GlyphsSDK)、
[Bravura](https://github.com/steinbergmedia/bravura)。
