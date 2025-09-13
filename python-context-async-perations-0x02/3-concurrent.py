import asyncio
import aiosqlite

DB_NAME = "users.db"

# 🔹 Async function to fetch all users
async def asyncfetchusers():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All Users:", results)
            return results

# 🔹 Async function to fetch users older than 40
async def asyncfetcholder_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("Users older than 40:", results)
            return results

# 🔹 Run both queries concurrently
async def fetch_concurrently():
    results = await asyncio.gather(
        asyncfetchusers(),
        asyncfetcholder_users()
    )
    return results

# ✅ Run the event loop
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
