import requests
import json

# 测试配置
API_BASE_URL = 'https://yi.yiohyi.top'
API_PATH = '/api/v1/users/profile'

# 使用上次登录获取的令牌
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDc3MzAxOTksInN1YiI6IjY4MmMzMGY0NDdhOTYwMmU4MzAxMDEyZCJ9.pVCpN1ajDWO0xfB27hIc1nSx-zAN49LBdyYNRta19vU"

def test_get_profile():
    """测试获取用户个人资料"""
    print("正在测试获取用户个人资料...")
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    try:
        response = requests.get(f"{API_BASE_URL}{API_PATH}", headers=headers)
        
        # 打印响应信息
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("获取用户资料成功!")
            return True
        else:
            print(f"获取用户资料失败: HTTP {response.status_code}")
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
    test_get_profile() 