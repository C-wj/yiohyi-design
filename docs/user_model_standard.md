# 用户模型标准化方案

## 问题分析

当前系统中用户模型存在以下问题：

1. **模型定义冗余**: 在 `app.models.user` 和 `app.schemas.user` 两个模块中均定义了用户相关模型，导致代码冗余和可能的不一致。

2. **命名不一致**: 存在混用驼峰式命名 (`lastLogin`) 和下划线命名 (`last_login`) 的情况。

3. **模型结构不一致**: 
   - 在某些地方使用嵌套的 `profile` 对象
   - 在其他地方直接使用顶层属性如 `nickname`

4. **引用混乱**: 
   - 部分代码引用 `models.user.UserModel`（实际不存在该类）
   - 部分代码引用 `schemas.user.UserResponse`

5. **默认值处理不一致**: 
   - 有些接口为缺失字段提供默认值
   - 有些接口返回null/空字符串

## 解决方案

### 1. 模型定义职责分离

按照以下原则重构用户模型:

- **app.models.user**: 仅定义数据库表示模型
  - `User`: 完整的用户数据库模型
  - 枚举类型: `Gender`, `UserRole` 等

- **app.schemas.user**: 定义API请求/响应模型
  - 请求模型：`UserCreate`, `UserUpdate` 等
  - 响应模型：`UserResponse`, `UserProfileResponse` 等
  - 基础模型: `UserProfileBase`, `UserPreferencesBase` 等

### 2. 命名规范统一

- 所有Python代码使用下划线命名法 (`snake_case`)
- 所有JSON响应字段使用驼峰命名法 (`camelCase`)，通过Pydantic的`alias`特性实现

```python
class UserResponse(BaseModel):
    user_id: str = Field(..., alias="userId")
    
    class Config:
        allow_population_by_field_name = True
```

### 3. 模型结构统一

用户模型应采用以下统一结构:

```
User
├── id: str
├── openid: str
├── unionid: Optional[str]
├── profile: UserProfile
│   ├── nickname: str
│   ├── avatar: Optional[str]
│   ├── gender: Gender
│   ├── bio: Optional[str]
│   └── ...
├── preferences: UserPreferences
│   ├── dietary: List[str]
│   ├── allergies: List[str]
│   └── ...
├── stats: UserStats
│   ├── recipe_count: int
│   ├── favorite_count: int
│   └── ...
├── settings: UserSettings
│   ├── notification: bool
│   ├── privacy: str
│   └── ...
├── roles: List[UserRole]
├── is_active: bool
├── is_verified: bool
├── created_at: datetime
├── updated_at: datetime
└── last_login: Optional[datetime]
```

### 4. 代码引用修正

1. 扫描所有引用 `UserModel` 的地方，将其替换为正确的类名
2. 确保所有文件使用正确的导入路径
3. 移除不再使用的模型类定义

### 5. 默认值处理统一

- **原则**: API返回字段仅包含实际存在的数据，不为空字段提供默认值
- **实现**: 在序列化时移除值为None的字段

```python
user_data = {k: v for k, v in user_data.items() if v is not None}
```

## 迁移策略

1. 首先更新 `app.schemas.user`，确保它定义了所有需要的API模型
2. 更新 `app.models.user`，确保它定义了正确的数据库模型
3. 更新服务层函数，确保它们返回一致的数据结构
4. 更新API接口，使用正确的响应模型
5. 全局搜索并替换不正确的引用

## API接口规范

所有用户相关接口应返回一致的数据结构:

```json
{
  "code": 0,
  "data": {
    "id": "507f1f77bcf86cd799439011",
    "openid": "oLKQZ5R-VWyZM0VowVZsdQZfS_UM",
    "profile": {
      "nickname": "张三",
      "avatar": "https://example.com/avatar.jpg"
      // 其他字段...
    },
    // 其他字段...
  },
  "msg": "success"
} 