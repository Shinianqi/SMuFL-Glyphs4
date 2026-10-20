# 元数据导出器

> 中文为准。[English](README.en.md) · [日本語](README.ja.md)

从 Glyphs 4 的当前工程生成 SMuFL 字体元数据 JSON。

## 两种用法

**A. 插件（推荐）**

双击 `release/pkg/SMuFL Metadata.pkg`，或把
`release/manual/SMuFL Metadata/SMuFL Metadata.glyphsPlugin` 复制到：

```text
~/Library/Application Support/Glyphs 4/Plugins/
```

重启 Glyphs 后，**Script** 菜单里会多出 `Export SMuFL Metadata…`。

**B. 脚本**

把这两个文件放进 `~/Library/Application Support/Glyphs 4/Scripts/`：

```text
plugin/smufl_metadata_exporter.py
data/generated/smufl_glyphnames.json
```

然后 **Script → Reload Scripts**。

两种方式都需要 Glyphs 自带的 Python 能 import PyObjC。缺的话运行
`plugin/install_pyobjc.command`（或参考该文件里的手动命令），装完 ⌘Q 重启。

## 输出

默认写到 `.glyphs` 文件同目录的 `<字体名>.json`。字段：

| 字段 | 来源 | 默认 |
|---|---|---|
| `fontName` / `fontVersion` | 字体信息，可覆盖 | 必填 |
| `designSize` / `sizeRange` | 配置或 Glyphs 自定义参数 | 可选 |
| `engravingDefaults` | 从轮廓/节点测量（29 项） | 自动 |
| `glyphAdvanceWidths` | `layer.width / (upm/4)` | 开 |
| `glyphsWithAnchors` | 母版层的 SMuFL 锚点 | 开 |
| `glyphBBoxes` | `layer.bounds / (upm/4)` | 开 |
| `glyphsWithAlternates` | `salt` / `ssNN` / `cvNN` | 开 |
| `ligatures` | `liga` / `dlig` / `clig` / `rlig` | 开 |
| `sets` | `ssNN` + `smufl_sets_template.json` | 开 |
| `optionalGlyphs` | U+F400–U+F8FF | 开 |

写入是原子的：失败时不会留下半个文件，也不会改动 `.glyphs` 工程。

## 配置

把 `smufl-config.example.json` 复制成 `.glyphs` 旁边的
`<字体文件名>.smufl-config.json`（例如 `MyFont.smufl-config.json`），
按需覆盖。所有键都是可选的。

## 数据文件

| 文件 | 作用 | 许可 |
|---|---|---|
| `smufl_metadata_exporter.py` | 导出核心 | Apache-2.0 |
| `data/generated/smufl_glyphnames.json` | 规范字形名/码位/描述/classes | Apache-2.0 + SMuFL 署名 |
| `smufl_optional_reference.json` | 可选字形的描述/classes 参考 | **OFL-1.1** |
| `smufl_sets_template.json` | `ssNN` 样式集模板 | **OFL-1.1** |

导出器也接受未经合并的官方 `glyphnames.json`（`SMUFL_GLYPHNAMES_PATH`
环境变量可指定路径），但那样 `optionalGlyphs[].classes` 会是空数组。

## 测试

```bash
cd plugin
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

57 个单元测试，使用模拟的 Glyphs 对象模型，不需要安装 Glyphs。

真实字体的无界面验证见 `tests/README.md`。

## 与 Glyphs 的字形名差异

Glyphs 不接受以数字开头的字形名，所以数据表里：

```text
4stringTabClef -> fourStringTabClef
6stringTabClef -> sixStringTabClef
```

导出器会在内部把这两个名字映射回 SMuFL 规范名，输出 JSON 里仍然是规范名。
`unicode` / `production` 不受影响。

## 许可

导出器本体 Apache-2.0。插件启动器（`bundle/Contents/MacOS/`）来自
GlyphsSDK，Apache-2.0。两个参考 JSON 是 OFL-1.1，不要把它们的版权头改掉。
见仓库根目录的 `NOTICE`。
