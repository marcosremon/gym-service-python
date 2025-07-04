from src.core.interfaces.application.abstract_user_application import AbstractUserApplication
from src.infraestructure.persistence.user_repository import UserRepository
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
from src.transversal.request_response.user.create_user.create_user_response import CreateUserResponse
from src.transversal.request_response.user.delete_user.delete_user_request import DeleteUserRequest
from src.transversal.request_response.user.delete_user.delete_user_response import DeleteUserResponse
from src.transversal.request_response.user.get_user_by_email.get_user_by_email_request import GetUserByEmailRequest
from src.transversal.request_response.user.get_user_by_email.get_user_by_email_response import GetUserByEmailResponse
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse
from src.transversal.request_response.user.update_user.update_user_request import UpdateUserRequest
from src.transversal.request_response.user.update_user.update_user_response import UpdateUserResponse


class UserApplication(AbstractUserApplication):
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def get_users(self) -> GetUsersResponse:
        return await self._repository.get_users()

    async def create_user(self, generic_user_request: CreateGenericUserRequest) -> CreateUserResponse:
        return await self._repository.create_user(generic_user_request)

    async def get_user_by_email(self, get_user_by_email: GetUserByEmailRequest) -> GetUserByEmailResponse:
        return await self._repository.get_user_by_email(get_user_by_email)

    async def delete_user(self, delete_user_request: DeleteUserRequest) -> DeleteUserResponse:
        return await self._repository.delete_user(delete_user_request)

    async def update_user(self, update_user_request: UpdateUserRequest) -> UpdateUserResponse:
        return await self._repository.update_user(update_user_request)

    async def create_google_user(self, create_google_user_request: CreateGoogleUserRequest) -> CreateGoogleUserResponse:
        return await self._repository.create_google_user(create_google_user_request)

    async def create_new_password(self, create_new_password_request: CreateNewPasswordRequest) -> CreateNewPasswordResponse:
        return await self._repository.create_new_password(create_new_password_request)

    async def create_new_password_with_email_and_password(self, create_new_password_request: CreateNewPasswordWithEmailAndPasswordRequest) -> CreateNewPasswordWithEmailAndPasswordResponse:
        return await self._repository.create_new_password_with_email_and_password(create_new_password_request)