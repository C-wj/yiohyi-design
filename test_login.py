import requests
import json

# 测试配置
API_BASE_URL = 'https://yi.yiohyi.top'
API_PATH = '/api/v1/auth/login'

# 使用刚刚创建的测试账号
login_data = {
    "account": "testuser7371",  # 刚刚注册成功的用户名
    "password": "Test12345"
}

def test_login():
    """测试登录功能"""
    print("正在测试登录功能...")
    print(f"登录数据: {json.dumps(login_data, ensure_ascii=False)}")
    
    try:
        response = requests.post(f"{API_BASE_URL}{API_PATH}", json=login_data)
        
        # 打印响应信息
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("登录成功!")
            
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
            print(f"登录失败: HTTP {response.status_code}")
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
    test_login() 