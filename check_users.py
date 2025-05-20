import asyncio
from app.db.mongodb import get_collection, connect_to_mongo

async def list_users():
    await connect_to_mongo()
    coll = get_collection('users')
    users = await coll.find({}).to_list(length=10)
    
    print(f"Found {len(users)} users:")
    for user in users:
        print(f"ID: {user.get('_id')}, Username: {user.get('username')}, Nickname: {user.get('profile', {}).get('nickname')}")
    
    return users

if __name__ == "__main__":
    asyncio.run(list_users()) 