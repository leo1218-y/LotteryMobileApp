#!/bin/bash
set -e

echo "开始打包Android APK..."
echo "当前目录: $(pwd)"

# 检查必要文件
if [ ! -f "main.py" ]; then
    echo "错误: 未找到main.py"
    exit 1
fi

# 检查是否为WSL/Linux环境
if ! grep -q Microsoft /proc/version 2>/dev/null && ! grep -q Ubuntu /proc/version 2>/dev/null; then
    echo "警告：建议在WSL或Linux环境下运行此脚本。"
    echo "如果在Windows上，请先安装WSL：wsl --install -d Ubuntu-22.04"
    read -p "是否继续？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查并安装系统依赖
echo "检查系统依赖..."
if ! command -v pip3 &> /dev/null; then
    echo "安装pip3..."
    sudo apt update
    sudo apt install -y python3-pip
fi

if ! command -v java &> /dev/null; then
    echo "安装Java JDK..."
    sudo apt install -y openjdk-11-jdk
fi

# 检查buildozer
if ! command -v buildozer &> /dev/null; then
    echo "安装Buildozer..."
    pip3 install --user buildozer
    export PATH="$HOME/.local/bin:$PATH"
fi

# 清理旧构建
echo "清理旧构建..."
buildozer android clean 2>/dev/null || true

# 开始构建
echo "开始构建（首次需要下载SDK，请耐心等待）..."
# 自动接受Android SDK许可证
export YES_I_HAVE_READ_AND_AGREE_TO_THE_ANDROID_SDK_LICENSE_AGREEMENT=yes
buildozer android debug deploy

echo "构建完成！"
APK_FILE=$(ls bin/*.apk 2>/dev/null | head -1)
if [ -n "$APK_FILE" ]; then
    echo "APK文件: $APK_FILE"
    echo "文件大小: $(du -h "$APK_FILE" | cut -f1)"
    echo ""
    echo "安装到手机："
    echo "1. 将APK文件复制到手机"
    echo "2. 在手机文件管理器中找到APK"
    echo "3. 点击安装（需允许'未知来源应用'）"
else
    echo "未找到APK文件，构建可能失败。"
    echo "查看日志: buildozer android debug 2>&1 | tee build.log"
fi