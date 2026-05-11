import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from geography import StateUT, Base

# Database connection URL
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/voter_db"

STATES_DATA = [
    ("Andhra Pradesh", "AP", "State"),
    ("Arunachal Pradesh", "AR", "State"),
    ("Assam", "AS", "State"),
    ("Bihar", "BR", "State"),
    ("Chhattisgarh", "CG", "State"),
    ("Goa", "GA", "State"),
    ("Gujarat", "GJ", "State"),
    ("Haryana", "HR", "State"),
    ("Himachal Pradesh", "HP", "State"),
    ("Jharkhand", "JH", "State"),
    ("Karnataka", "KA", "State"),
    ("Kerala", "KL", "State"),
    ("Madhya Pradesh", "MP", "State"),
    ("Maharashtra", "MH", "State"),
    ("Manipur", "MN", "State"),
    ("Meghalaya", "ML", "State"),
    ("Mizoram", "MZ", "State"),
    ("Nagaland", "NL", "State"),
    ("Odisha", "OR", "State"),
    ("Punjab", "PB", "State"),
    ("Rajasthan", "RJ", "State"),
    ("Sikkim", "SK", "State"),
    ("Tamil Nadu", "TN", "State"),
    ("Telangana", "TG", "State"),
    ("Tripura", "TR", "State"),
    ("Uttar Pradesh", "UP", "State"),
    ("Uttarakhand", "UK", "State"),
    ("West Bengal", "WB", "State"),
]

UTS_DATA = [
    ("Andaman and Nicobar Islands", "AN", "UT"),
    ("Chandigarh", "CH", "UT"),
    ("Dadra and Nagar Haveli and Daman and Diu", "DN", "UT"),
    ("Delhi", "DL", "UT"),
    ("Jammu and Kashmir", "JK", "UT"),
    ("Ladakh", "LA", "UT"),
    ("Lakshadweep", "LD", "UT"),
    ("Puducherry", "PY", "UT"),
]

async def seed_geography():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            # Add States
            for name, code, gtype in STATES_DATA + UTS_DATA:
                state = StateUT(
                    id=str(uuid.uuid4()),
                    name=name,
                    code=code,
                    type=gtype
                )
                session.add(state)
            
            await session.commit()
    
    print(f"Successfully seeded {len(STATES_DATA)} States and {len(UTS_DATA)} UTs.")

if __name__ == "__main__":
    asyncio.run(seed_geography())
