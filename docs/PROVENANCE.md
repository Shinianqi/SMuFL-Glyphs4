# 文件来源

> 中文为准。[English](PROVENANCE.en.md) · [日本語](PROVENANCE.ja.md)

| 路径 | 来源 |
|---|---|
| `data/upstream/*.json` | `w3c-cg/smufl` 的 `metadata/`，commit `f9d12b2` |
| `data/layout/legacy.json` | 分组结构（名字 + range/class 引用） |
| `data/layout/anchors.json` | 按 range 的锚点兜底规则 |
| `data/layout/anchors.glyphs.json` | 从 Bravura 的 `glyphsWithAnchors`/`glyphBBoxes` 归一化的逐字形锚点 |
| `data/generated/*` | `tools/` 生成 |
| `tools/*`、`install/*`、`templates/*` | 本项目 |
| `icons/*` | Naruto 音乐字体（Copyright © YH & Kiyoaki, 2024–2026），经版权持有人许可以 Apache-2.0 使用 |
| `plugin/smufl_metadata_exporter.py`、`plugin/tests/*` | 本项目 |
| `plugin/bundle/Contents/MacOS/{main.py,plugin}` | GlyphsSDK 模板 |
| `plugin/smufl_optional_reference.json`、`plugin/smufl_sets_template.json`、`data/layout/anchors.glyphs.json` | Bravura `redist/Bravura.json` |
| `data/third-party/bravura/LICENSE-OFL-1.1.txt` | SIL 官方文本 |

上游快照可以用 `shasum -a 256 -c data/upstream/SHA256SUMS` 校验。
