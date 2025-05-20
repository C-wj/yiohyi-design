import asyncio
from datetime import datetime
from app.db.mongodb import connect_to_mongo, get_database
from app.models.comment import CommentCreate
from app.services.comment import create_comment, get_recipe_comments

async def main():
    print("连接数据库...")
    await connect_to_mongo()
    db = await get_database()
    
    print("查找测试用户和菜谱...")
    user = await db.users.find_one({})
    recipe = await db.recipes.find_one({})
    
    print(f"用户: {user['_id']}")
    print(f"菜谱: {recipe['_id']}")
    
    # 测试获取评论
    print("\n获取评论列表...")
    comments, total = await get_recipe_comments(str(recipe["_id"]), 1, 10)
    print(f"共 {total} 条评论")
    
    # 测试创建评论
    print("\n创建新评论...")
    comment_data = CommentCreate(
        content=f"测试评论 {datetime.now()}",
        rating=5,
        images=[]
    )
    new_comment = await create_comment(str(recipe["_id"]), comment_data, user)
    print(f"评论创建成功: {new_comment.id}")

if __name__ == "__main__":
    asyncio.run(main()) 