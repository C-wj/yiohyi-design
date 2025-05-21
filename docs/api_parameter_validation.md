# API参数校验规范

## 基本原则

1. **明确区分必填与非必填参数**
   - 必填参数：无默认值
   - 非必填参数：标记为`Optional`并提供默认值

2. **采用分层校验策略**
   - 类型校验：由Pydantic自动完成
   - 业务校验：使用validator装饰器实现

3. **规范错误信息**
   - 使用中文错误消息
   - 清晰具体指出错误原因

## 实现规范

### 模型定义

```python
from typing import Optional, List
from pydantic import BaseModel, Field, validator

class ApiModel(BaseModel):
    # 必填参数示例
    required_field: str
    
    # 非必填参数示例
    optional_field: Optional[str] = None
    optional_with_validation: Optional[str] = Field(None, min_length=3, max_length=50)
    optional_list: List[str] = Field(default_factory=list)
    
    @validator('required_field')
    def validate_required(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('不能为空')
        return v
```

### 路由处理器

```python
@router.post("/endpoint")
async def api_handler(data: ApiModel):
    # 只处理用户提供的字段
    data_dict = data.dict(exclude_unset=True)
    
    # 条件处理非必填参数
    if data.optional_field:
        # 处理可选字段
        pass

    # 返回统一格式响应
    return {
        "status": "success",
        "message": "操作成功",
        "data": result
    }
```

## 最佳实践

### 1. 参数验证

- **前置验证**：在使用前验证参数
- **条件验证**：对非必填字段进行条件检查
- **避免空值**：使用`if field is not None`避免空值问题

```python
# 正确示例
if data.optional_field is not None and data.optional_field == expected_value:
    # 安全处理
    pass
```

### 2. 数据库操作

- **唯一性检查**：先验证唯一约束
- **有条件查询**：只在用户提供值时进行检查

```python
# 唯一性检查示例
if data.username and await get_by_username(data.username):
    raise HTTPException(
        status_code=400, 
        detail="名称已存在"
    )
```

### 3. 响应格式

统一的响应格式确保API一致性：

```json
{
  "status": "success|error",
  "message": "操作结果描述",
  "data": {}, 
  "code": 200
}
```

错误响应格式：

```json
{
  "status": "error",
  "message": "错误描述",
  "code": 400,
  "errors": {
    "field_name": ["具体错误说明"]
  }
}
```

### 4. 状态码使用

| 状态码 | 使用场景 |
|-------|---------|
| 200   | 请求成功 |
| 400   | 参数错误/业务验证失败 |
| 401   | 未授权/认证失败 |
| 403   | 权限不足 |
| 404   | 资源不存在 |
| 409   | 资源冲突 |
| 422   | 请求体验证失败 |
| 500   | 服务器错误 |

## 实现示例

```python
from pydantic import BaseModel, validator
from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter()

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('名称不能为空')
        return v
        
    @validator('price')
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError('价格必须为正数')
        return v

@router.post("/items")
async def create_item(item: ItemCreate):
    # 检查名称是否存在
    if item.name and await is_name_exists(item.name):
        raise HTTPException(status_code=400, detail="名称已存在")
    
    # 创建数据
    data = item.dict(exclude_unset=True)
    result = await db.items.insert_one(data)
    
    return {
        "status": "success",
        "message": "创建成功",
        "data": {
            "id": str(result.inserted_id),
            **data
        }
    }
```

遵循此规范可确保API的一致性、可维护性和用户体验。 