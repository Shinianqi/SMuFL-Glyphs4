# SMuFL Metadata 手动安装

> 中文为准。[English](README.en.md) · [日本語](README.ja.md)

字体元数据导出插件。分类表在 `release/manual/SMuFL Glyphs/`。

## 安装

1. ⌘Q 完全退出 Glyphs。
2. 把 `SMuFL Metadata.glyphsPlugin` 复制到：

```text
~/Library/Application Support/Glyphs 4/Plugins/
```

3. 重新打开 Glyphs。

**Script** 菜单里会出现 `Export SMuFL Metadata…`。

## 使用

1. 打开一个 `.glyphs` 工程。
2. 运行 **Script > Export SMuFL Metadata…**。
3. 在保存面板里选择输出位置，默认是工程同目录的 `<字体名>.json`。

输出 SMuFL 的 `engravingDefaults`、`glyphAdvanceWidths`、`glyphsWithAnchors`、
`glyphBBoxes`、`glyphsWithAlternates`、`ligatures`、`sets`、`optionalGlyphs`。
不会修改 `.glyphs` 工程。

### 配置

把 `smufl-config.example.json` 复制成工程旁边的
`<字体文件名>.smufl-config.json`，按需修改。所有键都是可选的。

### 用脚本版代替

把 `smufl_metadata_exporter.py` 和 `smufl_glyphnames.json` 放进：

```text
~/Library/Application Support/Glyphs 4/Scripts/
```

然后按住 Option，选择 **Script → Reload Scripts**（⌘⌥⇧Y），或直接重启 Glyphs。

## 卸载

退出 Glyphs，删除：

```text
~/Library/Application Support/Glyphs 4/Plugins/SMuFL Metadata.glyphsPlugin
```

## 依赖

插件运行在 Glyphs 自带的 Python 里，需要 PyObjC。缺少时运行
`install_pyobjc.command`，或参考其中的手动命令；装完 ⌘Q 重启。
