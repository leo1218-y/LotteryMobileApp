#!/bin/bash

echo "启动彩票记录与分析工具..."
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

echo "Python版本:"
python3 --version

echo ""
echo "检查依赖包是否安装..."
python3 -c "import kivy" &> /dev/null
if [ $? -ne 0 ]; then
    echo "依赖包未安装，正在尝试自动安装..."
    ./install.sh
    if [ $? -ne 0 ]; then
        exit 1
    fi
fi

echo ""
echo "启动应用中..."
echo "应用窗口将很快显示..."
echo ""

# 运行应用
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "应用启动失败，请检查错误信息"
    exit 1
fi

echo ""
echo "应用已关闭"