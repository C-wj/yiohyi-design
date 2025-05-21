const request = require('request-promise-native');

// 测试配置
const API_BASE_URL = 'https://yi.yiohyi.top';
const LOGIN_API = '/api/v1/auth/login';
const PROFILE_API = '/api/v1/users/profile';

// 测试账号
const TEST_ACCOUNT = {
  account: "testuser7371",  // 最近测试中使用的账号
  password: "Test12345"
};

async function testLoginFlow() {
  console.log("=== 开始测试登录流程 ===");
  console.log(`1. 尝试使用账号 ${TEST_ACCOUNT.account} 登录...`);
  
  try {
    // 第一步：登录
    const loginResponse = await request({
      method: 'POST',
      uri: `${API_BASE_URL}${LOGIN_API}`,
      body: TEST_ACCOUNT,
      json: true
    });
    
    console.log("登录成功！");
    console.log("响应数据:", JSON.stringify(loginResponse, null, 2));
    
    if (!loginResponse.access_token) {
      console.error("错误：响应中没有access_token");
      return;
    }
    
    const accessToken = loginResponse.access_token;
    console.log(`获取到的访问令牌: ${accessToken.substring(0, 15)}...`);
    
    // 第二步：获取用户资料
    console.log("\n2. 尝试获取用户资料...");
    const profileResponse = await request({
      method: 'GET',
      uri: `${API_BASE_URL}${PROFILE_API}`,
      headers: {
        'Authorization': `Bearer ${accessToken}`
      },
      json: true
    });
    
    console.log("获取用户资料成功！");
    console.log("响应数据:", JSON.stringify(profileResponse, null, 2));
    
    // 检查获取的用户资料
    if (profileResponse.status === 'success' && profileResponse.data) {
      const userData = profileResponse.data;
      console.log("\n用户信息摘要:");
      console.log(`- 用户名: ${userData.id}`);
      console.log(`- 昵称: ${userData.profile?.nickname || '未设置'}`);
      console.log(`- 头像: ${userData.profile?.avatar || '未设置'}`);
      console.log(`- 菜谱数: ${userData.stats?.recipe_count || 0}`);
      console.log(`- 角色: ${userData.roles?.join(', ') || '普通用户'}`);
    } else {
      console.error("错误：响应格式不符合预期");
    }
    
    console.log("\n=== 登录流程测试完成 ===");
    
  } catch (error) {
    console.error("测试过程中出错:", error.message);
    if (error.response) {
      console.error("错误响应:", error.response.body);
    }
  }
}

testLoginFlow().catch(console.error); 