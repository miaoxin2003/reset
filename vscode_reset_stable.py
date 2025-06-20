#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VSCode 重置工具 - 2.0版本
彻底解决Augment进程清理问题的增强版
包含强化的文件删除机制和进程管理

版本: 2.0
主要改进:
- 彻底清理Augment相关进程
- 强化文件删除机制（重试+强制删除）
- 专门的Augment残留文件清理
- 深度优先删除顺序
- 增强的错误恢复能力
text1

"""

import os
import sys
import shutil
import platform
import subprocess
import time
import traceback
import ctypes
import json
from pathlib import Path


class VSCodeResetterUpgraded:
    def __init__(self):
        self.system = platform.system()
        self.user_home = Path.home()
        self.config = self._load_config()
        self.log_file = Path(self.config.get("log_file_name", "vscode_reset_log.txt"))
        self.augment_exe = Path(self.config.get("augment_exe_path", r"C:\Users\baishui\Desktop\augment-vip-windows-x86_64.exe"))
        self.vsix_folder = Path(self.config.get("vsix_folder_path", r"C:\Users\baishui\Desktop\code_baishui\vsix"))
        self.settings = self.config.get("settings", {})
        self.messages = self.config.get("messages", {})
        self.vscode_exe = None
        self._find_vscode_executable()

    def _load_config(self):
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
            "augment_exe_path": r"C:\Users\baishui\Desktop\augment-vip-windows-x86_64.exe",
            "vsix_folder_path": r"C:\Users\baishui\Desktop\code_baishui\vsix",
            "log_file_name": "vscode_reset_log.txt",
            "settings": {
                "wait_after_augment": 5,
                "wait_after_reset": 3,
                "install_timeout": 60,
                "process_kill_timeout": 10
            },
            "messages": {
                "warning": "警告: 此操作将执行完整的VSCode升级流程!",
                "description": "包括: 运行Augment、重置VSCode、安装插件",
                "success": "🎉 VSCode升级流程完成!",
                "restart_suggestion": "建议重启VSCode以确保所有更改生效"
            }
        }

    def _find_vscode_executable(self):
        """查找VSCode可执行文件"""
        try:
            if self.system == "Windows":
                # 常见的VSCode安装路径
                possible_paths = [
                    Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs' / 'Microsoft VS Code' / 'Code.exe',
                    Path(os.environ.get('PROGRAMFILES', '')) / 'Microsoft VS Code' / 'Code.exe',
                    Path(os.environ.get('PROGRAMFILES(X86)', '')) / 'Microsoft VS Code' / 'Code.exe',
                ]

                for path in possible_paths:
                    if path.exists():
                        self.vscode_exe = path
                        break

                # 如果没找到，尝试从PATH中查找
                if not self.vscode_exe:
                    try:
                        result = subprocess.run(['where', 'code'], capture_output=True, text=True, check=True)
                        if result.stdout.strip():
                            self.vscode_exe = Path(result.stdout.strip().split('\n')[0])
                    except:
                        pass
            else:
                # Unix-like系统
                try:
                    result = subprocess.run(['which', 'code'], capture_output=True, text=True, check=True)
                    if result.stdout.strip():
                        self.vscode_exe = Path(result.stdout.strip())
                except:
                    pass

        except Exception as e:
            self.log(f"查找VSCode可执行文件时出错: {e}")

    def is_admin(self):
        """检查是否以管理员身份运行"""
        try:
            if self.system == "Windows":
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except:
            return False

    def run_as_admin(self, command, args=None):
        """以管理员身份运行程序"""
        try:
            if self.system == "Windows":
                if args:
                    params = ' '.join([f'"{arg}"' if ' ' in str(arg) else str(arg) for arg in args])
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", str(command), params, None, 1
                    )
                else:
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", str(command), None, None, 1
                    )
                return True
            else:
                # Unix-like系统使用sudo
                if args:
                    subprocess.run(['sudo', str(command)] + [str(arg) for arg in args], check=True)
                else:
                    subprocess.run(['sudo', str(command)], check=True)
                return True
        except Exception as e:
            self.log(f"以管理员身份运行失败: {e}")
            return False

    def log(self, message):
        """记录日志"""
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            
            # 打印到控制台
            print(message)
            
            # 写入日志文件
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_message)
        except Exception as e:
            print(f"日志记录失败: {e}")
    
    def get_vscode_paths(self):
        """获取VSCode路径 - 按删除优先级排序"""
        all_paths = []

        try:
            if self.system == "Windows":
                appdata = os.environ.get('APPDATA', '')
                localappdata = os.environ.get('LOCALAPPDATA', '')

                # 收集所有可能的路径
                potential_paths = []

                if appdata:
                    base_code_path = Path(appdata) / 'Code'
                    if base_code_path.exists():
                        # 递归收集所有子路径
                        for root, dirs, files in os.walk(base_code_path):
                            root_path = Path(root)
                            # 添加所有文件
                            for file in files:
                                potential_paths.append(root_path / file)
                            # 添加所有目录
                            for dir in dirs:
                                potential_paths.append(root_path / dir)
                        # 添加根目录
                        potential_paths.append(base_code_path)

                if localappdata:
                    base_local_code_path = Path(localappdata) / 'Code'
                    if base_local_code_path.exists():
                        # 递归收集所有子路径
                        for root, dirs, files in os.walk(base_local_code_path):
                            root_path = Path(root)
                            # 添加所有文件
                            for file in files:
                                potential_paths.append(root_path / file)
                            # 添加所有目录
                            for dir in dirs:
                                potential_paths.append(root_path / dir)
                        # 添加根目录
                        potential_paths.append(base_local_code_path)

                # 添加用户目录下的.vscode
                vscode_user_path = Path(self.user_home) / '.vscode'
                if vscode_user_path.exists():
                    for root, dirs, files in os.walk(vscode_user_path):
                        root_path = Path(root)
                        # 添加所有文件
                        for file in files:
                            potential_paths.append(root_path / file)
                        # 添加所有目录
                        for dir in dirs:
                            potential_paths.append(root_path / dir)
                    # 添加根目录
                    potential_paths.append(vscode_user_path)

                all_paths = potential_paths

            elif self.system == "Darwin":  # macOS
                base_paths = [
                    self.user_home / 'Library' / 'Application Support' / 'Code',
                    self.user_home / 'Library' / 'Logs' / 'Code',
                    self.user_home / 'Library' / 'Caches' / 'com.microsoft.VSCode',
                    self.user_home / '.vscode',
                ]

                for base_path in base_paths:
                    if base_path.exists():
                        if base_path.is_file():
                            all_paths.append(base_path)
                        else:
                            for root, dirs, files in os.walk(base_path):
                                root_path = Path(root)
                                for file in files:
                                    all_paths.append(root_path / file)
                                for dir in dirs:
                                    all_paths.append(root_path / dir)
                            all_paths.append(base_path)

            else:  # Linux
                config_home = os.environ.get('XDG_CONFIG_HOME', self.user_home / '.config')
                cache_home = os.environ.get('XDG_CACHE_HOME', self.user_home / '.cache')

                base_paths = [
                    Path(config_home) / 'Code',
                    Path(cache_home) / 'vscode',
                    self.user_home / '.vscode',
                ]

                for base_path in base_paths:
                    if base_path.exists():
                        if base_path.is_file():
                            all_paths.append(base_path)
                        else:
                            for root, dirs, files in os.walk(base_path):
                                root_path = Path(root)
                                for file in files:
                                    all_paths.append(root_path / file)
                                for dir in dirs:
                                    all_paths.append(root_path / dir)
                            all_paths.append(base_path)

            # 去重并按路径深度排序（深度优先删除）
            unique_paths = list(set(all_paths))
            # 按路径长度降序排序，确保先删除深层文件/目录
            unique_paths.sort(key=lambda p: len(str(p)), reverse=True)

            return [p for p in unique_paths if p.exists()]

        except Exception as e:
            self.log(f"获取路径时出错: {e}")
            return []
    
    def kill_vscode_processes(self):
        """关闭VSCode和Augment相关进程"""
        try:
            self.log("正在关闭VSCode和Augment相关进程...")

            if self.system == "Windows":
                # 要关闭的进程列表
                processes_to_kill = [
                    'Code.exe',
                    'Code - Insiders.exe',
                    'augment.exe',
                    'augment-vip-windows-x86_64.exe',
                    'node.exe',  # VSCode的Node.js进程
                    'electron.exe',  # Electron进程
                ]

                # 关闭每个进程
                for process_name in processes_to_kill:
                    try:
                        result = subprocess.run(['taskkill', '/F', '/IM', process_name],
                                              capture_output=True, text=True, check=False)
                        if result.returncode == 0:
                            self.log(f"✓ 已关闭进程: {process_name}")
                        elif "找不到该进程" not in result.stderr and "not found" not in result.stderr.lower():
                            self.log(f"⚠️ 关闭进程 {process_name} 时出现问题: {result.stderr.strip()}")
                    except Exception as e:
                        self.log(f"⚠️ 关闭进程 {process_name} 时出错: {e}")

                # 额外关闭包含特定关键词的进程
                try:
                    # 查找并关闭包含"augment"的进程
                    result = subprocess.run(['wmic', 'process', 'where', 'name like "%augment%"', 'delete'],
                                          capture_output=True, text=True, check=False)
                    if result.returncode == 0 and "deleted successfully" in result.stdout.lower():
                        self.log("✓ 已关闭所有Augment相关进程")
                except:
                    pass

            else:
                # Unix-like系统
                processes_to_kill = ['code', 'augment', 'electron', 'node']
                for process_name in processes_to_kill:
                    try:
                        subprocess.run(['pkill', '-f', process_name],
                                     capture_output=True, check=False)
                        self.log(f"✓ 已关闭进程: {process_name}")
                    except:
                        pass

            # 等待进程完全关闭
            time.sleep(3)
            self.log("VSCode和Augment进程关闭完成")

        except Exception as e:
            self.log(f"关闭进程时出错: {e}")
    
    def run_augment_installer(self):
        """运行Augment安装程序"""
        try:
            self.log("=" * 50)
            self.log("开始运行Augment安装程序")
            self.log("=" * 50)

            if not self.augment_exe.exists():
                self.log(f"❌ Augment安装程序不存在: {self.augment_exe}")
                return False

            self.log(f"📁 Augment程序路径: {self.augment_exe}")

            # 检查是否需要管理员权限
            if not self.is_admin():
                self.log("⚠️ 当前不是管理员权限，尝试以管理员身份运行Augment...")
                if self.run_as_admin(self.augment_exe):
                    self.log("✅ 已请求管理员权限运行Augment")
                    # 等待用户完成安装
                    self.log("请在弹出的窗口中完成Augment安装，完成后按任意键继续...")
                    try:
                        input()
                    except:
                        time.sleep(10)
                    return True
                else:
                    self.log("❌ 无法以管理员身份运行Augment")
                    return False
            else:
                # 已经是管理员，直接运行
                self.log("✅ 当前已是管理员权限，直接运行Augment...")
                try:
                    process = subprocess.Popen([str(self.augment_exe)],
                                             shell=True,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)

                    self.log("Augment安装程序已启动，等待完成...")
                    _, stderr = process.communicate()

                    if process.returncode == 0:
                        self.log("✅ Augment安装完成")
                        return True
                    else:
                        self.log(f"⚠️ Augment安装可能有问题，返回码: {process.returncode}")
                        if stderr:
                            self.log(f"错误信息: {stderr.decode('utf-8', errors='ignore')}")
                        return True  # 即使有警告也继续

                except Exception as e:
                    self.log(f"❌ 运行Augment时出错: {e}")
                    return False

        except Exception as e:
            self.log(f"❌ Augment安装过程出错: {e}")
            return False

    def find_vscode_after_reset(self):
        """重置后重新查找VSCode可执行文件"""
        try:
            if self.system == "Windows":
                # 常见的VSCode安装路径
                possible_paths = [
                    Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs' / 'Microsoft VS Code' / 'Code.exe',
                    Path(os.environ.get('PROGRAMFILES', '')) / 'Microsoft VS Code' / 'Code.exe',
                    Path(os.environ.get('PROGRAMFILES(X86)', '')) / 'Microsoft VS Code' / 'Code.exe',
                    Path("C:\\Program Files\\Microsoft VS Code\\Code.exe"),
                    Path("C:\\Program Files (x86)\\Microsoft VS Code\\Code.exe"),
                    Path("C:\\D\\Microsoft VS Code\\Code.exe"),  # 添加D盘路径
                ]

                for path in possible_paths:
                    if path.exists():
                        self.log(f"✅ 找到VSCode: {path}")
                        return path

                # 尝试从PATH中查找，但要转换为真正的exe路径
                try:
                    result = subprocess.run(['where', 'code'], capture_output=True, text=True, check=True)
                    if result.stdout.strip():
                        code_path = Path(result.stdout.strip().split('\n')[0])
                        self.log(f"🔍 从PATH找到: {code_path}")

                        # 如果找到的是bin/code，转换为真正的Code.exe路径
                        if code_path.name == 'code' and 'bin' in str(code_path):
                            # 从 C:\D\Microsoft VS Code\bin\code 转换为 C:\D\Microsoft VS Code\Code.exe
                            vscode_root = code_path.parent.parent
                            real_exe = vscode_root / 'Code.exe'
                            if real_exe.exists():
                                self.log(f"✅ 转换为真正的VSCode路径: {real_exe}")
                                return real_exe
                            else:
                                self.log(f"⚠️ 未找到真正的Code.exe: {real_exe}")

                        # 如果直接是exe文件
                        elif code_path.suffix.lower() == '.exe' and code_path.exists():
                            self.log(f"✅ 从PATH找到VSCode: {code_path}")
                            return code_path
                except Exception as e:
                    self.log(f"从PATH查找时出错: {e}")

                # 尝试通过注册表查找
                try:
                    import winreg
                    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                if "code" in subkey_name.lower():
                                    with winreg.OpenKey(key, subkey_name) as subkey:
                                        try:
                                            install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                            code_exe = Path(install_location) / "Code.exe"
                                            if code_exe.exists():
                                                self.log(f"✅ 从注册表找到VSCode: {code_exe}")
                                                return code_exe
                                        except:
                                            continue
                            except:
                                continue
                except:
                    pass

            return None

        except Exception as e:
            self.log(f"查找VSCode时出错: {e}")
            return None

    def install_vsix_extensions(self):
        """安装VSIX插件 - 增强版"""
        try:
            self.log("=" * 50)
            self.log("开始安装VSCode插件")
            self.log("=" * 50)

            # 首先检查配置文件中是否指定了VSCode路径
            vscode_path = None
            if "vscode_exe_path" in self.config:
                config_path = Path(self.config["vscode_exe_path"])
                if config_path.exists():
                    vscode_path = config_path
                    self.log(f"✅ 使用配置文件中的VSCode路径: {vscode_path}")
                else:
                    self.log(f"⚠️ 配置文件中的VSCode路径不存在: {config_path}")

            # 如果配置文件中没有或路径无效，则自动查找
            if not vscode_path:
                vscode_path = self.find_vscode_after_reset()

            if not vscode_path:
                self.log("❌ 未找到VSCode可执行文件")
                self.log("💡 可能的解决方案:")
                self.log("  1. 重新安装VSCode")
                self.log("  2. 手动安装插件：打开VSCode -> Ctrl+Shift+P -> Extensions: Install from VSIX")
                self.log("  3. 检查VSCode是否在PATH环境变量中")
                return False

            if not self.vsix_folder.exists():
                self.log(f"❌ VSIX文件夹不存在: {self.vsix_folder}")
                return False

            # 获取所有VSIX文件
            vsix_files = list(self.vsix_folder.glob("*.vsix"))
            if not vsix_files:
                self.log("❌ 未找到VSIX插件文件")
                return False

            self.log(f"发现 {len(vsix_files)} 个插件文件:")
            for vsix_file in vsix_files:
                self.log(f"  - {vsix_file.name}")

            # 等待VSCode完全启动
            self.log("⏳ 等待VSCode服务准备就绪...")
            time.sleep(3)

            # 安装每个插件
            success_count = 0
            for vsix_file in vsix_files:
                try:
                    self.log(f"正在安装: {vsix_file.name}")

                    # 使用完整路径和正确的参数
                    cmd = [str(vscode_path), "--install-extension", str(vsix_file), "--force"]
                    timeout = self.settings.get("install_timeout", 120)  # 增加超时时间

                    # 设置环境变量，避免VSCode启动界面和权限问题
                    env = os.environ.copy()
                    env['VSCODE_CLI'] = '1'

                    # 如果是管理员身份运行，尝试以普通用户身份执行VSCode命令
                    if self.is_admin():
                        self.log("⚠️ 检测到管理员权限，尝试以普通用户身份安装插件...")
                        try:
                            # 方法1：使用runas命令以当前用户身份运行
                            runas_cmd = ['runas', '/trustlevel:0x20000', ' '.join([f'"{str(vscode_path)}"', "--install-extension", f'"{str(vsix_file)}"', "--force"])]
                            result = subprocess.run(runas_cmd, capture_output=True, text=True,
                                                  timeout=timeout, env=env, shell=True)

                            if result.returncode != 0:
                                # 方法2：直接运行，忽略权限警告
                                self.log("⚠️ runas方法失败，尝试直接运行...")
                                result = subprocess.run(cmd, capture_output=True, text=True,
                                                      timeout=timeout, env=env)
                        except:
                            # 如果runas失败，回退到直接运行
                            result = subprocess.run(cmd, capture_output=True, text=True,
                                                  timeout=timeout, env=env)
                    else:
                        # 普通用户权限，直接运行
                        result = subprocess.run(cmd, capture_output=True, text=True,
                                              timeout=timeout, env=env)

                    if result.returncode == 0:
                        self.log(f"✅ 安装成功: {vsix_file.name}")
                        success_count += 1
                    else:
                        self.log(f"❌ 安装失败: {vsix_file.name}")
                        if result.stderr:
                            self.log(f"错误信息: {result.stderr}")
                        if result.stdout:
                            self.log(f"输出信息: {result.stdout}")

                except subprocess.TimeoutExpired:
                    self.log(f"⚠️ 安装超时: {vsix_file.name}")
                except Exception as e:
                    self.log(f"❌ 安装出错 {vsix_file.name}: {e}")

                # 每个插件安装后稍作等待
                time.sleep(2)

            self.log(f"插件安装结果: {success_count}/{len(vsix_files)} 成功")

            if success_count > 0:
                self.log("💡 建议:")
                self.log("  1. 重启VSCode以确保插件正常加载")
                self.log("  2. 检查VSCode扩展页面确认插件已安装")
                return True
            else:
                self.log("💡 手动安装方法:")
                self.log("  1. 打开VSCode")
                self.log("  2. 按Ctrl+Shift+P打开命令面板")
                self.log("  3. 输入'Extensions: Install from VSIX...'")
                self.log(f"  4. 选择VSIX文件夹: {self.vsix_folder}")
                return False

        except Exception as e:
            self.log(f"❌ 插件安装过程出错: {e}")
            return False

    def force_remove_file(self, file_path):
        """强制删除单个文件"""
        try:
            if not file_path.exists():
                return True

            # 移除只读属性
            if self.system == "Windows":
                try:
                    os.chmod(file_path, 0o777)
                    # 使用Windows API强制删除
                    import stat
                    os.chmod(file_path, stat.S_IWRITE)
                except:
                    pass

            # 尝试删除
            file_path.unlink()
            return True

        except Exception as e:
            # 最后尝试使用系统命令强制删除
            try:
                if self.system == "Windows":
                    subprocess.run(['del', '/F', '/Q', str(file_path)],
                                 shell=True, capture_output=True, check=False)
                else:
                    subprocess.run(['rm', '-f', str(file_path)],
                                 capture_output=True, check=False)
                return not file_path.exists()
            except:
                return False

    def safe_remove(self, path):
        """安全删除文件或目录 - 增强版"""
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                if not path.exists():
                    return True

                if path.is_file():
                    # 删除文件
                    if self.force_remove_file(path):
                        self.log(f"✓ 删除文件: {path}")
                        return True
                    else:
                        raise Exception("文件删除失败")

                elif path.is_dir():
                    # 删除目录 - 从最深层开始
                    success = self._remove_directory_recursive(path)
                    if success:
                        self.log(f"✓ 删除目录: {path}")
                        return True
                    else:
                        raise Exception("目录删除失败")

            except Exception as e:
                if attempt < max_retries - 1:
                    self.log(f"⚠️ 删除失败 {path} (尝试 {attempt + 1}/{max_retries}): {e}")
                    self.log(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 指数退避
                else:
                    self.log(f"✗ 删除失败 {path} (所有尝试均失败): {e}")
                    return False

        return False

    def _remove_directory_recursive(self, dir_path):
        """递归删除目录，从最深层开始"""
        try:
            # 首先尝试标准删除
            try:
                shutil.rmtree(dir_path)
                return True
            except:
                pass

            # 如果标准删除失败，手动递归删除
            for root, dirs, files in os.walk(dir_path, topdown=False):
                # 删除所有文件
                for file in files:
                    file_path = Path(root) / file
                    try:
                        self.force_remove_file(file_path)
                    except:
                        # 尝试使用系统命令
                        if self.system == "Windows":
                            subprocess.run(['del', '/F', '/Q', str(file_path)],
                                         shell=True, capture_output=True, check=False)

                # 删除所有空目录
                for dir in dirs:
                    dir_path_full = Path(root) / dir
                    try:
                        if self.system == "Windows":
                            os.chmod(dir_path_full, 0o777)
                        dir_path_full.rmdir()
                    except:
                        # 尝试使用系统命令
                        if self.system == "Windows":
                            subprocess.run(['rmdir', '/S', '/Q', str(dir_path_full)],
                                         shell=True, capture_output=True, check=False)

            # 最后删除根目录
            try:
                if self.system == "Windows":
                    os.chmod(dir_path, 0o777)
                dir_path.rmdir()
                return True
            except:
                # 最后尝试使用系统命令
                if self.system == "Windows":
                    result = subprocess.run(['rmdir', '/S', '/Q', str(dir_path)],
                                          shell=True, capture_output=True, check=False)
                    return result.returncode == 0
                else:
                    result = subprocess.run(['rm', '-rf', str(dir_path)],
                                          capture_output=True, check=False)
                    return result.returncode == 0

        except Exception as e:
            self.log(f"递归删除目录时出错: {e}")
            return False

    def clean_augment_residuals(self):
        """专门清理Augment残留文件"""
        try:
            self.log("🧹 开始清理Augment残留文件...")

            # 常见的Augment残留路径
            augment_paths = []

            if self.system == "Windows":
                appdata = os.environ.get('APPDATA', '')
                localappdata = os.environ.get('LOCALAPPDATA', '')

                # 搜索包含augment的目录
                search_paths = [
                    Path(appdata) if appdata else None,
                    Path(localappdata) if localappdata else None,
                    Path(self.user_home) / 'AppData' / 'Roaming',
                    Path(self.user_home) / 'AppData' / 'Local',
                ]

                for search_path in search_paths:
                    if search_path and search_path.exists():
                        try:
                            # 查找包含augment的文件夹
                            for item in search_path.rglob("*augment*"):
                                if item.exists():
                                    augment_paths.append(item)
                        except Exception as e:
                            self.log(f"搜索 {search_path} 时出错: {e}")

            # 去重并排序
            unique_augment_paths = list(set(augment_paths))
            unique_augment_paths.sort(key=lambda p: len(str(p)), reverse=True)

            if not unique_augment_paths:
                self.log("✅ 未发现Augment残留文件")
                return True

            self.log(f"发现 {len(unique_augment_paths)} 个Augment相关路径:")
            for i, path in enumerate(unique_augment_paths[:5], 1):
                self.log(f"  {i}. {path}")
            if len(unique_augment_paths) > 5:
                self.log(f"  ... 还有 {len(unique_augment_paths) - 5} 个")

            # 删除Augment残留文件
            success_count = 0
            for path in unique_augment_paths:
                if self.safe_remove(path):
                    success_count += 1

            self.log(f"Augment残留清理结果: {success_count}/{len(unique_augment_paths)} 成功")
            return success_count > 0

        except Exception as e:
            self.log(f"清理Augment残留文件时出错: {e}")
            return False
    
    def reset_vscode(self):
        """重置VSCode - 增强版"""
        try:
            self.log("=" * 50)
            self.log("VSCode 重置工具 - 2.0版本")
            self.log("=" * 50)

            # 1. 多次关闭进程，确保彻底
            for i in range(3):
                self.log(f"第 {i+1} 次关闭进程...")
                self.kill_vscode_processes()
                time.sleep(2)

            # 2. 额外等待，确保所有进程完全关闭
            self.log("等待进程完全关闭...")
            time.sleep(5)

            # 3. 获取路径
            paths = self.get_vscode_paths()
            self.log(f"发现 {len(paths)} 个VSCode相关路径")

            if not paths:
                self.log("没有发现VSCode文件，可能已经清理干净")
                return True

            # 4. 显示前10个路径（避免日志过长）
            self.log("将要删除的路径（显示前10个）:")
            for i, path in enumerate(paths[:10], 1):
                self.log(f"  {i}. {path}")
            if len(paths) > 10:
                self.log(f"  ... 还有 {len(paths) - 10} 个路径")

            # 5. 分批删除文件，提供更好的进度反馈
            success_count = 0
            total_count = len(paths)

            self.log("开始删除文件和目录...")
            for i, path in enumerate(paths, 1):
                if i % 50 == 0 or i == total_count:  # 每50个或最后一个显示进度
                    self.log(f"进度: {i}/{total_count} ({i/total_count*100:.1f}%)")

                if self.safe_remove(path):
                    success_count += 1

            # 6. 验证删除结果
            self.log("验证删除结果...")
            remaining_paths = self.get_vscode_paths()

            # 7. 结果报告
            self.log(f"删除结果: {success_count}/{total_count} 成功")

            if remaining_paths:
                self.log(f"⚠️ 仍有 {len(remaining_paths)} 个路径未能删除:")
                for path in remaining_paths[:5]:  # 只显示前5个
                    self.log(f"  - {path}")
                if len(remaining_paths) > 5:
                    self.log(f"  ... 还有 {len(remaining_paths) - 5} 个")

                # 如果删除率超过80%，仍然认为是成功的
                success_rate = success_count / total_count
                if success_rate >= 0.8:
                    self.log(f"✅ VSCode重置基本完成! (成功率: {success_rate*100:.1f}%)")
                    return True
                else:
                    self.log(f"❌ VSCode重置失败! (成功率: {success_rate*100:.1f}%)")
                    return False
            else:
                self.log("✅ VSCode重置完全成功!")
                return True

        except Exception as e:
            self.log(f"重置过程中出错: {e}")
            self.log(f"错误详情: {traceback.format_exc()}")
            return False

    def full_upgrade_process(self):
        """完整的升级流程 - 简化版（不包含插件安装）"""
        try:
            self.log("🚀 开始VSCode完整升级流程")
            self.log("=" * 60)

            # 步骤1: 关闭VSCode和Augment进程（只执行一次）
            self.log("📋 步骤1: 关闭VSCode和Augment进程")
            self.kill_vscode_processes()
            self.log("等待进程完全关闭...")
            time.sleep(3)

            # 步骤2: 运行Augment安装程序
            self.log("📋 步骤2: 运行Augment安装程序")
            augment_success = self.run_augment_installer()
            if not augment_success:
                self.log("❌ Augment安装失败，但继续执行重置...")
            else:
                self.log("✅ Augment安装成功")
                # Augment安装后等待
                self.log("等待Augment安装完成...")
                time.sleep(3)

            # 步骤3: 清理Augment残留文件
            self.log("📋 步骤3: 清理Augment残留文件")
            augment_clean_success = self.clean_augment_residuals()
            if augment_clean_success:
                self.log("✅ Augment残留清理成功")
            else:
                self.log("⚠️ Augment残留清理失败或无残留文件")

            # 步骤4: 重置VSCode
            self.log("📋 步骤4: 重置VSCode配置")
            reset_success = self.reset_vscode()
            if not reset_success:
                self.log("❌ VSCode重置失败")
            else:
                self.log("✅ VSCode重置成功")

            # 步骤5: 等待重置完成
            wait_time = self.settings.get("wait_after_reset", 3)
            self.log(f"⏳ 等待重置完成... ({wait_time}秒)")
            time.sleep(wait_time)

            # 最终结果评估
            self.log("=" * 60)
            success_count = sum([augment_success, reset_success, augment_clean_success])
            total_steps = 3

            if success_count == total_steps:
                self.log("🎉 VSCode升级流程完全成功!")
                self.log("所有步骤都已成功完成")
            elif success_count >= 2:
                self.log("✅ VSCode升级流程基本成功!")
                self.log(f"成功完成 {success_count}/{total_steps} 个主要步骤")
            else:
                self.log("⚠️ VSCode升级流程部分成功")
                self.log(f"成功完成 {success_count}/{total_steps} 个主要步骤")

            # 插件安装提示
            self.log("")
            self.log("💡 插件安装说明:")
            self.log("  插件安装已从主流程中移除，请使用以下方法安装插件:")
            self.log("  方法1: 运行 install_plugins_normal_user.ps1 (推荐)")
            self.log("  方法2: 运行 python install_plugins_only.py")
            self.log("  方法3: 手动安装 - 打开VSCode -> Ctrl+Shift+P -> Extensions: Install from VSIX")

            self.log(self.messages.get("restart_suggestion", "建议重启VSCode以确保所有更改生效"))

            # 只要有任何步骤成功，就认为流程有效
            return success_count > 0

        except Exception as e:
            self.log(f"❌ 升级流程出错: {e}")
            self.log(f"错误详情: {traceback.format_exc()}")
            return False
    
    def show_paths(self):
        """显示路径"""
        try:
            self.log("VSCode 路径信息:")
            self.log("-" * 30)
            
            paths = self.get_vscode_paths()
            if not paths:
                self.log("没有发现VSCode文件")
                return
            
            for i, path in enumerate(paths, 1):
                self.log(f"{i:2d}. {path}")
                
        except Exception as e:
            self.log(f"显示路径时出错: {e}")


def main():
    """主函数 - 增强错误处理"""
    resetter = None

    try:
        # 创建重置器
        resetter = VSCodeResetterUpgraded()

        # 检查命令行参数
        if len(sys.argv) > 1:
            arg = sys.argv[1].lower()

            if arg in ['--show-paths', '-s']:
                resetter.show_paths()
                return
            elif arg in ['--help', '-h']:
                resetter.log("VSCode重置工具 - 2.0版本（简化版）")
                resetter.log("=" * 50)
                resetter.log("🚀 主要改进:")
                resetter.log("  ✅ 彻底清理Augment相关进程")
                resetter.log("  ✅ 强化文件删除机制（重试+强制删除）")
                resetter.log("  ✅ 专门的Augment残留文件清理")
                resetter.log("  ✅ 深度优先删除顺序")
                resetter.log("  ✅ 增强的错误恢复能力")
                resetter.log("  ✅ 移除插件自动安装（避免权限冲突）")
                resetter.log("")
                resetter.log("📋 使用方法:")
                resetter.log("  VSCode重置工具2.0版.exe              # 执行完整升级流程（不含插件安装）")
                resetter.log("  VSCode重置工具2.0版.exe -s           # 显示路径")
                resetter.log("  VSCode重置工具2.0版.exe -h           # 显示帮助")
                resetter.log("  VSCode重置工具2.0版.exe --reset      # 仅执行重置")
                resetter.log("  VSCode重置工具2.0版.exe --augment    # 仅运行Augment")
                resetter.log("")
                resetter.log("💡 插件安装:")
                resetter.log("  插件安装已移除，请使用以下独立工具:")
                resetter.log("  - install_plugins_normal_user.ps1 (推荐)")
                resetter.log("  - python install_plugins_only.py")
                return
            elif arg in ['--reset']:
                # 仅执行重置
                resetter.log("执行VSCode重置...")
                if resetter.reset_vscode():
                    resetter.log("重置完成!")
                else:
                    resetter.log("重置失败!")
                return
            elif arg in ['--augment']:
                # 仅运行Augment
                resetter.log("运行Augment安装程序...")
                if resetter.run_augment_installer():
                    resetter.log("Augment安装完成!")
                else:
                    resetter.log("Augment安装失败!")
                return


        # 执行完整升级流程
        resetter.log(resetter.messages.get("warning", "警告: 此操作将执行完整的VSCode升级流程!"))
        resetter.log("包括: 运行Augment、清理残留文件、重置VSCode配置")
        resetter.log("注意: 插件安装已移除，请使用独立工具安装插件")
        resetter.log("")
        resetter.log("开始执行升级流程...")

        if resetter.full_upgrade_process():
            resetter.log("升级流程完成!")
        else:
            resetter.log("升级流程失败!")
        
    except Exception as e:
        error_msg = f"程序运行出错: {e}"
        if resetter:
            resetter.log(error_msg)
            resetter.log(f"错误详情: {traceback.format_exc()}")
        else:
            print(error_msg)
            print(f"错误详情: {traceback.format_exc()}")
    
    finally:
        # 在打包环境中暂停
        try:
            if hasattr(sys, 'frozen') and sys.frozen:
                if resetter:
                    resetter.log("按任意键退出...")
                else:
                    print("按任意键退出...")
                
                # 尝试多种方式等待用户输入
                try:
                    input()
                except:
                    try:
                        import msvcrt
                        msvcrt.getch()
                    except:
                        time.sleep(5)  # 最后等待5秒
        except:
            pass


if __name__ == "__main__":
    main()
