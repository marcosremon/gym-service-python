from abc import ABC, abstractmethod

from src.transversal.request_response.user.create_generic_user.create_generic_user_request import \
    CreateGenericUserRequest
from src.transversal.request_response.user.create_user.create_user_request import CreateUserRequest
from src.transversal.request_response.user.create_user.create_user_response import CreateUserResponse
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

class AbstractUserRepository(ABC):
    @abstractmethod
    def get_users(self) -> GetUsersResponse:
        pass

    @abstractmethod
    def create_user(self, generic_user_request: CreateGenericUserRequest) -> CreateUserResponse:
        pass