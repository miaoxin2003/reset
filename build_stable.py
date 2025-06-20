#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VSCode重置工具 2.0版本 打包脚本
增强版 - 彻底解决Augment进程清理问题
包含强化的文件删除机制和进程管理
"""

import subprocess
import sys
import shutil
from pathlib import Path
import time


def build_stable():
    """构建2.0版本（简化版）"""
    print("🔧 构建VSCode重置工具 - 2.0版本（简化版）")
    print("🚀 主要功能:")
    print("  ✅ 彻底清理Augment相关进程")
    print("  ✅ 强化文件删除机制（重试+强制删除）")
    print("  ✅ 专门的Augment残留文件清理")
    print("  ✅ 深度优先删除顺序")
    print("  ✅ 增强的错误恢复能力")
    print("  ✅ 移除插件自动安装（避免权限冲突）")
    print("  ✅ 简化进程关闭（只执行一次）")
    print("=" * 60)
    
    # 检查源文件
    source_file = "vscode_reset_stable.py"
    if not Path(source_file).exists():
        print(f"❌ 源文件不存在: {source_file}")
        return False
    
    # 清理旧文件
    print("🧹 清理旧文件...")
    for dir_name in ["build", "dist"]:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"✅ 清理: {dir_name}")
    
    # 删除spec文件
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"✅ 删除: {spec_file}")
    
    # 构建命令 - 2.0版本优化参数，使用Python模块方式调用
    cmd = [
        sys.executable, "-m", "PyInstaller",  # 使用Python模块方式调用
        "--onefile",                        # 单文件
        "--console",                        # 控制台模式
        "--name", "VSCode重置工具2.0版",      # 2.0版本名称
        "--clean",                          # 清理
        "--noconfirm",                      # 不确认
        "--noupx",                          # 不使用UPX压缩（避免兼容性问题）
        "--strip",                          # 去除调试信息
        "--uac-admin",                      # 请求管理员权限
        "--add-data", "config.json;.",      # 包含配置文件
        "--hidden-import", "ctypes",        # 确保ctypes模块被包含
        "--hidden-import", "subprocess",    # 确保subprocess模块被包含
        "--hidden-import", "shutil",        # 确保shutil模块被包含
        source_file
    ]
    
    print("🔨 开始构建...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        # 执行构建
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        # 检查输出文件
        exe_path = Path("dist") / "VSCode重置工具2.0版.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print("✅ 构建成功!")
            print(f"📁 文件: {exe_path}")
            print(f"📏 大小: {size_mb:.2f} MB")
            print(f"🏷️ 版本: 2.0 (增强版)")
            print(f"📅 构建时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 简单测试
            print("🧪 测试运行...")
            try:
                test_result = subprocess.run([str(exe_path), "--help"], 
                                           capture_output=True, text=True, timeout=15)
                if test_result.returncode == 0:
                    print("✅ 测试通过!")
                else:
                    print("⚠️ 测试有警告，但文件已生成")
                    print(f"输出: {test_result.stdout}")
                    print(f"错误: {test_result.stderr}")
            except subprocess.TimeoutExpired:
                print("⚠️ 测试超时，但文件可能正常")
            except Exception as e:
                print(f"⚠️ 测试出错: {e}")
            
            # 清理临时文件
            print("🧹 清理临时文件...")
            build_dir = Path("build")
            if build_dir.exists():
                shutil.rmtree(build_dir)
            
            for spec_file in Path(".").glob("*.spec"):
                spec_file.unlink()
            
            return True
        else:
            print("❌ 未找到输出文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print("❌ 构建失败!")
        print(f"返回码: {e.returncode}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 构建过程出错: {e}")
        return False


def create_test_script():
    """创建2.0版本测试脚本"""
    test_script = """@echo off
chcp 65001 >nul
echo ========================================
echo VSCode重置工具 2.0版本 测试脚本
echo ========================================
echo.

if not exist "dist\\VSCode重置工具2.0版.exe" (
    echo 错误: 可执行文件不存在
    echo 请先运行 build_stable.py 进行构建
    pause
    exit /b 1
)

echo [测试1] 显示帮助信息
echo ----------------------------------------
"dist\\VSCode重置工具2.0版.exe" --help
echo.

echo [测试2] 显示VSCode路径
echo ----------------------------------------
"dist\\VSCode重置工具2.0版.exe" --show-paths
echo.

echo [测试3] 仅清理Augment残留（安全测试）
echo ----------------------------------------
echo 这个测试相对安全，只清理Augment残留文件
echo 按Ctrl+C取消，或按任意键继续...
pause
"dist\\VSCode重置工具2.0版.exe" --augment
echo.

echo [警告] 测试4: 完整重置测试（危险操作）
echo ----------------------------------------
echo 警告: 这将实际执行VSCode重置操作!
echo 建议在虚拟机中进行此测试
echo 按Ctrl+C取消，或按任意键继续...
pause
"dist\\VSCode重置工具2.0版.exe" --reset
echo.

echo [完成] 测试完成
echo 请检查日志文件: vscode_reset_log.txt
pause
"""

    test_file = Path("test_v2.bat")
    test_file.write_text(test_script, encoding='utf-8')
    print(f"✅ 创建2.0版本测试脚本: {test_file}")


def create_version_info():
    """创建版本信息文件"""
    version_info = f"""# VSCode重置工具 2.0版本

## 版本信息
- **版本号**: 2.0
- **构建时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **主要改进**: 彻底解决Augment进程清理问题

## 新增功能
✅ **彻底的进程清理**
- 关闭所有VSCode相关进程（Code.exe, node.exe, electron.exe）
- 专门清理Augment相关进程（augment.exe, augment-vip-windows-x86_64.exe）
- 多轮进程关闭确保彻底

✅ **强化的文件删除机制**
- 重试机制：最多3次重试，指数退避
- 强制删除：使用系统命令作为备选方案
- 递归删除：从最深层文件开始删除
- 权限处理：自动修改文件权限

✅ **专门的Augment残留清理**
- 搜索所有包含"augment"的文件夹
- 彻底清理Augment用户资产文件
- 解决"目录不是空的"错误

✅ **改进的删除顺序**
- 深度优先：按路径长度降序排序
- 分批处理：提供进度反馈
- 容错处理：即使部分失败也继续执行

## 使用方法
```
VSCode重置工具2.0版.exe              # 执行完整升级流程
VSCode重置工具2.0版.exe -s           # 显示路径
VSCode重置工具2.0版.exe -h           # 显示帮助
VSCode重置工具2.0版.exe --reset      # 仅执行重置
VSCode重置工具2.0版.exe --augment    # 仅运行Augment
VSCode重置工具2.0版.exe --plugins    # 仅安装插件
```

## 升级流程
1. **彻底关闭进程** - 多轮关闭VSCode和Augment相关进程
2. **运行Augment安装** - 以管理员身份运行Augment安装程序
3. **清理Augment残留** - 专门清理Augment残留文件
4. **重置VSCode配置** - 使用强化删除机制重置配置
5. **安装插件** - 自动安装指定的VSIX插件

## 故障排除
如果仍有问题：
1. 以管理员身份运行
2. 检查杀毒软件是否拦截
3. 查看日志文件: vscode_reset_log.txt
4. 确保在虚拟机中测试
5. 检查Augment程序路径和VSIX文件夹
"""

    readme_file = Path("README_v2.md")
    readme_file.write_text(version_info, encoding='utf-8')
    print(f"✅ 创建版本信息文件: {readme_file}")


def main():
    """主函数"""
    if build_stable():
        print("\n🎉 VSCode重置工具 2.0版本（简化版）构建完成!")
        print("\n📋 2.0版本使用说明:")
        print("  VSCode重置工具2.0版.exe              # 执行完整升级流程（不含插件安装）")
        print("  VSCode重置工具2.0版.exe -s           # 显示路径")
        print("  VSCode重置工具2.0版.exe -h           # 显示帮助")
        print("  VSCode重置工具2.0版.exe --reset      # 仅执行重置")
        print("  VSCode重置工具2.0版.exe --augment    # 仅运行Augment")

        print("\n🚀 2.0版本升级流程（简化版）:")
        print("  1. 关闭VSCode和Augment进程（单次清理）")
        print("  2. 以管理员身份运行Augment安装程序")
        print("  3. 专门清理Augment残留文件")
        print("  4. 使用强化机制重置VSCode配置")

        print("\n✨ 2.0版本主要改进:")
        print("  ✅ 彻底解决Augment进程清理问题")
        print("  ✅ 强化文件删除机制（重试+强制删除）")
        print("  ✅ 深度优先删除顺序")
        print("  ✅ 专门的Augment残留文件清理")
        print("  ✅ 增强的错误恢复能力")
        print("  ✅ 移除插件自动安装（避免权限冲突）")
        print("  ✅ 简化进程关闭流程")

        print("\n💡 使用建议:")
        print("  1. 建议在虚拟机中先测试")
        print("  2. 以管理员身份运行主程序")
        print("  3. 检查日志文件了解详细执行情况")
        print("  4. 确保Augment程序路径正确")

        print("\n🔌 插件安装（独立工具）:")
        print("  插件安装已从主程序中移除，请使用以下独立工具:")
        print("  1. install_plugins_normal_user.ps1 (推荐)")
        print("  2. python install_plugins_only.py")
        print("  3. 手动安装: VSCode -> Ctrl+Shift+P -> Extensions: Install from VSIX")

        # 创建测试脚本和版本信息
        create_test_script()
        create_version_info()

        print(f"\n🧪 可以运行 test_v2.bat 进行测试")
        print(f"📖 查看 README_v2.md 了解详细信息")
    else:
        print("\n❌ 构建失败!")


if __name__ == "__main__":
    main()
