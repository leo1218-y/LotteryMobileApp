@echo off
echo 安装 WSL (Linux子系统) 的分步指南
echo ===================================
echo.
echo 第一步：检查 Windows 版本
echo 请确认你的Windows版本是 2004 或更高版本
echo 按 Win + R 键，输入 "winver" 按回车查看
echo.
echo 如果版本太低，需要先更新Windows：
echo 1. 打开"设置" -> "更新和安全" -> "Windows更新"
echo 2. 检查更新并安装所有可用更新
echo.
echo 第二步：以管理员身份启用 Windows 功能
echo.
echo 方法A（推荐）：
echo 1. 右键点击开始菜单，选择"Windows PowerShell (管理员)"
echo 2. 复制粘贴以下命令，按回车：
echo    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
echo 3. 再粘贴以下命令，按回车：
echo    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
echo 4. 重启电脑
echo.
echo 方法B：
echo 1. 按 Win + R 键，输入 "optionalfeatures" 按回车
echo 2. 找到并勾选：
echo    - [ ] 适用于 Linux 的 Windows 子系统
echo    - [ ] 虚拟机平台
echo 3. 点击"确定"，重启电脑
echo.
echo 第三步：安装 WSL2 内核更新
echo 1. 下载更新包：
echo    https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi
echo 2. 运行下载的 msi 文件
echo.
echo 第四步：安装 Ubuntu
echo 1. 打开 Microsoft Store（应用商店）
echo 2. 搜索 "Ubuntu 22.04 LTS"
echo 3. 点击"获取"进行安装
echo.
echo 第五步：启动 Ubuntu
echo 1. 在开始菜单找到 "Ubuntu" 并打开
echo 2. 第一次启动需要设置：
echo    - 用户名：英文名（不要用中文）
echo    - 密码：输入时不会显示，输完按回车
echo.
echo 第六步：在 Ubuntu 中打包
echo 在 Ubuntu 窗口中一行一行输入：
echo.
echo 1. 进入你的项目文件夹：
echo    cd /mnt/c/Users/86152/LotteryMobileApp
echo.
echo 2. 给脚本添加权限：
echo    chmod +x build_android.sh
echo.
echo 3. 开始打包：
echo    ./build_android.sh
echo.
echo 注意：第一次打包需要下载Android SDK（2-5GB），请保持网络稳定。
echo 打包完成后APK文件在 bin/ 文件夹里。
echo.
echo 如果还有问题，请截图发给我看。
echo.
pause