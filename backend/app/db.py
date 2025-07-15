from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Импорт Base из models
from .models import Base

db_url = os.getenv("DATABASE_URL")  # postgres+asyncpg://user:pass@db/oporagpt
engine = create_async_engine(db_url, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session
