# Check if WSL is installed and help install it
Write-Host "Checking WSL installation..." -ForegroundColor Yellow

# Check if wsl command exists
try {
    $wslCheck = wsl --list --quiet 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "WSL is already installed!" -ForegroundColor Green
        Write-Host "Installed distributions:" -ForegroundColor Cyan
        wsl --list --verbose
        Write-Host ""
        Write-Host "To build APK, open Ubuntu and run:" -ForegroundColor Cyan
        Write-Host "cd /mnt/c/Users/86152/LotteryMobileApp"
        Write-Host "chmod +x build_android.sh"
        Write-Host "./build_android.sh"
        exit 0
    }
} catch {
    # WSL not installed or command failed
}

Write-Host "WSL is not installed." -ForegroundColor Red
Write-Host ""
Write-Host "To install WSL, you have two options:" -ForegroundColor Yellow
Write-Host ""
Write-Host "OPTION 1: Simple GUI method" -ForegroundColor Cyan
Write-Host "1. Press Win + R, type 'optionalfeatures', press Enter"
Write-Host "2. Check these two boxes:"
Write-Host "   - Windows Subsystem for Linux"
Write-Host "   - Virtual Machine Platform"
Write-Host "3. Click OK, restart computer"
Write-Host "4. Open Microsoft Store, install 'Ubuntu 22.04 LTS'"
Write-Host ""
Write-Host "OPTION 2: Command line method (run as Administrator)" -ForegroundColor Cyan
Write-Host "Run this in PowerShell as Administrator:"
Write-Host "wsl --install -d Ubuntu-22.04"
Write-Host ""
Write-Host "After installing Ubuntu, open it from Start menu,"
Write-Host "setup username/password, then run the build commands."
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')