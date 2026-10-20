# 锚点

> 中文为准。[English](ANCHORS.en.md) · [日本語](ANCHORS.ja.md)

`GlyphData` 的 `anchors` 属性支持带位置的锚点：

```xml
<glyph name="ogonek" anchors="ogonek@maxX;baseline" .../>
```

语法是 `名字@x表达式;y表达式`，逗号分隔多个。变量：

| 变量 | 含义 |
|---|---|
| `minX` / `maxX` / `width` / `centerX` | 水平 |
| `minY` / `maxY` / `height` / `centerY` | 垂直 |
| `baseline` / `ascender` / `descender` / `xHeight` / `capHeight` | 垂直度量 |

## 用法

![添加锚点](images/anchors.gif)

Glyphs **不会**在新建字形时写入锚点，而是在执行
**Glyph > Set Anchors（⌘U）** 时应用。不需要锚点时不要按 ⌘U，字形保持干净。

## 数据来源

| 文件 | 内容 |
|---|---|
| `data/layout/anchors.glyphs.json` | 逐字形锚点：从 Bravura 1.482 的 `glyphsWithAnchors` + `glyphBBoxes` 归一化为表达式，586 个字形 |
| `data/layout/anchors.json` | 按 range 的兜底规则：Dynamics、音符类、变音记号、Multi-segment lines |

生成时优先用逐字形数据，没有才用 range 规则。当前共 1,016 个字形带锚点，覆盖
`stemUpSE`、`stemDownNW`、`splitStem*`、`cutOut*`、`noteheadOrigin`、
`opticalCenter`、`repeatOffset`、`graceNoteSlash*` 等。

坐标是从 Bravura 的 staff space 坐标按字形包围盒归一化到 `minX/centerX/maxX` 和
`minY/centerY/maxY/baseline` 得到的，属于近似值，需要时手动微调。

## 修改

- 单个字形：改 `anchors.glyphs.json` 的 `glyphs` 条目。
- 整类字形：改 `anchors.json` 的 `rules`，`ranges` 用 `data/upstream/ranges.json` 的键。

```bash
python3 tools/build_all.py
```
