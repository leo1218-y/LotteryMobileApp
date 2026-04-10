@echo off
echo APK BUILD GUIDE
echo.
echo Step 1: Install WSL
echo Press Win + R, type: optionalfeatures
echo Check: Windows Subsystem for Linux
echo Check: Virtual Machine Platform
echo Click OK, restart computer
echo.
echo Step 2: Install Ubuntu
echo Open Microsoft Store
echo Search: Ubuntu 22.04 LTS
echo Click Get, install
echo.
echo Step 3: Setup Ubuntu
echo Open Ubuntu from Start menu
echo Username: lottery
echo Password: type anything
echo.
echo Step 4: Build APK
echo In Ubuntu window type:
echo cd /mnt/c/Users/86152/LotteryMobileApp
echo chmod +x build_android.sh
echo ./build_android.sh
echo.
echo Wait 30min-2hours for first build
echo APK in bin/ folder
echo.
pause