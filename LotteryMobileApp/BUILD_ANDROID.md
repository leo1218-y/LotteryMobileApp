# 打包为Android APK安装包

本文档指导如何将彩票记录与分析工具打包为Android APK文件，可直接安装到手机。

## 📱 支持的Android版本
- Android 5.0 (API 21) 及以上版本
- 支持ARM和x86架构设备

## 🛠️ 打包前准备

### 方法一：使用WSL（Windows用户推荐）

#### 1. 安装WSL
```bash
# 以管理员身份打开PowerShell，运行：
wsl --install -d Ubuntu-22.04

# 重启电脑后，从开始菜单启动Ubuntu
# 完成初始设置（创建用户名和密码）
```

#### 2. 在WSL中配置环境
```bash
# 更新系统
sudo apt update
sudo apt upgrade -y

# 安装必要工具
sudo apt install -y python3-pip git zip unzip openjdk-11-jdk

# 安装Buildozer
pip3 install --user buildozer

# 添加到PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 验证安装
buildozer --version
```

#### 3. 复制项目到WSL
```bash
# 在WSL中，进入主目录
cd ~

# 从Windows复制项目（假设项目在Windows的Documents文件夹）
cp -r /mnt/c/Users/86152/LotteryMobileApp/ .
cd LotteryMobileApp
```

### 方法二：使用Linux系统（Ubuntu/Debian）

如果你有Linux系统或虚拟机，直接运行：

```bash
# 安装依赖
sudo apt update
sudo apt install -y python3-pip git zip unzip openjdk-11-jdk

# 安装Buildozer
pip3 install --user buildozer

# 添加到PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 方法三：使用云服务（无需本地环境）

推荐使用Kivy的云构建服务或GitHub Actions，但需要GitHub账号。

## 🚀 开始打包

### 步骤1：初始化Buildozer配置
```bash
# 进入项目目录
cd ~/LotteryMobileApp

# 如果还没有buildozer.spec文件，初始化（已有可跳过）
buildozer init

# 编辑配置文件（可选）
# nano buildozer.spec
```

### 步骤2：下载依赖（第一次较慢）
```bash
# 下载Android SDK、NDK等工具（约2-5GB，需要良好网络）
buildozer android debug

# 如果网络问题，可以尝试使用国内镜像
# 编辑~/.buildozer/android/platform/android-sdk/tools/bin/sdkmanager
# 在合适位置添加：--proxy=http --proxy_host=127.0.0.1 --proxy_port=8080
```

### 步骤3：编译APK
```bash
# 完整编译（首次需要30分钟到2小时）
buildozer android debug deploy

# 或者分步骤
buildozer android update  # 更新依赖
buildozer android debug   # 编译调试版
```

### 步骤4：找到生成的APK
```bash
# APK文件位置
ls -la bin/*.apk

# 通常为：bin/lottery.tool-1.0.0-debug.apk
```

## 📦 APK文件说明

### 调试版 (Debug)
- 文件名：`lottery.tool-1.0.0-debug.apk`
- 特点：可调试，未优化，体积较大
- 用途：测试安装

### 发布版 (Release)
需要签名密钥，首次打包建议使用调试版。

## 📲 安装到手机

### 方法一：USB连接安装
```bash
# 连接手机并启用USB调试
# 查看设备
adb devices

# 安装APK
adb install bin/lottery.tool-1.0.0-debug.apk
```

### 方法二：手动安装
1. 将APK文件复制到手机
2. 在手机文件管理器中找到APK
3. 点击安装（需允许"未知来源应用"）

### 方法三：扫码安装（需Python简单服务器）
```bash
# 在项目目录启动HTTP服务器
python3 -m http.server 8000

# 生成二维码（需要qrcode模块）
python3 -c "import qrcode; qrcode.make('http://电脑IP:8000/bin/lottery.tool-1.0.0-debug.apk').save('qrcode.png')"

# 手机扫码下载安装
```

## 🔧 常见问题解决

### 1. 网络超时或下载失败
```bash
# 方法A：使用代理
export http_proxy="http://127.0.0.1:8080"
export https_proxy="http://127.0.0.1:8080"

# 方法B：手动下载SDK
# 从 https://developer.android.com/studio 下载Command Line Tools
# 解压到 ~/.buildozer/android/platform/android-sdk/
```

### 2. 内存不足
```bash
# 增加交换空间
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 3. 编译错误
```bash
# 清理缓存重新编译
buildozer android clean
buildozer android debug

# 查看详细日志
buildozer android debug 2>&1 | tee build.log
```

### 4. 权限问题
```bash
# 确保有足够权限
sudo chown -R $USER:$USER ~/.buildozer
```

### 5. Python版本问题
确保使用Python 3.7+：
```bash
python3 --version
# 如果不是3.7+，安装合适版本
sudo apt install python3.9
```

## ⚙️ 自定义配置

### 修改应用图标
1. 准备图标文件（建议512x512 PNG）
2. 放在项目目录，如`data/icon.png`
3. 修改`buildozer.spec`：
   ```ini
   icon.filename = %(source.dir)s/data/icon.png
   ```

### 修改应用名称和版本
```ini
title = 彩票记录与分析工具
package.name = lottery.tool
version = 1.0.0
```

### 添加其他权限
```ini
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,WRITE_EXTERNAL_STORAGE
```

## 📈 优化建议

### 减小APK体积
```ini
# 在buildozer.spec中添加
android.abi = armeabi-v7a  # 只支持ARMv7，兼容大多数设备
android.no-compile-pyo = true
```

### 加速编译
```bash
# 使用ccache
sudo apt install ccache
export USE_CCACHE=1
```

### 并行编译
```bash
# 使用多核CPU
export MAKEFLAGS="-j$(nproc)"
```

## 🌐 云打包方案

### 使用GitHub Actions（高级）
创建`.github/workflows/build.yml`：
```yaml
name: Build Android APK

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build APK
      uses: rahulbordoloi/Buildozer-Action@v1.1
      with:
        workdir: '.'
        buildozer_version: 'stable'
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: lottery-app
        path: bin/*.apk
```

## 🆘 紧急帮助

### 快速打包脚本
创建`build_android.sh`：
```bash
#!/bin/bash
set -e

echo "开始打包Android APK..."
echo "当前目录: $(pwd)"

# 检查必要文件
if [ ! -f "main.py" ]; then
    echo "错误: 未找到main.py"
    exit 1
fi

# 检查buildozer
if ! command -v buildozer &> /dev/null; then
    echo "安装Buildozer..."
    pip3 install --user buildozer
fi

# 清理旧构建
echo "清理旧构建..."
buildozer android clean 2>/dev/null || true

# 开始构建
echo "开始构建（首次需要下载SDK，请耐心等待）..."
buildozer android debug deploy

echo "构建完成！"
echo "APK文件: bin/$(ls bin/*.apk 2>/dev/null | head -1)"
```

运行：
```bash
chmod +x build_android.sh
./build_android.sh
```

## 📞 技术支持

如果遇到问题：

1. **查看日志**：`buildozer android debug 2>&1 | tee build.log`
2. **检查文件**：确保所有Python文件在正确位置
3. **网络检查**：确保能访问Google和Android官网
4. **磁盘空间**：确保有至少10GB空闲空间
5. **内存检查**：确保有至少4GB可用内存

## 📝 注意事项

1. **首次构建很慢**：需要下载Android SDK/NDK（2-5GB）
2. **需要稳定网络**：建议使用稳定的网络连接
3. **防病毒软件**：可能误报，添加例外或临时关闭
4. **手机安装**：需要开启"未知来源应用"权限
5. **版权声明**：仅供个人使用，请勿商用

## 🎉 完成！

成功打包后，你将获得：
- `bin/lottery.tool-1.0.0-debug.apk` - 调试版APK
- 可在Android 5.0+设备上安装运行

**开始你的彩票记录与分析之旅吧！**