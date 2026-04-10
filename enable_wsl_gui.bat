@echo off
echo 启用WSL最简单的方法（不用输入命令）：
echo.
echo 第1步：按 Win + R 键
echo       输入： optionalfeatures
echo       按回车
echo.
echo 第2步：在弹出的窗口中，找到并勾选：
echo       [√] 适用于 Linux 的 Windows 子系统
echo       [√] 虚拟机平台
echo.
echo 第3步：点击"确定"
echo       系统会自动安装需要的组件
echo.
echo 第4步：重启电脑
echo.
echo 第5步：打开 Microsoft Store（应用商店）
echo       搜索 "Ubuntu 22.04 LTS" -> 点击"获取"
echo.
echo 第6步：在开始菜单打开 "Ubuntu"
echo       第一次需要设置：
echo       用户名：英文名（例如：lottery）
echo       密码：随便设一个（输入时不显示）
echo.
echo 第7步：在 Ubuntu 窗口中，一行一行输入：
echo       cd /mnt/c/Users/86152/LotteryMobileApp
echo       chmod +x build_android.sh
echo       ./build_android.sh
echo.
echo 等待完成（第一次需要30分钟-2小时）
echo APK文件会在 bin/ 文件夹里
echo.
pause