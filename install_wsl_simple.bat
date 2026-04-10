@echo off
echo 最简单安装WSL的方法（只需复制粘贴）：
echo.
echo 第1步：右键点击开始菜单 -> "Windows PowerShell (管理员)"
echo.
echo 第2步：在蓝色窗口中，复制粘贴这条命令（按回车）：
echo    dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
echo.
echo 第3步：再粘贴这条命令（按回车）：
echo    dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
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
echo.
pause