import asyncio
import json
from app.services.ingredient import get_ingredient_categories, recognize_ingredient

async def test_get_categories():
    """测试获取食材分类列表"""
    categories = await get_ingredient_categories()
    print("食材分类列表：")
    print(json.dumps(categories, ensure_ascii=False, indent=2))
    return categories

async def test_recognize_ingredient():
    """测试食材识别"""
    text = "500克土豆"
    result = await recognize_ingredient(text)
    print(f"识别\"{text}\"的结果：")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return result

async def main():
    print("开始测试食材服务...")
    
    # 测试获取分类
    await test_get_categories()
    
    # 测试食材识别
    await test_recognize_ingredient()
    
    print("测试完成！")

if __name__ == "__main__":
    asyncio.run(main()) 