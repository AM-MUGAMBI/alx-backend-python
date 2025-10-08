import asyncio
import aiosqlite

DB_NAME = "example_async.db"

# Function to set up the database with test data
async def setup_database():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')
        await db.executemany('''
            INSERT OR IGNORE INTO users (id, name, age) VALUES (?, ?, ?)
        ''', [
            (1, 'Alice', 30),
            (2, 'Bob', 45),
            (3, 'Charlie', 50),
            (4, 'Diana', 25)
        ])
        await db.commit()

# Asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        await cursor.close()
        print("\nAll Users:")
        for user in users:
            print(user)
        return users

# Asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        older_users = await cursor.fetchall()
        await cursor.close()
        print("\nUsers Older Than 40:")
        for user in older_users:
            print(user)
        return older_users

# Run both queries concurrently
async def fetch_concurrently():
    await setup_database()  # Ensure table and data are ready
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

