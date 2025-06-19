from fastapi import Depends
from src.core.interfaces.application.abstract_user_application import AbstractUserApplication
from src.infraestructure.persistence.user_repository import UserRepository
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

class UserApplication(AbstractUserApplication):
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def get_users(self) -> GetUsersResponse:
        return await self._repository.get_users()