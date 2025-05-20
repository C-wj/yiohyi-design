import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime
from bson import ObjectId
import jwt

# Create a password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def get_password_hash(password):
    return pwd_context.hash(password)

async def connect_to_mongo():
    print("当前工作目录:", os.getcwd())
    env_file = os.path.exists(".env")
    print("env文件是否存在:", env_file)
    
    if env_file:
        print("env文件内容:")
        with open(".env", "r") as f:
            content = f.read()
            print(" " + content)
            
            # 提取JWT密钥
            for line in content.split('\n'):
                if line.startswith('JWT_SECRET_KEY='):
                    global jwt_secret_key
                    jwt_secret_key = line.split('=')[1].strip().strip('"')
                    print(f"JWT密钥: {jwt_secret_key}")
    
    mongo_uri = os.environ.get("MONGODB_URI", "mongodb://yiohyi:yiohyi@192.168.1.18:27017/yiohyi")
    print("系统环境变量MONGODB_URI:", os.environ.get("MONGODB_URI"))
    client = AsyncIOMotorClient(mongo_uri)
    db = client.get_database("yiohyi")
    return db

async def get_collection(db, collection_name):
    return db[collection_name]

def create_token(user_id):
    # 创建一个测试JWT令牌
    payload = {"sub": str(user_id)}
    token = jwt.encode(payload, jwt_secret_key, algorithm="HS256")
    decoded = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
    print(f"创建令牌: {token}")
    print(f"解码令牌: {decoded}")
    print(f"令牌中的用户ID: {decoded['sub']}")

async def fix_user():
    db = await connect_to_mongo()
    users_collection = await get_collection(db, "users")
    
    # 获取当前用户
    users = await users_collection.find().to_list(10)
    print(f"当前用户: {len(users)} 个")
    for user in users:
        print(f"ID: {user['_id']}, ID类型: {type(user['_id'])}, Username: {user.get('username')}, Nickname: {user.get('profile', {}).get('nickname')}, OpenID: {user.get('openid')}, PasswordHash: {user.get('passwordHash') is not None}")
    
    if users:
        # 更新第一个用户
        user_id = users[0]["_id"]
        password_hash = get_password_hash("Password123")  # 设置一个已知的密码
        
        # 创建基本的用户资料 - 注意性别用枚举值
        profile = {
            "nickname": "测试用户12",
            "avatar": "",
            "bio": "这是一个测试账户",
            "gender": "unknown",  # 使用枚举值：unknown, male, female
            "location": ""
        }
        
        # 创建用户统计信息 - 包含所有必需字段
        stats = {
            "recipeCount": 0,
            "followingCount": 0,
            "followersCount": 0,
            "favoriteCount": 0,  # 必需字段
            "orderCount": 0,     # 必需字段
            "lastLogin": datetime.utcnow().isoformat()
        }
        
        # 检查是否存在openid, 如果不存在则添加一个测试openid
        update_data = {
            "username": "testuser123", 
            "is_active": True,
            "passwordHash": password_hash,  # 修改字段名为passwordHash
            "profile": profile,
            "stats": stats,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # 如果没有openid，添加一个模拟的openid
        user = users[0]
        if not user.get('openid'):
            update_data["openid"] = f"test_openid_{str(ObjectId())}"
            print(f"添加模拟OpenID: {update_data['openid']}")
        
        # 更新用户
        result = await users_collection.update_one(
            {"_id": user_id},
            {"$set": update_data}
        )
        
        print(f"更新结果: {result.modified_count} 个文档被修改")
        
        # 验证更新
        updated_user = await users_collection.find_one({"_id": user_id})
        print(f"更新后: ID: {updated_user['_id']}, Username: {updated_user.get('username')}, Nickname: {updated_user.get('profile', {}).get('nickname')}, OpenID: {updated_user.get('openid')}, PasswordHash: {updated_user.get('passwordHash') is not None}")
        
        # 测试令牌的创建和解析
        create_token(user_id)
        
        # 尝试模拟用户ID查询
        try:
            # 测试使用字符串ID查找
            str_id = str(user_id)
            print(f"使用字符串ID查找: {str_id}")
            user_by_str = await users_collection.find_one({"_id": str_id})
            print(f"通过字符串ID查找结果: {user_by_str is not None}")
            
            # 测试使用ObjectId查找
            obj_id = ObjectId(str_id)
            print(f"使用ObjectId查找: {obj_id}")
            user_by_obj = await users_collection.find_one({"_id": obj_id})
            print(f"通过ObjectId查找结果: {user_by_obj is not None}")
            
        except Exception as e:
            print(f"ID查询测试异常: {str(e)}")

if __name__ == "__main__":
    jwt_secret_key = "change_this_to_another_secure_random_string"
    asyncio.run(fix_user()) 