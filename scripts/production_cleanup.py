import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

# Database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

async def purge_demo_data():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    tables_to_purge = [
        "voters",
        "voter_profiles",
        "candidates",
        "elections",
        "fraud_alerts",
        "audit_logs",
        "notifications"
    ]

    async with async_session() as session:
        async with session.begin():
            print("Purging demo data from production database...")
            for table in tables_to_purge:
                try:
                    await session.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"))
                    print(f"Purged table: {table}")
                except Exception as e:
                    print(f"Error purging {table}: {e}")
            
            await session.commit()
    
    print("Production cleanup complete. Database is now empty and safe for seeding.")

if __name__ == "__main__":
    asyncio.run(purge_demo_data())
