from typing import AsyncGenerator, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.service.configuration.config import load_db_config

Base = declarative_base()

class ApplicationDbContext:
    def __init__(self):
        config = load_db_config()
        database_url = f"postgresql+asyncpg://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['name']}"
        self._engine = create_async_engine(
            database_url,
            echo=True
        )
        self._SessionLocal = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )

    @property
    def engine(self):
        return self._engine

    @property
    def SessionLocal(self):
        return self._SessionLocal

    async def create_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session: AsyncSession
        async with self.SessionLocal() as session:
            yield session