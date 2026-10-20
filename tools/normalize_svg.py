#!/usr/bin/env python3
"""
把 SVG 图标的坐标系统归一化到 16x16。

为什么需要：
  Glyphs 的侧边栏按 SVG 的**固有尺寸**渲染图标（原版图标都是 viewBox="0 0 16 16"）。
  如果换成 viewBox="0 0 67 67" 的图，侧边栏就会把它画成 67pt —— 变成巨无霸，
  还会挤掉文字间距。启动窗口里因为会缩放，所以看起来正常。

做法：
  保持图稿本身不变，只把它包进一个 <g transform="translate(...) scale(...)">，
  并把 viewBox 改成 "0 0 16 16"。这样形状、相对大小、留白全都不变，
  只是"固有尺寸"变成了 16pt。

用法:
    python3 tools/normalize_svg.py <输入.svg> <输出.svg>
    python3 tools/normalize_svg.py <输入.svg> --check   # 只报告尺寸，不写文件
    python3 tools/normalize_svg.py icons/*.svg           # 原地批量处理
"""
import re
import sys

TARGET = 16.0


def find_svg_tag(s):
    m = re.search(r"<svg\b[^>]*>", s, re.IGNORECASE)
    if not m:
        raise SystemExit("错误: 找不到 <svg> 标签")
    return m


def parse_viewbox(tag):
    m = re.search(r'viewBox\s*=\s*"\s*([-\d.]+)[\s,]+([-\d.]+)[\s,]+([-\d.]+)[\s,]+([-\d.]+)\s*"',
                  tag, re.IGNORECASE)
    if not m:
        return None
    return tuple(float(x) for x in m.groups())


def set_attr(tag, name, value):
    """只替换 <svg> 标签上的独立属性，不碰 stroke-width 这类复合名。"""
    pattern = r'(?<![-\w])%s\s*=\s*"[^"]*"' % re.escape(name)
    new = '%s="%s"' % (name, value)
    if re.search(pattern, tag, re.IGNORECASE):
        return re.sub(pattern, new, tag, count=1, flags=re.IGNORECASE)
    return tag.replace("<svg", "<svg %s" % new, 1)


def normalize(text):
    """返回 (新内容, 原始 viewBox)。原始 viewBox 为 None 表示找不到。"""
    m = find_svg_tag(text)
    tag = m.group(0)
    vb = parse_viewbox(tag)

    if vb is None:
        raise SystemExit("错误: <svg> 上没有 viewBox，无法判断尺寸。"
                         "请给它加上 viewBox（例如 0 0 67 67）后重试。")

    minx, miny, w, h = vb
    if w <= 0 or h <= 0:
        raise SystemExit("错误: viewBox 的宽高不合法: %r" % (vb,))

    already = (abs(minx) < 1e-9 and abs(miny) < 1e-9
               and abs(w - TARGET) < 1e-9 and abs(h - TARGET) < 1e-9)
    if already:
        return text, vb

    sx, sy = TARGET / w, TARGET / h
    new_tag = set_attr(tag, "viewBox", "0 0 %g %g" % (TARGET, TARGET))
    new_tag = set_attr(new_tag, "width", "100%")
    new_tag = set_attr(new_tag, "height", "100%")

    start = m.end()
    end = text.lower().rindex("</svg>")
    inner = text[start:end]

    tx, ty = -minx * sx, -miny * sy
    if tx == 0:
        tx = 0.0          # 避免输出 "-0"
    if ty == 0:
        ty = 0.0
    wrapper = ('\n<g transform="translate(%g,%g) scale(%g,%g)">\n'
               % (tx, ty, sx, sy))
    out = (text[:m.start()] + new_tag + wrapper + inner
           + "\n</g>\n" + text[end:])
    return out, vb


def check(path):
    with open(path, encoding="utf-8") as f:
        _, vb = normalize(f.read())
    print("%s: viewBox %g %g %g %g" % (path, vb[0], vb[1], vb[2], vb[3]))
    return vb


def convert(src, dst):
    with open(src, encoding="utf-8") as f:
        out, vb = normalize(f.read())
    with open(dst, "w", encoding="utf-8") as f:
        f.write(out)
    if vb == (0.0, 0.0, TARGET, TARGET):
        print("%s: viewBox 已经是 16x16，未做改动" % dst)
    else:
        print("%s: viewBox \"%g %g %g %g\" -> \"0 0 16 16\""
              % (dst, vb[0], vb[1], vb[2], vb[3]))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    if args[0] == "--check":
        if len(args) < 2:
            print("用法: normalize_svg.py --check <file>...")
            return 2
        for path in args[1:]:
            check(path)
        return 0

    if args[0] == "--in-place":
        if len(args) < 2:
            print("用法: normalize_svg.py --in-place <file>...")
            return 2
        for path in args[1:]:
            convert(path, path)
        return 0

    if len(args) == 2:
        src, dst = args
        if dst == "--check":
            check(src)
            return 0
        convert(src, dst)
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
