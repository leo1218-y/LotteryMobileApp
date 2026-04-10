#!/bin/bash

echo "正在安装彩票记录与分析工具依赖包..."
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

echo "Python版本:"
python3 --version

echo ""
echo "正在安装依赖包..."
echo "请确保网络连接正常，这可能需要几分钟时间..."
echo ""

# 安装依赖
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "依赖安装失败，尝试使用国内镜像源..."
    echo ""
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
fi

if [ $? -ne 0 ]; then
    echo ""
    echo "依赖安装失败，请手动安装:"
    echo "pip3 install kivy==2.3.0 requests==2.31.0 plyer==2.4.0"
    exit 1
fi

echo ""
echo "依赖安装完成！"
echo ""
echo "运行应用请执行: ./run.sh"
echo "或直接运行: python3 main.py"
echo ""