from fastapi import Depends
from src.core.interfaces.application.abstract_user_application import AbstractUserApplication
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

_user_repository = AbstractUserRepository = Depends()

class UserApplication(AbstractUserApplication):

    async def get_users(self) -> GetUsersResponse:
        return await _user_repository.get_users()