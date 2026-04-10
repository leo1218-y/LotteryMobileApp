#!/bin/bash
echo "Fixing Android SDK download issues..."

# Check if we're in WSL
if ! grep -q Microsoft /proc/version 2>/dev/null; then
    echo "This script should run in WSL (Windows Subsystem for Linux)"
    exit 1
fi

echo "Current directory: $(pwd)"
echo ""

# Method 1: Set proxy for Android SDK
echo "Method 1: Setting up proxy for Android SDK..."
if [ -f ~/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager ]; then
    echo "Found sdkmanager, adding proxy settings..."
    # Backup original file
    cp ~/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager ~/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager.backup

    # Add proxy arguments (uncomment and modify if you have proxy)
    # sed -i 's/DEFAULT_JVM_OPTS=""/DEFAULT_JVM_OPTS="-Djava.net.useSystemProxies=true -Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=8080"/' \
    #    ~/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager
    echo "Proxy settings added (commented out, edit if needed)"
else
    echo "sdkmanager not found, will be downloaded during build"
fi

echo ""

# Method 2: Manual SDK download
echo "Method 2: Manual SDK download instructions"
echo "If automatic download fails, you can manually download:"
echo "1. Android SDK Command Line Tools:"
echo "   https://developer.android.com/studio#command-tools"
echo "2. Download 'commandlinetools-linux-*.zip'"
echo "3. Extract to: ~/.buildozer/android/platform/android-sdk/cmdline-tools/latest/"
echo ""

# Method 3: Clean and retry with verbose logging
echo "Method 3: Clean build and retry with detailed logging"
echo "Run these commands:"
echo "  buildozer android clean"
echo "  buildozer android debug 2>&1 | tee build.log"
echo ""

# Method 4: Use mirror (for China users)
echo "Method 4: Using mirror for China users"
echo "Set environment variables:"
echo "  export HTTP_PROXY=http://127.0.0.1:7890"
echo "  export HTTPS_PROXY=http://127.0.0.1:7890"
echo "  export ALL_PROXY=socks5://127.0.0.1:7890"
echo ""
echo "Or use Tsinghua mirror (if in China):"
echo "  export SDK_MIRROR_URL=https://mirrors.tuna.tsinghua.edu.cn/android/repository/"
echo ""

echo "After trying above methods, run: ./build_android.sh"
echo ""
echo "Common solutions:"
echo "1. Check internet connection"
echo "2. Disable VPN/firewall temporarily"
echo "3. Try again later (Google servers might be slow)"
echo "4. Ensure enough disk space (need 10GB+)"
echo ""