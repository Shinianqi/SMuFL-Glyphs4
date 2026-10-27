# 参与贡献

> 中文为准。[English](i18n/CONTRIBUTING.en.md) · [日本語](i18n/CONTRIBUTING.ja.md)

## 数据

`data/generated/` 是生成结果，不要手改。修改下面任意一处后重新生成：

| 内容 | 文件 |
|---|---|
| 分组、预创建入口 | `data/layout/legacy.json` |
| 锚点规则 | `data/layout/anchors.json` |
| 图标 | `icons/` |
| 生成规则 | `tools/build_*.py` |

```bash
python3 tools/build_all.py
```

提交时带上 `data/generated/` 的变更。

## 更新 SMuFL 数据

SMuFL 发布新版本时，把 `data/upstream/` 更新到新的 tag 或 commit，再重新生成：

```bash
python3 tools/fetch_upstream.py --ref <tag-or-commit>
python3 tools/build_all.py
```

## 代码

- Python 3.9+，只用标准库。
- 测试：

```bash
cd plugin
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

## 不要提交

`build/`、`release/pkg/`、`release/manual/`、`__pycache__`、`.DS_Store`。
