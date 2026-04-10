@echo off
echo 启动彩票记录与分析工具...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo Python版本:
python --version

echo.
echo 检查依赖包是否安装...
python -c "import kivy" >nul 2>&1
if errorlevel 1 (
    echo 依赖包未安装，正在尝试自动安装...
    call install.bat
    if errorlevel 1 (
        pause
        exit /b 1
    )
)

echo.
echo 启动应用中...
echo 应用窗口将很快显示...
echo.

REM 运行应用
python main.py

if errorlevel 1 (
    echo.
    echo 应用启动失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo 应用已关闭
pause