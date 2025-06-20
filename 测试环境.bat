@echo off
chcp 65001 >nul
title 环境测试 - VSCode插件安装器

echo ========================================
echo 环境测试 - VSCode插件安装器
echo ========================================
echo.

echo [1] 当前工作目录:
echo %CD%
echo.

echo [2] 批处理文件位置:
echo %~dp0
echo.

echo [3] 切换到批处理文件目录...
cd /d "%~dp0"
echo 新工作目录: %CD%
echo.

echo [4] 检查Python:
python --version
if errorlevel 1 (
    echo ❌ Python未找到
) else (
    echo ✅ Python可用
)
echo.

echo [5] 检查文件:
echo 查找Python脚本文件...
if exist "install_plugins_only.py" (
    echo ✅ install_plugins_only.py 存在
) else (
    echo ❌ install_plugins_only.py 不存在
)

if exist "config.json" (
    echo ✅ config.json 存在
) else (
    echo ❌ config.json 不存在
)

if exist "vscode_reset_stable.py" (
    echo ✅ vscode_reset_stable.py 存在
) else (
    echo ❌ vscode_reset_stable.py 不存在
)
echo.

echo [6] 列出当前目录所有文件:
dir
echo.

echo [7] 检查VSCode路径:
if exist "C:\D\Microsoft VS Code\Code.exe" (
    echo ✅ VSCode存在: C:\D\Microsoft VS Code\Code.exe
) else (
    echo ❌ VSCode不存在: C:\D\Microsoft VS Code\Code.exe
)
echo.

echo [8] 检查VSIX文件夹:
if exist "C:\Users\baishui\Desktop\code_baishui\vsix" (
    echo ✅ VSIX文件夹存在
    echo 文件夹内容:
    dir "C:\Users\baishui\Desktop\code_baishui\vsix\*.vsix"
) else (
    echo ❌ VSIX文件夹不存在: C:\Users\baishui\Desktop\code_baishui\vsix
)
echo.

echo ========================================
echo 环境检查完成
echo ========================================
echo.
echo 如果所有检查都通过，可以尝试运行插件安装器
echo 如果有问题，请根据上面的信息进行修复
echo.
pause
