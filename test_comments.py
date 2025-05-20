#!/usr/bin/env python
"""
手动测试评论功能
"""

import asyncio
import json
from bson import ObjectId
from datetime import datetime

from app.db.mongodb import connect_to_mongo, get_database
from app.models.comment import CommentCreate
from app.services.comment import (
    create_comment,
    get_recipe_comments,
    delete_comment,
    like_comment,
    unlike_comment,
    reply_comment,
    get_comment_by_id
)

async def setup_test_data():
    """设置测试数据"""
    print("设置测试数据...")

    # 连接数据库
    await connect_to_mongo()
    db = await get_database()

    # 设置测试用户
    user_id = ObjectId()
    user = {
        "_id": user_id,
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "hashed_password",
        "profile": {
            "nickname": "测试用户",
            "avatar": "https://example.com/avatar.jpg"
        },
        "is_active": True,
        "is_admin": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    # 创建测试用户（如果不存在）
    existing_user = await db.users.find_one({"username": "testuser"})
    if not existing_user:
        await db.users.insert_one(user)
        print(f"创建测试用户: {user_id}")
    else:
        user_id = existing_user["_id"]
        user = existing_user
        print(f"使用已存在的测试用户: {user_id}")

    # 设置测试菜谱
    recipe_id = ObjectId()
    recipe = {
        "_id": recipe_id,
        "title": "测试菜谱",
        "description": "这是一个测试菜谱",
        "cover_image": "https://example.com/recipe.jpg",
        "creator_id": str(user_id),
        "status": "published",
        "ingredients": [{"name": "测试食材", "amount": "100g"}],
        "steps": [{"description": "测试步骤", "image": "https://example.com/step.jpg"}],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    # 创建测试菜谱（如果不存在）
    existing_recipe = await db.recipes.find_one({"title": "测试菜谱"})
    if not existing_recipe:
        await db.recipes.insert_one(recipe)
        print(f"创建测试菜谱: {recipe_id}")
    else:
        recipe_id = existing_recipe["_id"]
        recipe = existing_recipe
        print(f"使用已存在的测试菜谱: {recipe_id}")

    return user, recipe

async def test_comment_features():
    """测试评论相关功能"""
    # 设置测试数据
    user, recipe = await setup_test_data()
    
    print("\n--- 测试创建评论 ---")
    # 创建评论
    comment_data = CommentCreate(
        content="这是一条测试评论",
        rating=5,
        images=[]
    )
    
    comment = await create_comment(
        str(recipe["_id"]),
        comment_data,
        user
    )
    
    print(f"评论创建成功: {comment.id}")
    print(f"评论内容: {comment.content}")
    
    print("\n--- 测试获取评论列表 ---")
    # 获取评论列表
    comments, total = await get_recipe_comments(
        str(recipe["_id"]),
        page=1,
        limit=10
    )
    
    print(f"共有 {total} 条评论")
    for i, c in enumerate(comments):
        print(f"{i+1}. {c.content} (ID: {c.id})")
    
    print("\n--- 测试获取评论详情 ---")
    # 获取评论详情
    comment_detail = await get_comment_by_id(
        str(recipe["_id"]),
        comment.id
    )
    
    print(f"评论ID: {comment_detail.id}")
    print(f"评论内容: {comment_detail.content}")
    print(f"评论者: {comment_detail.user.name}")
    
    print("\n--- 测试点赞评论 ---")
    # 点赞评论
    like_result = await like_comment(
        comment.id,
        str(user["_id"])
    )
    
    print(f"点赞结果: {'成功' if like_result else '失败'}")
    
    # 获取更新后的评论
    updated_comment = await get_comment_by_id(
        str(recipe["_id"]),
        comment.id
    )
    
    print(f"评论点赞数: {updated_comment.likes}")
    
    print("\n--- 测试回复评论 ---")
    # 回复评论
    reply_data = CommentCreate(
        content="这是一条回复评论",
        rating=4,
        images=[]
    )
    
    reply = await reply_comment(
        str(recipe["_id"]),
        comment.id,
        reply_data,
        user
    )
    
    print(f"回复创建成功: {reply.id}")
    print(f"回复内容: {reply.content}")
    print(f"父评论ID: {reply.parent_id}")
    
    print("\n--- 测试取消点赞评论 ---")
    # 取消点赞
    unlike_result = await unlike_comment(
        comment.id,
        str(user["_id"])
    )
    
    print(f"取消点赞结果: {'成功' if unlike_result else '失败'}")
    
    # 获取更新后的评论
    updated_comment = await get_comment_by_id(
        str(recipe["_id"]),
        comment.id
    )
    
    print(f"评论点赞数: {updated_comment.likes}")
    
    print("\n--- 测试删除评论 ---")
    # 删除评论
    delete_result = await delete_comment(
        str(recipe["_id"]),
        reply.id,  # 删除回复
        user
    )
    
    print(f"删除结果: {'成功' if delete_result else '失败'}")
    
    # 尝试获取已删除的评论
    deleted_comment = await get_comment_by_id(
        str(recipe["_id"]),
        reply.id
    )
    
    print(f"尝试获取已删除评论: {'不存在' if deleted_comment is None else '仍然存在'}")
    
    print("\n所有测试完成!")

async def main():
    """主函数"""
    print("开始测试评论功能...")
    await test_comment_features()

if __name__ == "__main__":
    asyncio.run(main()) 