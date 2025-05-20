const axios = require('axios');

// 测试配置
const API_BASE_URL = 'http://localhost:8000';  // 修改为你的后端API地址
const API_PATH = '/auth/register';

// 模拟注册数据
const registerData = {
  username: 'testuser' + Math.floor(Math.random() * 10000),
  password: 'Test12345',
  nickname: '测试用户',
  email: `test${Math.floor(Math.random() * 10000)}@example.com`,
  phone: `1351234${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`
};

// 测试注册功能
async function testRegister() {
  console.log('正在测试注册功能...');
  console.log('注册数据:', registerData);
  
  try {
    const response = await axios.post(`${API_BASE_URL}${API_PATH}`, registerData);
    console.log('注册成功!');
    console.log('响应状态:', response.status);
    console.log('响应数据:', response.data);
    
    // 检查返回的令牌
    if (response.data && response.data.access_token) {
      console.log('令牌验证: ✓');
    } else {
      console.log('令牌验证: ✗ - 没有收到有效的访问令牌');
    }
    
    return response.data;
  } catch (error) {
    console.error('注册失败!');
    
    if (error.response) {
      console.error('响应状态:', error.response.status);
      console.error('错误详情:', error.response.data);
    } else if (error.request) {
      console.error('没有收到响应，可能是服务器未运行或网络问题');
    } else {
      console.error('请求配置错误:', error.message);
    }
    
    throw error;
  }
}

// 执行测试
testRegister()
  .then(() => {
    console.log('测试完成!');
  })
  .catch(() => {
    console.log('测试失败!');
  }); 