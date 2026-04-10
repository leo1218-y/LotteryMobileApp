# PowerShell script to enable WSL
Write-Host "Enabling WSL (Windows Subsystem for Linux)..." -ForegroundColor Green
Write-Host ""

# Method 1: Try using Enable-WindowsOptionalFeature if available
try {
    Write-Host "Method 1: Using Enable-WindowsOptionalFeature..." -ForegroundColor Yellow
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart -ErrorAction Stop
    Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart -ErrorAction Stop
    Write-Host "Successfully enabled WSL features!" -ForegroundColor Green
} catch {
    Write-Host "Method 1 failed: $_" -ForegroundColor Red
    Write-Host ""

    # Method 2: Try using dism.exe directly
    Write-Host "Method 2: Trying dism.exe..." -ForegroundColor Yellow
    try {
        & "dism.exe" @('/online', '/enable-feature', '/featurename:Microsoft-Windows-Subsystem-Linux', '/all', '/norestart')
        & "dism.exe" @('/online', '/enable-feature', '/featurename:VirtualMachinePlatform', '/all', '/norestart')
        Write-Host "Successfully enabled WSL features using dism!" -ForegroundColor Green
    } catch {
        Write-Host "Method 2 failed: $_" -ForegroundColor Red
        Write-Host ""

        # Method 3: Manual instructions
        Write-Host "Method 3: Please enable WSL manually:" -ForegroundColor Yellow
        Write-Host "1. Press Win + R, type 'optionalfeatures', press Enter"
        Write-Host "2. Check these two boxes:"
        Write-Host "   - Windows Subsystem for Linux"
        Write-Host "   - Virtual Machine Platform"
        Write-Host "3. Click OK and restart your computer"
        Write-Host ""
    }
}

Write-Host "Next steps after restart:" -ForegroundColor Cyan
Write-Host "1. Open Microsoft Store and install 'Ubuntu 22.04 LTS'"
Write-Host "2. Open Ubuntu from Start menu, setup username/password"
Write-Host "3. Run these commands in Ubuntu:"
Write-Host "   cd /mnt/c/Users/86152/LotteryMobileApp"
Write-Host "   chmod +x build_android.sh"
Write-Host "   ./build_android.sh"
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')