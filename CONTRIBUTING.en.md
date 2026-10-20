# Contributing

> Chinese is the primary language. [中文](CONTRIBUTING.md) · [日本語](CONTRIBUTING.ja.md)

## Data

`data/generated/` is generated; do not edit it by hand. Change any of the
following and rebuild:

| Content | File |
|---|---|
| Groups, presets | `data/layout/legacy.json` |
| Anchor rules | `data/layout/anchors.json`, `anchors.glyphs.json` |
| Icons | `icons/` |
| Generation logic | `tools/build_*.py` |

```bash
python3 tools/build_all.py
```

Include the `data/generated/` changes in the commit.

## Updating the SMuFL data

When a new SMuFL version is published, point `data/upstream/` at the new tag or
commit and regenerate:

```bash
python3 tools/fetch_upstream.py --ref <tag-or-commit>
python3 tools/build_all.py
```

## Code

- Python 3.9+, standard library only.
- Tests:

```bash
cd plugin
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

## Do not commit

`build/`, `release/pkg/`, `release/manual/`, `__pycache__`, `.DS_Store`.
