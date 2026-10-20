#!/bin/bash
# 为 Glyphs 4 当前使用的 Python 安装 PyObjC。
# 双击运行；如果 Gatekeeper 拦截，请右键 -> 打开。
set -u

PY="${PYTHON:-/Library/Frameworks/Python.framework/Versions/3.14/bin/python3}"
if [ ! -x "$PY" ]; then
    PY="$(command -v python3)"
fi

echo "Glyphs 4 配置的 Python:"
echo "  $PY"
echo

if [ -z "$PY" ] || [ ! -x "$PY" ]; then
    echo "找不到 python3。请在“终端”手动运行："
    echo "  /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 -m pip install --user pyobjc-framework-Cocoa"
    echo
    read -n 1 -s -r -p "按任意键关闭..."
    exit 1
fi

"$PY" -m pip install --user pyobjc-framework-Cocoa
STATUS=$?

echo
if [ "$STATUS" -eq 0 ]; then
    if "$PY" -c "import objc, AppKit" >/dev/null 2>&1; then
        echo "PyObjC 安装成功。"
        echo "请完全退出 Glyphs 4（⌘Q），重新打开后再运行脚本。"
    else
        echo "PyObjC 已安装，但当前 Python 仍无法导入 objc/AppKit。"
        echo "请把下面的输出保存下来，反馈问题时一并提供："
        "$PY" -c "import sys; print(sys.executable); print(sys.path)" 2>&1
    fi
else
    echo "安装失败。请在“终端”手动运行："
    echo "  $PY -m pip install --user pyobjc-framework-Cocoa"
fi

echo
read -n 1 -s -r -p "按任意键关闭..."
