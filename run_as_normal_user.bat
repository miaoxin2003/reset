@echo off
title VSCode Plugin Installer - Force Normal User

echo ========================================
echo VSCode Plugin Installer - Force Normal User
echo ========================================
echo.

echo This script will attempt to run the plugin installer
echo with normal user privileges to avoid admin conflicts.
echo.

REM Change to script directory
cd /d "%~dp0"

REM Method 1: Use runas with trustlevel
echo Method 1: Using runas with reduced privileges...
runas /trustlevel:0x20000 "cmd /c \"cd /d \"%~dp0\" && python install_plugins_only.py && pause\""

if errorlevel 1 (
    echo.
    echo Method 1 failed. Trying alternative method...
    echo.
    
    REM Method 2: Create a new command prompt without admin
    echo Method 2: Opening new non-admin command prompt...
    echo Please run the following command in the new window:
    echo.
    echo cd /d "%~dp0"
    echo python install_plugins_only.py
    echo.
    
    REM Open new command prompt
    start cmd /k "echo Please run: cd /d \"%~dp0\" && echo Then run: python install_plugins_only.py"
)

echo.
echo If both methods fail, please:
echo 1. Close ALL command prompts and PowerShell windows
echo 2. Open a NEW Command Prompt (NOT as Administrator)
echo 3. Navigate to: %~dp0
echo 4. Run: python install_plugins_only.py
echo.
pause
