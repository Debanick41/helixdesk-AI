from pymongo.errors import PyMongoError

from app.db.mongo import client, database


async def check_database_connection() -> bool:
    try:
        await client.admin.command("ping")
        print(f"MongoDB connected. Database: {database.name}")
        return True
    except PyMongoError as exc:
        print(f"MongoDB connection failed: {exc}")
        return False
    finally:
        await client.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(check_database_connection())