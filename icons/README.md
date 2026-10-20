# 侧边栏图标

> 中文为准。[English](README.en.md) · [日本語](README.ja.md)

文件名必须是 `<名字>Template.<扩展名>`，plist 里用 `icon = <名字>Template;` 引用。
文件不存在时，生成脚本会省略该 `icon` 键。

图标来自 Naruto 音乐字体，Copyright © YH & Kiyoaki, 2024–2026，
由版权持有人以 Apache-2.0 授权在本项目中使用。

共 13 个文件，全部用在 `SMuFL Common Glyphs` 下；`smuflTemplate` 另外用在
`SMuFL Glyphs` 和语言条目上。

| 文件 | 用在哪 | 画什么 |
|---|---|---|
| `smuflTemplate.svg` | 两个分类 + 语言条目 | 五线谱 + 音符 |
| `staffTemplate.svg` | Staff Structure | 谱表 / 小节线 |
| `notesRestsTemplate.svg` | Notes & Rests | 符头 + 休止符 |
| `clefsTemplate.svg` | Clefs & Octaves | 高音谱号 |
| `timeSignaturesTemplate.svg` | Time Signatures | `4/4` |
| `dynamicsTemplate.svg` | Dynamics | `f` / `p` |
| `accidentalsTemplate.svg` | Accidentals | ♯ ♭ ♮ |
| `articulationsTemplate.svg` | Articulations | 断音点 / 重音 |
| `repetitionsTemplate.svg` | Repetitions | 反复记号 |
| `holdsPausesTemplate.svg` | Holds & Pauses | 延长记号 |
| `ornamentsTemplate.svg` | Ornaments & Lines | `tr` / 波音 |
| `techniquesTemplate.svg` | Techniques | 演奏技法 |
| `signsTextsTemplate.svg` | Signs & Texts | 速度 / 指法 |

## 规格

- 16 × 16 pt，`viewBox="0 0 16 16"`。Glyphs 按 SVG 固有尺寸渲染。
- 只用 alpha 通道：黑色 + 透明背景，颜色会被忽略。
- SVG / PDF / PNG（PNG 需要 `@2x`）。

## viewBox 不一致时

```bash
python3 tools/normalize_svg.py --in-place icons/*.svg   # 原地归一化到 16×16
python3 tools/normalize_svg.py --check icons/*.svg      # 只检查
python3 tools/build_all.py
```

## 替换后

```bash
python3 tools/build_all.py
./install/build-release.sh
```

⌘Q 重启 Glyphs 查看侧边栏。
