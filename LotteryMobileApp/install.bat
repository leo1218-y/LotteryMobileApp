@echo off
echo 正在安装彩票记录与分析工具依赖包...
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
echo 正在安装依赖包...
echo 请确保网络连接正常，这可能需要几分钟时间...
echo.

REM 安装依赖
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo 依赖安装失败，尝试使用国内镜像源...
    echo.
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)

if errorlevel 1 (
    echo.
    echo 依赖安装失败，请手动安装:
    echo pip install kivy==2.3.0 requests==2.31.0 plyer==2.4.0
    pause
    exit /b 1
)

echo.
echo 依赖安装完成！
echo.
echo 运行应用请执行: run.bat
echo 或直接运行: python main.py
echo.
pause