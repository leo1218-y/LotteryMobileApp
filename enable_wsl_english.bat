@echo off
echo Easiest way to install WSL (no commands needed):
echo.
echo Step 1: Press Win + R key
echo        Type: optionalfeatures
echo        Press Enter
echo.
echo Step 2: In the window that pops up, check these two boxes:
echo       [√] Windows Subsystem for Linux
echo       [√] Virtual Machine Platform
echo.
echo Step 3: Click "OK"
echo        Windows will install needed components
echo.
echo Step 4: Restart your computer
echo.
echo Step 5: Open Microsoft Store
echo        Search for "Ubuntu 22.04 LTS" -> Click "Get"
echo.
echo Step 6: Open "Ubuntu" from Start menu
echo        First time setup:
echo        Username: English name (e.g., lottery)
echo        Password: type anything (won't show while typing)
echo.
echo Step 7: In Ubuntu window, type one by one:
echo       cd /mnt/c/Users/86152/LotteryMobileApp
echo       chmod +x build_android.sh
echo       ./build_android.sh
echo.
echo Wait for completion (first time 30min-2hours)
echo APK file will be in bin/ folder
echo.
pause