# PowerShell script to install WSL Ubuntu 22.04 LTS on G drive
Write-Host "在 G 盘安装 WSL Ubuntu 22.04 LTS" -ForegroundColor Green
Write-Host "目标目录: G:\suoyoufuzhuwenjian\wsl-ubuntu" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "错误：请以管理员身份运行此脚本！" -ForegroundColor Red
    Write-Host "右键点击 PowerShell -> '以管理员身份运行'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "按任意键退出..."
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
    exit 1
}

# Check if G drive exists
$gDrive = "G:\"
if (-not (Test-Path $gDrive)) {
    Write-Host "错误：G 盘不存在！" -ForegroundColor Red
    Write-Host "请确保 G 盘已连接并可用" -ForegroundColor Yellow
    exit 1
}

# Check target directory
$targetDir = "G:\suoyoufuzhuwenjian\wsl-ubuntu"
if (Test-Path $targetDir) {
    Write-Host "警告：目标目录已存在: $targetDir" -ForegroundColor Yellow
    $choice = Read-Host "是否删除现有目录并重新安装？ (y/n)"
    if ($choice -eq 'y' -or $choice -eq 'Y') {
        Remove-Item -Recurse -Force $targetDir -ErrorAction SilentlyContinue
        Write-Host "已删除旧目录" -ForegroundColor Green
    } else {
        Write-Host "安装取消" -ForegroundColor Yellow
        exit 0
    }
}

# Step 1: Enable WSL features
Write-Host ""
Write-Host "步骤 1: 启用 WSL 功能..." -ForegroundColor Cyan
try {
    # Try Enable-WindowsOptionalFeature first
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -NoRestart -ErrorAction Stop
    Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart -ErrorAction Stop
    Write-Host "✓ WSL 功能已启用" -ForegroundColor Green
} catch {
    Write-Host "使用 dism.exe 启用 WSL 功能..." -ForegroundColor Yellow
    & "dism.exe" @('/online', '/enable-feature', '/featurename:Microsoft-Windows-Subsystem-Linux', '/all', '/norestart')
    & "dism.exe" @('/online', '/enable-feature', '/featurename:VirtualMachinePlatform', '/all', '/norestart')
    Write-Host "✓ WSL 功能已启用" -ForegroundColor Green
}

Write-Host ""
Write-Host "步骤 2: 设置 WSL 2 为默认版本..." -ForegroundColor Cyan
# Check WSL version
try {
    wsl --set-default-version 2
    Write-Host "✓ WSL 2 已设置为默认版本" -ForegroundColor Green
} catch {
    Write-Host "需要安装 WSL 2 内核更新..." -ForegroundColor Yellow
    Write-Host "请下载并安装: https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi" -ForegroundColor Yellow
    Write-Host "安装完成后重新运行此脚本" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "步骤 3: 创建目标目录..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
Write-Host "✓ 目录创建成功: $targetDir" -ForegroundColor Green

Write-Host ""
Write-Host "步骤 4: 下载并安装 Ubuntu 22.04 LTS..." -ForegroundColor Cyan
Write-Host "这将从 Microsoft Store 下载 Ubuntu 22.04 LTS" -ForegroundColor Yellow
Write-Host "可能需要几分钟时间，请耐心等待..." -ForegroundColor Yellow

# Method 1: Use wsl --import with a downloaded distribution
# First, we need to get the distribution
$tempDir = "$env:TEMP\wsl-ubuntu"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

Write-Host "正在获取 Ubuntu 22.04 LTS..." -ForegroundColor Yellow

# Try to download Ubuntu using winget or direct link
$ubuntuUrl = "https://aka.ms/wslubuntu2204"
$ubuntuFile = "$tempDir\Ubuntu_2204.appx"

try {
    # Download Ubuntu appx package
    Write-Host "下载 Ubuntu 22.04 LTS..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $ubuntuUrl -OutFile $ubuntuFile

    # Extract the package
    Write-Host "解压安装包..." -ForegroundColor Yellow
    Expand-Archive -Path $ubuntuFile -DestinationPath "$tempDir\ubuntu" -Force

    # Import the distribution
    Write-Host "导入到 G 盘..." -ForegroundColor Yellow
    $installTar = Get-ChildItem -Path "$tempDir\ubuntu" -Filter "*.tar" -Recurse | Select-Object -First 1

    if ($installTar) {
        wsl --import Ubuntu-22.04-G $targetDir $installTar.FullName --version 2
        Write-Host "✓ Ubuntu 22.04 LTS 已成功安装到 G 盘！" -ForegroundColor Green
    } else {
        throw "找不到 tar 文件"
    }

    # Clean up temp files
    Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue

} catch {
    Write-Host "自动安装失败，请使用手动方法：" -ForegroundColor Red
    Write-Host "1. 打开 Microsoft Store (应用商店)" -ForegroundColor Yellow
    Write-Host "2. 搜索 'Ubuntu 22.04 LTS' 并安装" -ForegroundColor Yellow
    Write-Host "3. 打开 Ubuntu 一次，设置用户名和密码" -ForegroundColor Yellow
    Write-Host "4. 然后在 PowerShell 中运行以下命令：" -ForegroundColor Yellow
    Write-Host "   wsl --export Ubuntu $targetDir\ubuntu.tar" -ForegroundColor Cyan
    Write-Host "   wsl --unregister Ubuntu" -ForegroundColor Cyan
    Write-Host "   wsl --import Ubuntu-G $targetDir $targetDir\ubuntu.tar --version 2" -ForegroundColor Cyan
    Write-Host "5. 设置默认发行版：" -ForegroundColor Yellow
    Write-Host "   wsl --set-default Ubuntu-G" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "步骤 5: 设置默认发行版..." -ForegroundColor Cyan
try {
    wsl --set-default Ubuntu-22.04-G
    Write-Host "✓ 已设置 Ubuntu-22.04-G 为默认发行版" -ForegroundColor Green
} catch {
    Write-Host "注意：可能需要手动设置默认发行版" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "安装完成！" -ForegroundColor Green
Write-Host "你可以通过以下方式启动 Ubuntu：" -ForegroundColor Cyan
Write-Host "1. 在开始菜单搜索 'Ubuntu'" -ForegroundColor Yellow
Write-Host "2. 或在 PowerShell 中运行: wsl" -ForegroundColor Yellow
Write-Host ""
Write-Host "WSL 数据存储在: $targetDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')