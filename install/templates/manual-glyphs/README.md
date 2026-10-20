# SMuFL Glyphs 手动安装

> 中文为准。[English](README.en.md) · [日本語](README.ja.md)

分类表（GlyphData、Groups、图标、筛选器）。插件版在
`release/manual/SMuFL Metadata/`。

## 安装

1. ⌘Q 完全退出 Glyphs。
2. 把本目录下的 `Info` 和 `Filters` 复制到：

```text
~/Library/Application Support/Glyphs 4/
```

结果应为：

```text
~/Library/Application Support/Glyphs 4/
├── Filters/
│   └── CustomFilterSMuFL.plist
└── Info/
    ├── GlyphData-SMuFL.xml
    ├── Groups-SMuFL.plist
    └── Icons/
        └── *Template.svg
```

3. 重新打开 Glyphs。

如果已经有自己的 `GlyphData-*.xml` 或 `Groups-*.plist`，逐个文件复制，
不要整个文件夹覆盖。

## 使用

- 侧边栏出现 `SMuFL Glyphs` 和 `SMuFL Common Glyphs`。
- 启动窗口的「预创建字形」有 5 个入口。
- 字形按 Unicode 码位排序。

锚点需要手动应用：选中字形后执行 **Glyph > Set Anchors（⌘U）**。
`Dynamics` 会得到 `opticalCenter`，音符类字形会得到 `stemUpSE`、`stemDownNW`、
`splitStemUpSE`、`splitStemDownNW`。

## 卸载

退出 Glyphs，删除：

```text
~/Library/Application Support/Glyphs 4/Info/GlyphData-SMuFL.xml
~/Library/Application Support/Glyphs 4/Info/Groups-SMuFL.plist
~/Library/Application Support/Glyphs 4/Info/Icons/*Template.svg
~/Library/Application Support/Glyphs 4/Filters/CustomFilterSMuFL.plist
```

## 常见问题

- **侧边栏没有出现**：确认文件在 `Application Support/Glyphs 4/Info/` 下，
  而不是 `Glyphs 4/Info/Info/`。
- **提示 `Invalid filter in sidebar`**：删除 `Filters/CustomFilterSMuFL.plist` 再试。
- **Glyphs 启动报错**：删掉刚复制的文件，确认 XML/plist 没有被编辑器改坏。
