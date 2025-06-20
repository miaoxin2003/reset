@echo off
echo 测试VSCode重置工具升级版
echo.

if not exist "dist\VSCode重置工具升级版.exe" (
    echo 错误: 可执行文件不存在
    pause
    exit /b 1
)

echo 测试1: 显示帮助
"dist\VSCode重置工具升级版.exe" --help
echo.

echo 测试2: 显示路径
"dist\VSCode重置工具升级版.exe" --show-paths
echo.

echo 测试3: 仅重置测试
echo 注意: 这将实际执行重置操作!
echo 按Ctrl+C取消，或按任意键继续...
pause
"dist\VSCode重置工具升级版.exe" --reset
echo.

echo 测试完成
pause
