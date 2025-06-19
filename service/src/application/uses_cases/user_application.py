from fastapi import Depends
from src.core.interfaces.application.abstract_user_application import AbstractUserApplication
from src.infraestructure.persistence.user_repository import UserRepository
from src.transversal.request_response.user.create_generic_user.create_generic_user_request import \
    CreateGenericUserRequest
from src.transversal.request_response.user.create_user.create_user_request import CreateUserRequest
from src.transversal.request_response.user.create_user.create_user_response import CreateUserResponse
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

class UserApplication(AbstractUserApplication):
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def get_users(self) -> GetUsersResponse:
        return await self._repository.get_users()

    async def create_user(self, generic_user_request: CreateGenericUserRequest) -> CreateUserResponse:
        if generic_user_request.email is None or generic_user_request.dni is None or generic_user_request.username is None:
            return CreateUserResponse(
                is_success = False,
                message = "Username or email or dni is required",
                response_codes_json = 400
            )

        return await self._repository.create_user(generic_user_request)