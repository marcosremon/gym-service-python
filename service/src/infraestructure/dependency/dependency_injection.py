from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.application.uses_cases.user_application import UserApplication
from src.infraestructure.context.application_db_context import ApplicationDbContext
from src.infraestructure.persistence.user_repository import UserRepository

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    db_context = ApplicationDbContext()
    async for session in db_context.get_session():
        yield session

async def get_user_repository(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(session)

async def get_user_application(repository: UserRepository = Depends(get_user_repository)) -> UserApplication:
    return UserApplication(repository)