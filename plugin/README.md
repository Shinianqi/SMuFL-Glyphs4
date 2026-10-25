# 元数据导出器

> 中文为准。[English](README.en.md) · [日本語](README.ja.md)

从 Glyphs 4 的当前工程生成 SMuFL 字体元数据 JSON。

## 两种用法

**A. 插件（推荐）**

双击 `release/pkg/SMuFL-Metadata.pkg`，或把
`release/manual/SMuFL Metadata/SMuFL Metadata.glyphsPlugin` 复制到：

```text
~/Library/Application Support/Glyphs 4/Plugins/
```

pkg 未签名，首次打开的处理步骤见 [`release/README.md`](../release/README.md)。

重启 Glyphs 后，**Script** 菜单里会多出 `Export SMuFL Metadata…`。

**B. 脚本**

把这两个文件放进 `~/Library/Application Support/Glyphs 4/Scripts/`：

```text
plugin/smufl_metadata_exporter.py
data/generated/smufl_glyphnames.json
```

然后按住 Option，选择 **Script → Reload Scripts**（⌘⌥⇧Y），或直接重启 Glyphs。

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

## 字形命名

脚本不会改字形名。Glyphs 通常根据 Unicode 生成 production name（`uniE050`），
导出前确认每个 SMuFL 字形都设了 Unicode；如果流程依赖字形名与码位一致，
按原有步骤改名。

## 配置

不建配置文件、不加自定义参数也能正常导出。只有想覆盖自动测量值、指定母版、
补充别名或手动锚点、关闭某些输出字段时，才用下面两种方式。

### Glyphs 自定义参数

在 Font Info → Font → Custom Parameters 里加：

| 参数 | 值 | 单位 |
|---|---|---|
| `SMuFL Design Size` | 单个正整数 | decipoint（1/720 英寸）；`120` = 12 pt |
| `SMuFL Size Range` | 两个正整数，可写成 `80, 480` 或 `80 480` | decipoint；`80, 480` = 8–48 pt |

两个都是可选的；没有就省略对应的 `designSize` / `sizeRange`。

### 配置文件

复制 `smufl-config.example.json` 成：

```
<工程文件名>.smufl-config.json
```

放在 `.glyphs` 旁边。文件名取工程文件名，不是家族名：

```
Naruto.glyphs          → Naruto.smufl-config.json
Naruto-Regular.glyphs  → Naruto-Regular.smufl-config.json
```

只改需要的键，`null` 表示不覆盖。也可以用 `SMUFL_CONFIG_PATH` 指定其他路径。

配置文件可以覆盖所有键，包括自定义参数做不到的部分：

| 键 | 作用 | 单位 / 示例 |
|---|---|---|
| `fontName` | 覆盖家族名 | `"Naruto"` |
| `fontVersion` | 覆盖版本号 | `1.234` |
| `designSize` | 覆盖优化字号 | decipoint，`120` |
| `sizeRange` | 覆盖字号范围 | `[80, 480]` |
| `master` | 多母版时指定读哪个 | 名称或 ID，`"Regular"` |
| `metadataSource` | 指定旧 JSON 作为回退 | 相对 `.glyphs` 的路径 |
| `engravingDefaults` | 单项覆盖测量值或文本字体 | staff space；`textFontFamily` 是数组 |
| `setsTemplate` | 覆盖 `ssNN` 的 type/description | 见示例 |
| `glyphNameAliases` | 自定义名映射到 SMuFL 名 | `{"myFlat": "accidentalFlat"}` |
| `glyphsWithAnchors` | 手动补/改锚点 | staff space，`[x, y]` |
| `include*` | 关闭某些输出段 | `false` 即不输出 |
| `_comment` | 说明文字 | 导出器忽略 |

`designSize` / `sizeRange` 的优先级：

```
配置文件 > Glyphs 自定义参数 > metadataSource > 不输出
```

两边都填时配置文件赢；配置文件里留 `null`，就走自定义参数。

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

59 个单元测试，使用模拟的 Glyphs 对象模型，不需要安装 Glyphs。

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
