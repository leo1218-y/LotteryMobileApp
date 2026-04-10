@echo off
echo 打包Android APK最简单的方法：
echo.
echo 1. 安装WSL（如果尚未安装）
echo    以管理员身份打开PowerShell，运行：wsl --install -d Ubuntu-22.04
echo    重启电脑后，从开始菜单启动Ubuntu，完成初始设置。
echo.
echo 2. 在WSL中运行以下命令：
echo     cd /mnt/c/Users/86152/LotteryMobileApp
echo     ./build_android.sh
echo.
echo 3. 如果遇到权限问题，先给脚本添加执行权限：
echo     chmod +x build_android.sh
echo.
echo 注意：首次构建需要下载Android SDK（约2-5GB），请确保网络连接良好。
echo.
echo 详细说明请参见 BUILD_ANDROID.md
echo.
pause