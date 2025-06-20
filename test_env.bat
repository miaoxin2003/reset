@echo off
title Environment Test

echo ========================================
echo Environment Test - VSCode Plugin Installer
echo ========================================
echo.

echo [1] Current working directory:
echo %CD%
echo.

echo [2] Batch file location:
echo %~dp0
echo.

echo [3] Changing to batch file directory...
cd /d "%~dp0"
echo New working directory: %CD%
echo.

echo [4] Checking Python:
python --version
if errorlevel 1 (
    echo ERROR: Python not found
) else (
    echo OK: Python is available
)
echo.

echo [5] Checking files:
echo Looking for Python script files...
if exist "install_plugins_only.py" (
    echo OK: install_plugins_only.py exists
) else (
    echo ERROR: install_plugins_only.py not found
)

if exist "config.json" (
    echo OK: config.json exists
) else (
    echo ERROR: config.json not found
)

if exist "vscode_reset_stable.py" (
    echo OK: vscode_reset_stable.py exists
) else (
    echo ERROR: vscode_reset_stable.py not found
)
echo.

echo [6] Listing all files in current directory:
dir
echo.

echo [7] Checking VSCode path:
if exist "C:\D\Microsoft VS Code\Code.exe" (
    echo OK: VSCode found at C:\D\Microsoft VS Code\Code.exe
) else (
    echo ERROR: VSCode not found at C:\D\Microsoft VS Code\Code.exe
)
echo.

echo [8] Checking VSIX folder:
if exist "C:\Users\baishui\Desktop\code_baishui\vsix" (
    echo OK: VSIX folder exists
    echo Folder contents:
    dir "C:\Users\baishui\Desktop\code_baishui\vsix\*.vsix"
) else (
    echo ERROR: VSIX folder not found at C:\Users\baishui\Desktop\code_baishui\vsix
)
echo.

echo ========================================
echo Environment check completed
echo ========================================
echo.
echo If all checks pass, you can try running the plugin installer
echo If there are problems, please fix them based on the information above
echo.
pause
