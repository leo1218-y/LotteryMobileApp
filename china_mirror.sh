#!/bin/bash
# Script for China users to fix Android SDK download issues

echo "设置Android SDK国内镜像..."
echo ""

# Set environment variables for China mirrors
export SDK_MIRROR_URL="https://mirrors.tuna.tsinghua.edu.cn/android/repository/"
export REPO_OS_OVERRIDE="linux"
export REPO_URL="https://mirrors.tuna.tsinghua.edu.cn/git/git-repo"

echo "已设置镜像源:"
echo "SDK_MIRROR_URL=$SDK_MIRROR_URL"
echo ""

# Also set proxy environment variables (uncomment if needed)
# echo "设置代理（如果需要）:"
# export HTTP_PROXY="http://127.0.0.1:7890"
# export HTTPS_PROXY="http://127.0.0.1:7890"
# export ALL_PROXY="socks5://127.0.0.1:7890"

# Create or update sdkmanager config
SDKMANAGER_DIR="$HOME/.buildozer/android/platform/android-sdk/tools/bin"
if [ -d "$SDKMANAGER_DIR" ]; then
    echo "Found Android SDK directory, updating config..."

    # Create sdkmanager config with proxy settings
    cat > /tmp/sdkmanager_config << EOF
# Android SDK Manager configuration
# Proxy settings
proxy.http=127.0.0.1:7890
proxy.https=127.0.0.1:7890

# Other settings
disable.https=false
EOF

    echo "Config file created at /tmp/sdkmanager_config"
    echo "Copy to ~/.android/android.cfg if needed"
fi

echo ""
echo "清理旧的构建缓存..."
buildozer android clean 2>/dev/null || true

echo ""
echo "开始构建（使用国内镜像）..."
echo "如果还是失败，请尝试:"
echo "1. 使用VPN"
echo "2. 手动下载SDK（见fix_android_sdk.sh）"
echo "3. 晚上或凌晨再试（网络可能更好）"
echo ""

# Continue with build
export YES_I_HAVE_READ_AND_AGREE_TO_THE_ANDROID_SDK_LICENSE_AGREEMENT=yes
buildozer android debug deploy