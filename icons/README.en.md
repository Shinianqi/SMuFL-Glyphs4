# Sidebar icons

> Chinese is the primary language. [中文](README.md) · [日本語](README.ja.md)

File names must be `<name>Template.<ext>`, referenced from the plist as
`icon = <name>Template;`. If a file is missing the build script simply omits
that `icon` key.

The icons come from the Naruto music font, Copyright (C) YH & Kiyoaki,
2024-2026, and are used in this project under the Apache License 2.0 with the
permission of the copyright holders.

There are 13 icons, all used under `SMuFL Common Glyphs`; `smuflTemplate` is
also used for `SMuFL Glyphs` and the language entry.

| File | Used by | What to draw |
|---|---|---|
| `smuflTemplate.svg` | both categories + language entry | staff + note |
| `staffTemplate.svg` | Staff Structure | staff / barlines |
| `notesRestsTemplate.svg` | Notes & Rests | notehead + rest |
| `clefsTemplate.svg` | Clefs & Octaves | treble clef |
| `timeSignaturesTemplate.svg` | Time Signatures | `4/4` |
| `dynamicsTemplate.svg` | Dynamics | `f` / `p` |
| `accidentalsTemplate.svg` | Accidentals | ♯ ♭ ♮ |
| `articulationsTemplate.svg` | Articulations | staccato / accent |
| `repetitionsTemplate.svg` | Repetitions | repeat signs |
| `holdsPausesTemplate.svg` | Holds & Pauses | fermata |
| `ornamentsTemplate.svg` | Ornaments & Lines | `tr` / mordent |
| `techniquesTemplate.svg` | Techniques | playing techniques |
| `signsTextsTemplate.svg` | Signs & Texts | tempo / fingering |

## Specs

- 16 × 16 pt, `viewBox="0 0 16 16"`. Glyphs renders at the SVG's intrinsic size.
- Alpha only: black on transparent; colour is ignored.
- SVG / PDF / PNG (PNG needs `@2x`).

## Fixing inconsistent viewBoxes

```bash
python3 tools/normalize_svg.py --in-place icons/*.svg   # normalize to 16x16 in place
python3 tools/normalize_svg.py --check icons/*.svg      # check only
python3 tools/build_all.py
```

## After replacing

```bash
python3 tools/build_all.py
./install/build-release.sh
```

Quit Glyphs (Cmd-Q), reopen, and check the sidebar.
