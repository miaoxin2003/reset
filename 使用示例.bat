@echo off
chcp 65001 >nul
echo ========================================
echo VSCode重置工具升级版 - 使用示例
echo ========================================
echo.

if not exist "dist\VSCode重置工具升级版.exe" (
    echo ❌ 错误: 可执行文件不存在
    echo 请先运行 build_stable.py 构建程序
    pause
    exit /b 1
)

echo 📋 可用选项:
echo   1. 执行完整升级流程 (推荐)
echo   2. 仅显示VSCode路径
echo   3. 仅执行重置操作
echo   4. 仅运行Augment程序
echo   5. 仅安装插件
echo   6. 显示帮助信息
echo   0. 退出
echo.

:menu
set /p choice="请选择操作 (0-6): "

if "%choice%"=="1" (
    echo.
    echo ⚠️ 警告: 这将执行完整的升级流程!
    echo 包括: 运行Augment、重置VSCode、安装插件
    echo.
    set /p confirm="确认执行? (y/N): "
    if /i "!confirm!"=="y" (
        echo 正在执行完整升级流程...
        "dist\VSCode重置工具升级版.exe"
    )
    goto end
)

if "%choice%"=="2" (
    echo 显示VSCode路径...
    "dist\VSCode重置工具升级版.exe" -s
    goto end
)

if "%choice%"=="3" (
    echo.
    echo ⚠️ 警告: 这将删除所有VSCode配置!
    set /p confirm="确认执行重置? (y/N): "
    if /i "!confirm!"=="y" (
        echo 正在执行重置...
        "dist\VSCode重置工具升级版.exe" --reset
    )
    goto end
)

if "%choice%"=="4" (
    echo 正在运行Augment程序...
    "dist\VSCode重置工具升级版.exe" --augment
    goto end
)

if "%choice%"=="5" (
    echo 正在安装插件...
    "dist\VSCode重置工具升级版.exe" --plugins
    goto end
)

if "%choice%"=="6" (
    echo 显示帮助信息...
    "dist\VSCode重置工具升级版.exe" --help
    goto end
)

if "%choice%"=="0" (
    echo 退出程序
    goto end
)

echo 无效选择，请重新输入
goto menu

:end
echo.
echo 操作完成，查看日志文件: vscode_reset_log.txt
pause
