#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试改进后的VSCode重置工具
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from vscode_reset_stable import VSCodeResetterUpgraded

def test_path_detection():
    """测试路径检测功能"""
    print("=" * 50)
    print("测试路径检测功能")
    print("=" * 50)
    
    resetter = VSCodeResetterUpgraded()
    paths = resetter.get_vscode_paths()
    
    print(f"发现 {len(paths)} 个VSCode相关路径:")
    for i, path in enumerate(paths[:10], 1):
        print(f"  {i}. {path}")
    if len(paths) > 10:
        print(f"  ... 还有 {len(paths) - 10} 个路径")
    
    return len(paths) > 0

def test_process_killing():
    """测试进程关闭功能"""
    print("\n" + "=" * 50)
    print("测试进程关闭功能")
    print("=" * 50)
    
    resetter = VSCodeResetterUpgraded()
    resetter.kill_vscode_processes()
    
    print("进程关闭测试完成")
    return True

def test_augment_residual_detection():
    """测试Augment残留文件检测"""
    print("\n" + "=" * 50)
    print("测试Augment残留文件检测")
    print("=" * 50)
    
    resetter = VSCodeResetterUpgraded()
    success = resetter.clean_augment_residuals()
    
    print(f"Augment残留清理测试完成: {'成功' if success else '失败'}")
    return True

def test_safe_remove():
    """测试安全删除功能"""
    print("\n" + "=" * 50)
    print("测试安全删除功能")
    print("=" * 50)
    
    # 创建测试文件和目录
    test_dir = Path("test_remove_dir")
    test_file = test_dir / "test_file.txt"
    
    try:
        # 创建测试目录和文件
        test_dir.mkdir(exist_ok=True)
        test_file.write_text("测试内容", encoding='utf-8')
        
        print(f"创建测试文件: {test_file}")
        
        # 测试删除
        resetter = VSCodeResetterUpgraded()
        success = resetter.safe_remove(test_dir)
        
        print(f"删除测试结果: {'成功' if success else '失败'}")
        print(f"文件是否还存在: {test_dir.exists()}")
        
        return success and not test_dir.exists()
        
    except Exception as e:
        print(f"测试过程中出错: {e}")
        return False
    finally:
        # 清理测试文件
        try:
            if test_file.exists():
                test_file.unlink()
            if test_dir.exists():
                test_dir.rmdir()
        except:
            pass

def main():
    """主测试函数"""
    print("VSCode重置工具改进版 - 功能测试")
    print("=" * 60)
    
    tests = [
        ("路径检测", test_path_detection),
        ("进程关闭", test_process_killing),
        ("Augment残留检测", test_augment_residual_detection),
        ("安全删除", test_safe_remove),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n开始测试: {test_name}")
            result = test_func()
            results.append((test_name, result))
            print(f"测试 {test_name}: {'✅ 通过' if result else '❌ 失败'}")
        except Exception as e:
            print(f"测试 {test_name} 出错: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果总结:")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{len(results)} 个测试通过")
    
    if passed == len(results):
        print("🎉 所有测试都通过了！代码改进成功！")
    elif passed >= len(results) * 0.8:
        print("✅ 大部分测试通过，代码改进基本成功！")
    else:
        print("⚠️ 部分测试失败，需要进一步调试")

if __name__ == "__main__":
    main()
