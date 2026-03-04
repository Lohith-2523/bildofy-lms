import asyncio
from app.db.session import engine
from app.db.session import Base
import app.db.base_imports  # IMPORTANT

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_models())
