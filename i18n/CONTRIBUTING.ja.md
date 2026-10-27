# コントリビュート

> 中国語版を優先します。[中文](../CONTRIBUTING.md) · [English](CONTRIBUTING.en.md)

## データ

`data/generated/` は生成物です。手で編集せず、次のいずれかを変更して再生成します。

| 内容 | ファイル |
|---|---|
| グループ、プリセット | `data/layout/legacy.json` |
| アンカーのルール | `data/layout/anchors.json`、`anchors.glyphs.json` |
| アイコン | `icons/` |
| 生成ロジック | `tools/build_*.py` |

```bash
python3 tools/build_all.py
```

コミットには `data/generated/` の変更も含めてください。

## SMuFL データの更新

SMuFL の新しいバージョンが出たら、`data/upstream/` を新しい tag または commit
に更新して再生成します。

```bash
python3 tools/fetch_upstream.py --ref <tag-or-commit>
python3 tools/build_all.py
```

## コード

- Python 3.9+、標準ライブラリのみ。
- テスト:

```bash
cd plugin
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

## コミットしないもの

`build/`、`release/pkg/`、`release/manual/`、`__pycache__`、`.DS_Store`。
