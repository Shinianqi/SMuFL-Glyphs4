# 构建

> 中文为准。[English](BUILD.en.md) · [日本語](BUILD.ja.md)

需要 Python 3.9+（只用标准库）；打包 `.pkg` 需要 macOS。

## 生成数据

```bash
python3 tools/build_all.py
```

| 脚本 | 输出 |
|---|---|
| `build_glyphdata.py` | `data/generated/GlyphData-SMuFL.xml` |
| `build_groups.py` | `data/generated/Groups-SMuFL.plist` |
| `build_glyphnames_snapshot.py` | `data/generated/smufl_glyphnames.json` |

最后运行 `verify.py` 检查结果。

生成结果是确定性的；结果已提交到仓库，安装和使用时不需要运行 Python。

## 更新 SMuFL 数据

```bash
python3 tools/fetch_upstream.py --ref <tag-or-commit>
python3 tools/build_all.py
git diff --stat data/
```

`fetch_upstream.py` 走 GitHub contents API，会更新 `VERSION.json` 和 `SHA256SUMS`。
当前数据跟随 `gh-pages` 上的 1.5 draft。

## 发布包

```bash
./install/build-release.sh
```

生成 `release/pkg/` 里的 4 个 pkg（分类表、分类表卸载、插件、插件卸载）和
`release/manual/` 里的手动安装文件。

本地调试时可以直接安装分类表：

```bash
./install/install.sh
./install/install.sh --uninstall
```

## 插件

```bash
./plugin/build.sh          # build/SMuFL Metadata.glyphsPlugin
```

bundle 由 `plugin/bundle/`（GlyphsSDK 骨架）+ 导出器 + 生成好的
`smufl_glyphnames.json` 组装。`build-release.sh` 会调用它。

## 测试

```bash
cd plugin
SMUFL_EXPORTER_NO_MAIN=1 python3 -m unittest discover -s tests -v
```

## 改侧边栏分组

编辑 `data/layout/legacy.json`：

- 分组：`{"name": ..., "icon": ..., "children": [...]}`
- 叶子：`{"name": ..., "range": "<ranges.json 的键>"}` 或
  `{"name": ..., "class": "<classes.json 的键>"}`
- `languages[0].precreate` 定义启动窗口入口，`from` 支持
  `all` / `category:<名字>` / `basics:<名字>` / `name:<叶子名>`。

叶子不存字形列表，字形来自官方数据。

> `Flags` 的名字末尾有一个零宽空格（U+200B）。Glyphs 的
> `categories.strings` 会把 `Flags` 本地化成「旗帜」，加这个字符可以绕开本地化，
> 界面上仍然显示 `Flags`。编辑这个文件时不要把它删掉。
