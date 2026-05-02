import asyncio
from database import async_session
from sqlalchemy import text


async def check():
    async with async_session() as session:
        result = await session.execute(text("SELECT * FROM products"))
        rows = result.fetchall()
        for row in rows:
            print(f"id={row[0]}, title={row[1]}, price={row[2]}, count={row[3]}, description={row[4]}")

if __name__ == "__main__":
    asyncio.run(check())