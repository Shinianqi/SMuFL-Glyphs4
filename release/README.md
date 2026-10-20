# 发布包

> 中文为准。[English](README.en.md) · [日本語](README.ja.md)

两个组件各自的安装/卸载 pkg，以及对应的手动安装文件。

| 文件 | 作用 |
|---|---|
| `pkg/SMuFL Glyphs.pkg` | 安装分类表（GlyphData、Groups、图标、筛选器） |
| `pkg/SMuFL Glyphs Uninstall.pkg` | 卸载分类表 |
| `pkg/SMuFL Metadata.pkg` | 安装元数据导出插件 |
| `pkg/SMuFL Metadata Uninstall.pkg` | 卸载元数据导出插件 |

手动安装：

| 目录 | 作用 |
|---|---|
| `manual/SMuFL Glyphs/` | 复制 `Info/`、`Filters/` 到 Glyphs 的 Application Support |
| `manual/SMuFL Metadata/` | 复制 `SMuFL Metadata.glyphsPlugin` 到 `Plugins/` |

## 安装

两个组件互相独立，装哪个都可以。

1. 双击 `SMuFL Glyphs.pkg`，按向导安装；
2. 双击 `SMuFL Metadata.pkg`，按向导安装；
3. ⌘Q 完全退出 Glyphs，再打开。

安装包未签名，首次打开如果被 Gatekeeper 拦截，右键 → 打开。

安装位置：

```text
~/Library/Application Support/Glyphs 4/
```

## 卸载

双击对应的 `Uninstall.pkg`，结束页会显示「卸载完成」，然后重启 Glyphs。

## 版本

1.0.0。
