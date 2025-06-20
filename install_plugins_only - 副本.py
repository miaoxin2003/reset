#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VSCode插件安装器 - 普通用户权限版本
专门用于解决管理员权限与用户范围VSCode安装的冲突问题
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path


def load_config():
    """加载配置文件"""
    try:
        config_file = Path(__file__).parent / "config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"加载配置文件失败: {e}")
    
    # 返回默认配置
    return {
        "vscode_exe_path": "C:\\D\\Microsoft VS Code\\Code.exe",
        "vsix_folder_path": "C:\\Users\\baishui\\Desktop\\code_baishui\\vsix",
    }


def find_vscode():
    """查找VSCode可执行文件"""
    config = load_config()
    
    # 首先尝试配置文件中的路径
    if "vscode_exe_path" in config:
        config_path = Path(config["vscode_exe_path"])
        if config_path.exists():
            print(f"✅ 使用配置文件中的VSCode路径: {config_path}")
            return config_path
    
    # 常见的VSCode安装路径
    possible_paths = [
        Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs' / 'Microsoft VS Code' / 'Code.exe',
        Path(os.environ.get('PROGRAMFILES', '')) / 'Microsoft VS Code' / 'Code.exe',
        Path(os.environ.get('PROGRAMFILES(X86)', '')) / 'Microsoft VS Code' / 'Code.exe',
        Path("C:\\D\\Microsoft VS Code\\Code.exe"),
    ]
    
    for path in possible_paths:
        if path.exists():
            print(f"✅ 找到VSCode: {path}")
            return path
    
    # 尝试从PATH中查找
    try:
        result = subprocess.run(['where', 'code'], capture_output=True, text=True, check=True)
        if result.stdout.strip():
            code_path = Path(result.stdout.strip().split('\n')[0])
            
            # 如果找到的是bin/code，转换为真正的Code.exe路径
            if code_path.name == 'code' and 'bin' in str(code_path):
                vscode_root = code_path.parent.parent
                real_exe = vscode_root / 'Code.exe'
                if real_exe.exists():
                    print(f"✅ 转换为真正的VSCode路径: {real_exe}")
                    return real_exe
            
            # 如果直接是exe文件
            elif code_path.suffix.lower() == '.exe' and code_path.exists():
                print(f"✅ 从PATH找到VSCode: {code_path}")
                return code_path
    except:
        pass
    
    return None


def install_plugins():
    """安装VSCode插件"""
    print("=" * 60)
    print("VSCode插件安装器 - 普通用户权限版本")
    print("=" * 60)
    
    # 检查是否以管理员身份运行
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if is_admin:
            print("⚠️ 警告: 当前以管理员身份运行")
            print("⚠️ 这可能导致与用户范围VSCode安装的权限冲突")
            print("💡 建议: 以普通用户身份运行此脚本")
            print()
    except:
        pass
    
    # 查找VSCode
    vscode_path = find_vscode()
    if not vscode_path:
        print("❌ 未找到VSCode可执行文件")
        print("💡 请确保VSCode已正确安装")
        return False
    
    # 获取配置
    config = load_config()
    vsix_folder = Path(config.get("vsix_folder_path", ""))
    
    if not vsix_folder.exists():
        print(f"❌ VSIX文件夹不存在: {vsix_folder}")
        return False
    
    # 获取所有VSIX文件
    vsix_files = list(vsix_folder.glob("*.vsix"))
    if not vsix_files:
        print("❌ 未找到VSIX插件文件")
        return False
    
    print(f"发现 {len(vsix_files)} 个插件文件:")
    for vsix_file in vsix_files:
        print(f"  - {vsix_file.name}")
    print()
    
    # 安装每个插件
    success_count = 0
    for i, vsix_file in enumerate(vsix_files, 1):
        try:
            print(f"[{i}/{len(vsix_files)}] 正在安装: {vsix_file.name}")
            
            # 构建命令
            cmd = [str(vscode_path), "--install-extension", str(vsix_file), "--force"]
            
            # 执行安装
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(f"✅ 安装成功: {vsix_file.name}")
                success_count += 1
            else:
                print(f"❌ 安装失败: {vsix_file.name}")
                if result.stderr:
                    print(f"   错误信息: {result.stderr.strip()}")
                if result.stdout:
                    print(f"   输出信息: {result.stdout.strip()}")
            
        except subprocess.TimeoutExpired:
            print(f"⚠️ 安装超时: {vsix_file.name}")
        except Exception as e:
            print(f"❌ 安装出错 {vsix_file.name}: {e}")
        
        # 每个插件安装后稍作等待
        if i < len(vsix_files):
            time.sleep(2)
    
    print()
    print("=" * 60)
    print(f"插件安装结果: {success_count}/{len(vsix_files)} 成功")
    
    if success_count > 0:
        print("✅ 部分或全部插件安装成功!")
        print("💡 建议重启VSCode以确保插件正常加载")
    else:
        print("❌ 所有插件安装失败")
        print("💡 手动安装方法:")
        print("   1. 打开VSCode")
        print("   2. 按Ctrl+Shift+P打开命令面板")
        print("   3. 输入'Extensions: Install from VSIX...'")
        print(f"   4. 选择VSIX文件夹: {vsix_folder}")
    
    return success_count > 0


def main():
    """主函数"""
    try:
        success = install_plugins()
        if success:
            print("\n🎉 插件安装完成!")
        else:
            print("\n❌ 插件安装失败!")
    except KeyboardInterrupt:
        print("\n⚠️ 用户取消操作")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
    
    print("\n按任意键退出...")
    try:
        input()
    except:
        time.sleep(3)


if __name__ == "__main__":
    main()
