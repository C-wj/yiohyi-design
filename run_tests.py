#!/usr/bin/env python

"""
评论功能测试脚本
运行方式: python run_tests.py
"""

import os
import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="运行评论相关的测试")
    parser.add_argument("--api", action="store_true", help="只运行API测试")
    parser.add_argument("--service", action="store_true", help="只运行服务层测试")
    args = parser.parse_args()
    
    # 设置环境变量
    os.environ["PYTHONPATH"] = os.getcwd()
    
    print("======= 开始运行评论功能测试 =======")
    
    api_result = None
    service_result = None
    
    # 运行API测试
    if not args.service:
        print("\n--- 运行 API 测试 ---")
        api_test_cmd = ["python", "-m", "pytest", "tests/api/v1/test_recipes.py", "-v"]
        print(f"执行命令: {' '.join(api_test_cmd)}")
        
        api_result = subprocess.run(
            api_test_cmd,
            capture_output=True,
            text=True
        )
        print(api_result.stdout)
        if api_result.stderr:
            print("错误信息:")
            print(api_result.stderr)
    
    # 运行服务层测试
    if not args.api:
        print("\n--- 运行服务层测试 ---")
        service_test_cmd = ["python", "-m", "pytest", "tests/services/test_comment.py", "-v"]
        print(f"执行命令: {' '.join(service_test_cmd)}")
        
        service_result = subprocess.run(
            service_test_cmd,
            capture_output=True,
            text=True
        )
        print(service_result.stdout)
        if service_result.stderr:
            print("错误信息:")
            print(service_result.stderr)
    
    # 输出测试总结
    print("\n======= 测试结果摘要 =======")
    
    has_api = api_result is not None
    has_service = service_result is not None
    
    api_ok = has_api and api_result.returncode == 0
    service_ok = has_service and service_result.returncode == 0
    
    if (has_api and has_service and api_ok and service_ok) or \
       (has_api and not has_service and api_ok) or \
       (has_service and not has_api and service_ok):
        print("✅ 所有测试通过！")
        return 0
    else:
        print("❌ 部分测试失败！")
        if has_api and not api_ok:
            print("- API 测试失败")
        if has_service and not service_ok:
            print("- 服务层测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 