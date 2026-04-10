@echo off
echo 在 G 盘安装 WSL Ubuntu 22.04 LTS
echo ====================================
echo.
echo 此脚本将在 G:\suoyoufuzhuwenjian\wsl-ubuntu 目录安装 Ubuntu 22.04 LTS
echo.
echo 需要以管理员身份运行！
echo.
echo 请确保：
echo 1. Windows 版本为 2004 或更高
echo 2. G 盘已连接并有足够空间（至少 10GB）
echo 3. 已连接到互联网
echo.
echo 如果出现"无法加载文件"错误，请先运行：
echo    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
echo.
echo 按任意键开始安装（按 Ctrl+C 取消）...
pause > nul

echo.
echo 正在启动 PowerShell 脚本...
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0install_wsl_gdrive.ps1"

echo.
echo 安装脚本执行完毕！
echo 如果遇到问题，请查看上面的错误信息。
echo.
pause