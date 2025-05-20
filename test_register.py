import requests
import random
import json

# 测试配置
API_BASE_URL = 'https://yi.yiohyi.top'  # 修改为正确的后端API地址
API_PATH = '/api/v1/auth/register'

# 生成测试数据
username = f'testuser{random.randint(1000, 9999)}'
email = f'test{random.randint(1000, 9999)}@example.com'
phone = f'1351234{random.randint(1000, 9999):04d}'

# 模拟注册数据
register_data = {
    "username": username,
    "password": "Test12345",
    "nickname": "测试用户",
    "email": email,
    "phone": phone
}

def test_register():
    """测试注册功能"""
    print("正在测试注册功能...")
    print(f"注册数据: {json.dumps(register_data, ensure_ascii=False)}")
    
    try:
        response = requests.post(f"{API_BASE_URL}{API_PATH}", json=register_data)
        
        # 打印响应信息
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("注册成功!")
            
            # 解析响应JSON
            try:
                result = response.json()
                if 'access_token' in result:
                    print("令牌验证: ✓")
                    return True
                else:
                    print("令牌验证: ✗ - 没有收到有效的访问令牌")
            except json.JSONDecodeError:
                print("解析响应失败: 响应不是有效的JSON格式")
        else:
            print(f"注册失败: HTTP {response.status_code}")
            try:
                error = response.json()
                print(f"错误详情: {json.dumps(error, ensure_ascii=False)}")
            except:
                print(f"错误响应: {response.text}")
        
        return False
    except requests.RequestException as e:
        print(f"请求异常: {e}")
        return False

if __name__ == "__main__":
    test_register() 