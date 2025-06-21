from abc import ABC, abstractmethod

from src.transversal.request_response.routine.create_routine.create_routine_request import CreateRoutineRequest
from src.transversal.request_response.routine.create_routine.create_routine_response import CreateRoutineResponse
from src.transversal.request_response.user.create_generic_user.create_generic_user_request import \
    CreateGenericUserRequest
from src.transversal.request_response.user.create_google_user.create_google_user_request import CreateGoogleUserRequest
from src.transversal.request_response.user.create_google_user.create_google_user_response import \
    CreateGoogleUserResponse
from src.transversal.request_response.user.create_new_password.create_new_password_request import \
    CreateNewPasswordRequest
from src.transversal.request_response.user.create_new_password.create_new_password_response import \
    CreateNewPasswordResponse
from src.transversal.request_response.user.create_new_password_with_email_and_password.create_new_password_with_email_and_password_request import \
    CreateNewPasswordWithEmailAndPasswordRequest
from src.transversal.request_response.user.create_new_password_with_email_and_password.create_new_password_with_email_and_password_response import \
    CreateNewPasswordWithEmailAndPasswordResponse
from src.transversal.request_response.user.create_user.create_user_request import CreateUserRequest
from src.transversal.request_response.user.create_user.create_user_response import CreateUserResponse
from src.transversal.request_response.user.delete_user.delete_user_request import DeleteUserRequest
from src.transversal.request_response.user.delete_user.delete_user_response import DeleteUserResponse
from src.transversal.request_response.user.get_user_by_email.get_user_by_email_request import GetUserByEmailRequest
from src.transversal.request_response.user.get_user_by_email.get_user_by_email_response import GetUserByEmailResponse
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse
from src.transversal.request_response.user.update_user.update_user_request import UpdateUserRequest
from src.transversal.request_response.user.update_user.update_user_response import UpdateUserResponse


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_users(self) -> GetUsersResponse:
        pass

    @abstractmethod
    def create_user(self, generic_user_request: CreateGenericUserRequest) -> CreateUserResponse:
        pass

    @abstractmethod
    async def get_user_by_email(self, get_user_by_email: GetUserByEmailRequest) -> GetUserByEmailResponse:
        pass

    @abstractmethod
    async def delete_user(self, delete_user_request: DeleteUserRequest) -> DeleteUserResponse:
        pass

    @abstractmethod
    async def update_user(self, update_user_request: UpdateUserRequest) -> UpdateUserResponse:
        pass

    @abstractmethod
    async def create_google_user(self, create_google_user_request: CreateGoogleUserRequest) -> CreateGoogleUserResponse:
        pass

    @abstractmethod
    async def create_new_password(self, create_new_password_request: CreateNewPasswordRequest) -> CreateNewPasswordResponse:
        pass

    @abstractmethod
    async def create_new_password_with_email_and_password(self, create_new_password_request: CreateNewPasswordWithEmailAndPasswordRequest) -> CreateNewPasswordWithEmailAndPasswordResponse:
        pass