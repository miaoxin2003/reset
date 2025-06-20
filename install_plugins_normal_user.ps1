# VSCode插件安装器 - 强制普通用户权限
# 解决管理员权限与用户范围VSCode安装的冲突

Write-Host "========================================" -ForegroundColor Green
Write-Host "VSCode Plugin Installer - Normal User Mode" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 检查当前是否为管理员
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if ($isAdmin) {
    Write-Host "WARNING: Running as Administrator detected" -ForegroundColor Yellow
    Write-Host "This will cause conflicts with user-scope VSCode installation" -ForegroundColor Yellow
    Write-Host "Attempting to restart as normal user..." -ForegroundColor Yellow
    Write-Host ""
    
    # 获取当前用户的用户名
    $currentUser = $env:USERNAME
    
    # 构建命令
    $scriptPath = $PSScriptRoot + "\install_plugins_only.py"
    $pythonCmd = "python `"$scriptPath`""
    
    try {
        # 方法1: 使用runas /trustlevel
        Write-Host "Method 1: Using runas with trustlevel..." -ForegroundColor Cyan
        $process = Start-Process -FilePath "runas" -ArgumentList "/trustlevel:0x20000", "cmd /c `"cd /d `"$PSScriptRoot`" && $pythonCmd && pause`"" -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-Host "Plugin installation completed successfully!" -ForegroundColor Green
            exit 0
        }
    }
    catch {
        Write-Host "Method 1 failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    try {
        # 方法2: 创建新的非管理员进程
        Write-Host "Method 2: Creating new non-admin process..." -ForegroundColor Cyan
        
        # 创建临时批处理文件
        $tempBat = "$env:TEMP\install_vscode_plugins_temp.bat"
        $batContent = @"
@echo off
cd /d "$PSScriptRoot"
python install_plugins_only.py
pause
"@
        Set-Content -Path $tempBat -Value $batContent -Encoding ASCII
        
        # 以普通用户身份运行
        Start-Process -FilePath $tempBat -Verb runAsUser -Wait
        
        # 清理临时文件
        Remove-Item $tempBat -Force -ErrorAction SilentlyContinue
        
        Write-Host "Plugin installation completed!" -ForegroundColor Green
        exit 0
    }
    catch {
        Write-Host "Method 2 failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "MANUAL SOLUTION:" -ForegroundColor Yellow
    Write-Host "1. Close this window" -ForegroundColor White
    Write-Host "2. Open a NEW Command Prompt (NOT as Administrator)" -ForegroundColor White
    Write-Host "3. Navigate to: $PSScriptRoot" -ForegroundColor White
    Write-Host "4. Run: python install_plugins_only.py" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
else {
    Write-Host "OK: Running with normal user privileges" -ForegroundColor Green
    Write-Host ""
    
    # 切换到脚本目录
    Set-Location $PSScriptRoot
    
    # 运行Python脚本
    Write-Host "Starting plugin installation..." -ForegroundColor Cyan
    python install_plugins_only.py
    
    Write-Host ""
    Write-Host "Plugin installation script completed!" -ForegroundColor Green
    Read-Host "Press Enter to exit"
}
