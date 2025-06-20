@echo off
chcp 65001 >nul
title VSCode插件安装器 - 普通用户权限版本

echo ========================================
echo VSCode插件安装器 - 普通用户权限版本
echo ========================================
echo.
echo 此脚本专门用于解决管理员权限与用户范围VSCode安装的冲突问题
echo 将以普通用户权限运行插件安装
echo.

echo [调试] 当前工作目录: %CD%
echo [调试] 批处理文件位置: %~dp0
echo.

REM 切换到批处理文件所在目录
cd /d "%~dp0"
echo [调试] 切换后工作目录: %CD%
echo.

echo [检查] 正在检查Python...
python --version
if errorlevel 1 (
    echo.
    echo ❌ 错误: 未找到Python
    echo 请确保Python已正确安装并添加到PATH环境变量中
    echo.
    echo 可能的解决方案:
    echo 1. 安装Python: https://www.python.org/downloads/
    echo 2. 确保Python添加到PATH环境变量
    echo 3. 重启命令提示符
    echo.
    pause
    exit /b 1
)
echo ✅ Python检查通过
echo.

echo [检查] 正在检查Python脚本文件...
if not exist "install_plugins_only.py" (
    echo.
    echo ❌ 错误: 未找到install_plugins_only.py文件
    echo 当前目录: %CD%
    echo 请确保此文件与批处理文件在同一目录中
    echo.
    dir *.py
    echo.
    pause
    exit /b 1
)
echo ✅ Python脚本文件检查通过
echo.

echo [检查] 正在检查配置文件...
if not exist "config.json" (
    echo ⚠️ 警告: 未找到config.json文件
    echo 将使用默认配置
) else (
    echo ✅ 配置文件检查通过
)
echo.

echo 🚀 开始安装VSCode插件...
echo ============================================================
echo.

REM 以普通用户权限运行Python脚本
python install_plugins_only.py

echo.
echo ============================================================
echo 插件安装脚本执行完成！
echo.
echo 如果遇到问题，请检查上方的错误信息
echo 或手动运行: python install_plugins_only.py
echo.
pause
