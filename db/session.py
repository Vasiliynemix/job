from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from settings import DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
