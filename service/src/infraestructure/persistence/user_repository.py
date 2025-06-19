from datetime import datetime

from src.application.mappers.user_mapper import UserMapper
from src.core.interfaces.repository.abstract_user_repository import AbstractUserRepository
from src.core.model.entities.user import User
from src.transversal.request_response.user.create_generic_user.create_generic_user_request import \
    CreateGenericUserRequest
from src.transversal.request_response.user.create_user.create_user_response import CreateUserResponse
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse
from src.transversal.utils.generic_utils import GenericUtils
from src.transversal.security.password_utils import PasswordUtils


class UserRepository(AbstractUserRepository):
    def __init__(self, session):
        self._session = session

    async def get_users(self) -> GetUsersResponse:
        try:
            users = self._session.query(User).all()
            if not users:
                return GetUsersResponse(
                    is_success = False,
                    message = "No users found",
                    response_codes_json= 404,
                    users = []
                )

            return GetUsersResponse(
                is_success = True,
                message = "users found successfully",
                response_codes_json= 200,
                users = UserMapper.map_user_list(users)
            )
        except Exception as e:
            return GetUsersResponse(
                is_success = False,
                message = str(f"unexpected error in get-users repository: {e}"),
                response_codes_json= 500,
                users = []
            )

    async def create_user(self, generic_user_request: CreateGenericUserRequest) -> CreateUserResponse:
        try:
            if not generic_user_request.email:
                return CreateUserResponse(
                    is_success = False,
                    message = "No email found",
                    response_codes_json= 404,
                )

            user = self._session.query(User).filter_by(email = generic_user_request.email).first()
            if user is not None:
                return CreateUserResponse(
                    is_success = False,
                    message = "User already exists with that email",
                    response_codes_json = 404,
                )

            if not PasswordUtils.is_password_valid(generic_user_request.password):
                return CreateUserResponse(
                    is_success = False,
                    message = "Invalid password, the password must be at least 8 characters long, one uppercase letter, one number, one lowercase letter and one special character",
                    response_codes_json = 404,
                )

            user_dni = generic_user_request.dni
            if len(user_dni) != 9 or not user_dni[:8].isdigit() or not user_dni[8].isupper():
                return CreateUserResponse(
                    is_success = False,
                    message = "Invalid DNI, the email need 8 consecutive numbers and one uppercase letter",
                    response_codes_json = 404,
                )

            user = self._session.query(User).filter_by(dni = user_dni).first()
            if user is not None:
                return CreateUserResponse(
                    is_success = False,
                    message = "User already exist with that dni",
                    response_codes_json = 404,
                )

            if not generic_user_request.password == generic_user_request.confirm_password:
                return CreateUserResponse(
                    is_success = False,
                    message = "the passwords not equals",
                    response_codes_json = 404,
                )

            user = User(
                dni = generic_user_request.dni,
                username = generic_user_request.username,
                surname = generic_user_request.surname,
                email = generic_user_request.email,
                friend_code = GenericUtils.create_friend_code(),
                password = PasswordUtils.encrypt_password(generic_user_request.password),
                role = GenericUtils.rol_tostring(generic_user_request.role),
                inscription_date = datetime.now()
            )

            self._session.add(user)
            self._session.commit()

            return CreateUserResponse(
                is_success = True,
                message = "User created successfully",
                response_codes_json= 200,
                user_dto = UserMapper.map_user(user)
            )
        except Exception as e:
            return CreateUserResponse(
                is_success = False,
                message = str(f"unexpected error in create-user repository: {e}"),
                response_codes_json= 500,
            )