@echo off
chcp 65001 >nul
echo ========================================
echo VSCode重置工具 2.0版本 测试脚本
echo ========================================
echo.

if not exist "dist\VSCode重置工具2.0版.exe" (
    echo 错误: 可执行文件不存在
    echo 请先运行 build_stable.py 进行构建
    pause
    exit /b 1
)

echo [测试1] 显示帮助信息
echo ----------------------------------------
"dist\VSCode重置工具2.0版.exe" --help
echo.

echo [测试2] 显示VSCode路径
echo ----------------------------------------
"dist\VSCode重置工具2.0版.exe" --show-paths
echo.

echo [测试3] 仅清理Augment残留（安全测试）
echo ----------------------------------------
echo 这个测试相对安全，只清理Augment残留文件
echo 按Ctrl+C取消，或按任意键继续...
pause
"dist\VSCode重置工具2.0版.exe" --augment
echo.

echo [警告] 测试4: 完整重置测试（危险操作）
echo ----------------------------------------
echo 警告: 这将实际执行VSCode重置操作!
echo 建议在虚拟机中进行此测试
echo 按Ctrl+C取消，或按任意键继续...
pause
"dist\VSCode重置工具2.0版.exe" --reset
echo.

echo [完成] 测试完成
echo 请检查日志文件: vscode_reset_log.txt
pause
