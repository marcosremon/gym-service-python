from abc import ABC, abstractmethod

from src.transversal.request_response.user.create_user.create_user_request import CreateUserRequest
from src.transversal.request_response.user.create_user.create_user_response import CreateUserResponse
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

class AbstractUserApplication(ABC):
    @abstractmethod
    async def get_users(self) -> GetUsersResponse:
        pass

    @abstractmethod
    async def create_user(self, create_user_request: CreateUserRequest) -> CreateUserResponse:
        pass