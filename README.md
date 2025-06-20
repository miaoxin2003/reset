# VSCode重置工具 - 升级版

## 功能概述

这是一个升级版的VSCode重置工具，不仅包含原有的重置功能，还新增了以下特性：

1. **自动运行Augment程序** - 以管理员权限运行指定的Augment安装程序
2. **完全重置VSCode** - 删除所有VSCode配置、扩展、缓存等
3. **自动安装插件** - 重置后自动安装指定的VSIX插件文件

## 文件结构

```
stable/
├── vscode_reset_stable.py    # 主程序文件
├── build_stable.py          # 构建脚本
├── config.json              # 配置文件
├── README.md               # 说明文档
└── test_upgraded.bat       # 测试脚本（构建后生成）
```

## 配置文件说明

`config.json` 包含以下配置项：

- `augment_exe_path`: Augment程序的完整路径
- `vsix_folder_path`: VSIX插件文件夹路径
- `log_file_name`: 日志文件名
- `settings`: 各种超时和等待时间设置
- `messages`: 用户界面消息文本

## 使用方法

### 构建可执行文件

```bash
python build_stable.py
```

### 运行程序

1. **完整升级流程**（推荐）：
   ```bash
   VSCode重置工具升级版.exe
   ```

2. **仅显示路径**：
   ```bash
   VSCode重置工具升级版.exe -s
   ```

3. **显示帮助**：
   ```bash
   VSCode重置工具升级版.exe -h
   ```

4. **仅执行重置**：
   ```bash
   VSCode重置工具升级版.exe --reset
   ```

5. **仅运行Augment**：
   ```bash
   VSCode重置工具升级版.exe --augment
   ```

6. **仅安装插件**：
   ```bash
   VSCode重置工具升级版.exe --plugins
   ```

## 升级流程详解

完整的升级流程包括以下步骤：

1. **关闭VSCode进程** - 确保VSCode完全关闭
2. **运行Augment安装程序** - 以管理员权限运行
3. **重置VSCode配置** - 删除所有用户数据
4. **等待重置完成** - 确保文件系统操作完成
5. **安装VSIX插件** - 自动安装指定插件

## 支持的插件

当前配置支持安装以下插件：

- `augment.vscode-augment-0.479.0.vsix`
- `ms-python.debugpy-2025.9.2025053001.vsix`
- `ms-python.python-2025.7.2025060501@alpine-arm64.vsix`
- `ms-python.vscode-pylance-2025.5.103.vsix`

## 注意事项

1. **管理员权限**：程序需要管理员权限才能正常运行
2. **路径配置**：确保配置文件中的路径正确
3. **备份重要数据**：重置操作会删除所有VSCode配置
4. **杀毒软件**：可能需要将程序添加到杀毒软件白名单
5. **日志文件**：查看 `vscode_reset_log.txt` 了解详细执行过程

## 故障排除

如果遇到问题，请检查：

1. 是否以管理员身份运行
2. Augment程序路径是否正确
3. VSIX文件夹是否存在且包含插件文件
4. 查看日志文件了解具体错误信息
5. 检查杀毒软件是否拦截程序运行

## 技术特性

- **跨平台支持**：Windows、macOS、Linux
- **智能路径检测**：自动识别VSCode安装路径
- **安全删除**：处理只读文件和权限问题
- **详细日志**：记录所有操作过程
- **配置化**：通过JSON文件灵活配置
- **错误处理**：完善的异常处理机制
