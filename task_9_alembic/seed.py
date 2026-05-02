import asyncio
from database import async_session
from models import Product


async def seed():
    async with async_session() as session:
        products = [
            Product(title="Ноутбук", price=999.99, count=10),
            Product(title="Мышь", price=49.99, count=50),
        ]
        session.add_all(products)
        await session.commit()
        print("Добавлены 2 записи в таблицу products")


if __name__ == "__main__":
    asyncio.run(seed())