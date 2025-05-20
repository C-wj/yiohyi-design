#!/usr/bin/env python3
"""
简单测试评论功能的脚本
"""

import asyncio
import json
from datetime import datetime
from bson import ObjectId

async def main():
    """主函数"""
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
    
    print("开始测试评论功能...")
    
    # 连接数据库
    print("1. 连接数据库...")
    await connect_to_mongo()
    db = await get_database()
    
    # 获取一个真实存在的用户
    print("2. 获取用户...")
    user = await db.users.find_one({})
    if not user:
        print("错误: 没有找到用户，请先创建用户")
        return
    print(f"使用用户: {user['_id']} ({user.get('profile', {}).get('nickname', '未命名')})")
    
    # 获取一个真实存在的菜谱
    print("3. 获取菜谱...")
    recipe = await db.recipes.find_one({})
    if not recipe:
        print("错误: 没有找到菜谱，请先创建菜谱")
        return
    print(f"使用菜谱: {recipe['_id']} ({recipe.get('title', '未命名')})")
    
    print("\n--- 测试创建评论 ---")
    # 创建评论
    comment_data = CommentCreate(
        content=f"测试评论 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        rating=5,
        images=[]
    )
    try:
        comment = await create_comment(
            str(recipe["_id"]),
            comment_data,
            user
        )
        print(f"评论创建成功: {comment.id}")
        print(f"评论内容: {comment.content}")
    except Exception as e:
        print(f"创建评论失败: {str(e)}")
        return
    
    print("\n--- 测试获取评论列表 ---")
    # 获取评论列表
    try:
        comments, total = await get_recipe_comments(
            str(recipe["_id"]),
            page=1,
            limit=10
        )
        print(f"共有 {total} 条评论")
        for i, c in enumerate(comments[:3]):  # 只显示前3条
            print(f"{i+1}. {c.content} (ID: {c.id})")
        if len(comments) > 3:
            print(f"... 还有 {len(comments) - 3} 条评论")
    except Exception as e:
        print(f"获取评论列表失败: {str(e)}")
    
    print("\n--- 测试获取评论详情 ---")
    # 获取评论详情
    try:
        comment_detail = await get_comment_by_id(
            str(recipe["_id"]),
            comment.id
        )
        print(f"评论ID: {comment_detail.id}")
        print(f"评论内容: {comment_detail.content}")
        print(f"评论者: {comment_detail.user.name}")
    except Exception as e:
        print(f"获取评论详情失败: {str(e)}")
    
    print("\n--- 测试点赞评论 ---")
    # 点赞评论
    try:
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
    except Exception as e:
        print(f"点赞评论失败: {str(e)}")
    
    print("\n--- 测试回复评论 ---")
    # 回复评论
    reply = None
    try:
        reply_data = CommentCreate(
            content=f"回复评论 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
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
    except Exception as e:
        print(f"回复评论失败: {str(e)}")
    
    print("\n--- 测试取消点赞评论 ---")
    # 取消点赞
    try:
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
    except Exception as e:
        print(f"取消点赞评论失败: {str(e)}")
    
    if reply:
        print("\n--- 测试删除评论 ---")
        # 删除评论（回复）
        try:
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
        except Exception as e:
            print(f"删除评论失败: {str(e)}")
    
    print("\n所有测试完成!")

if __name__ == "__main__":
    asyncio.run(main()) 