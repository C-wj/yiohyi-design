#!/usr/bin/env python

"""
评论功能测试脚本
运行方式: python run_comment_tests.py
"""

import os
import sys
import subprocess

def main():
    """运行评论相关的测试"""
    os.environ["PYTHONPATH"] = os.getcwd()
    
    print("======= 开始运行评论功能测试 =======")
    
    # 运行 API 测试
    print("\n--- 运行 API 测试 ---")
    api_test_result = subprocess.run(
        ["pytest", "tests/api/v1/test_recipes.py", "-v"],
        capture_output=True,
        text=True
    )
    print(api_test_result.stdout)
    if api_test_result.stderr:
        print("错误信息:")
        print(api_test_result.stderr)
    
    # 运行服务层测试
    print("\n--- 运行服务层测试 ---")
    service_test_result = subprocess.run(
        ["pytest", "tests/services/test_comment.py", "-v"],
        capture_output=True,
        text=True
    )
    print(service_test_result.stdout)
    if service_test_result.stderr:
        print("错误信息:")
        print(service_test_result.stderr)
    
    # 输出测试总结
    print("\n======= 测试结果摘要 =======")
    if api_test_result.returncode == 0 and service_test_result.returncode == 0:
        print("✅ 所有测试通过！")
        return 0
    else:
        print("❌ 部分测试失败！")
        if api_test_result.returncode != 0:
            print("- API 测试失败")
        if service_test_result.returncode != 0:
            print("- 服务层测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 