# 测试说明

> 中文为准。[English](README.en.md) · [日本語](README.ja.md)

## 1. 单元测试（不需要安装 Glyphs）

```bash
cd ..
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

测试会注入一个很小的 Glyphs 4 对象模型模拟层
（`font.masters`、`glyph.layerForId_()`、`layer.anchors`、`anchor.position`、
`layer.bounds`、`layer.width`、`font.features` 等），不需要 PyObjC 或 Glyphs。

`SMUFL_EXPORTER_NO_MAIN=1` 用于阻止导入脚本时自动执行 Glyphs 菜单入口。

当前共有 **57 个测试**，覆盖：

- staff space 换算（UPM 1000 / 2048）；
- 规范名、别名、Unicode 兜底、拒绝乱猜；
- 多母版策略；
- 可选字形、classes、description；
- `salt`/`ssNN` 替代字形、`ssNN` 样式集、`liga` 连字；
- `engravingDefaults` / `designSize` / `sizeRange` 配置与 `metadataSource`；
- BBox/advance width 默认开启及关闭；
- 新字段校验、NaN、重复、未知键；
- 原子写、重复运行、失败不覆盖；
- 模拟 Script 菜单入口。

## 2. 可选的真实字体无界面验证（需要 Glyphs 4 + PyObjC）

```bash
python3 -m venv .venv
.venv/bin/pip install pyobjc-framework-Cocoa

.venv/bin/python tests/headless_glyphs4.py \
  "/path/to/YourFont.glyphs" \
  /tmp/YourFont.json \
  --report /tmp/YourFont_report.txt
```

工具只把 `GSApplication` 替换成桩（它位于 Glyphs 可执行文件，不在框架中），
这样 `GlyphsApp` 模块才能导入；`GSFont`、`GSGlyph`、`GSLayer`、`GSAnchor`、
`layer.bounds` 等都是 GlyphsCore 4.2 的真实类。字体只读打开，不会保存。

这个工具只是开发/验证辅助；正式的 Glyphs 脚本不需要额外安装 PyObjC，
Glyphs 自带的 Python 环境已经提供 AppKit。

## 3. 样例

本仓库不附带样例字体（`Naruto_SMuFL.glyphs` 不在开源范围内）。想验证时用
你自己的工程跑上面的无界面命令即可。
