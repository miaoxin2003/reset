@echo off
title VSCode Plugin Installer

echo ========================================
echo VSCode Plugin Installer
echo ========================================
echo.
echo This script installs VSCode plugins with normal user privileges
echo to avoid conflicts with user-scope VSCode installation.
echo.

echo [DEBUG] Current directory: %CD%
echo [DEBUG] Batch file location: %~dp0
echo.

REM Change to batch file directory
cd /d "%~dp0"
echo [DEBUG] Changed to directory: %CD%
echo.

echo [CHECK] Checking Python...
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python not found
    echo Please ensure Python is installed and added to PATH
    echo.
    pause
    exit /b 1
)
echo OK: Python is available
echo.

echo [CHECK] Checking Python script file...
if not exist "install_plugins_only.py" (
    echo.
    echo ERROR: install_plugins_only.py not found
    echo Current directory: %CD%
    echo Please ensure this file is in the same directory as the batch file
    echo.
    dir *.py
    echo.
    pause
    exit /b 1
)
echo OK: Python script file found
echo.

echo [CHECK] Checking config file...
if not exist "config.json" (
    echo WARNING: config.json not found
    echo Will use default configuration
) else (
    echo OK: Config file found
)
echo.

echo Starting VSCode plugin installation...
echo ============================================================
echo.

REM Run Python script with normal user privileges
python install_plugins_only.py

echo.
echo ============================================================
echo Plugin installation script completed!
echo.
echo If you encountered problems, check the error messages above
echo or manually run: python install_plugins_only.py
echo.
pause
