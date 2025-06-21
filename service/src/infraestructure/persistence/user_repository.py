from datetime import datetime
from src.application.mappers.user_mapper import UserMapper
from src.core.interfaces.repository.abstract_user_repository import AbstractUserRepository
from src.core.model.entities import Routine, UserFriend
from src.core.model.entities.user import User
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
from src.transversal.utils.generic_utils import GenericUtils
from src.transversal.security.password_utils import PasswordUtils
from src.transversal.utils.mail_utils import MailUtils


class UserRepository(AbstractUserRepository):
    def __init__(self, session):
        self._session = session

    async def get_users(self) -> GetUsersResponse:
        try:
            users = await self._session.query(User).all()
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

            user = await self._session.query(User).filter_by(email = generic_user_request.email).first()
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

            user = await self._session.query(User).filter_by(dni = user_dni).first()
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

            unique_friend_code = GenericUtils.create_friend_code()
            exist_friend_code = await self._session.query(User).filter_by(friend_code = unique_friend_code).exist()
            while True:
                if not exist_friend_code:
                    break
                unique_friend_code = GenericUtils.create_friend_code()

            user = User(
                dni = generic_user_request.dni,
                username = generic_user_request.username,
                surname = generic_user_request.surname,
                email = generic_user_request.email,
                friend_code = unique_friend_code,
                password = PasswordUtils.encrypt_password(generic_user_request.password),
                role = GenericUtils.rol_tostring(generic_user_request.role),
                inscription_date = datetime.now()
            )

            await self._session.add(user)
            await self._session.commit()

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

    async def get_user_by_email(self, get_user_by_email: GetUserByEmailRequest) -> GetUserByEmailResponse:
        try:
            user = await self._session.query(User).filter_by(email = get_user_by_email.email).first()
            if not user:
                return GetUserByEmailResponse(
                    is_success = False,
                    message = "No user found with that email",
                    response_codes_json= 404,
                )

            return GetUserByEmailResponse(
                is_success = True,
                message = "user found successfully",
                response_codes_json= 200,
                user_dto = UserMapper.map_user(user),
                routines_count = await self._session.query(Routine).filter_by(user_id = user.user_id).count(),
                friends_count = await self._session.query(UserFriend).filter_by(user_id = user.user_id).count()
            )
        except Exception as e:
            return GetUserByEmailResponse(
                is_success = False,
                message = f"unexpected error in get-user-by-email repository: {e}",
                response_codes_json= 500,
            )

    async def delete_user(self, delete_user_request: DeleteUserRequest) -> DeleteUserResponse:
        try:
            user = await self._session.query(User).filter_by(email = delete_user_request.email).first()
            if user is None:
                return DeleteUserResponse(
                    is_success = False,
                    message = "No user found with that email",
                    response_codes_json= 404,
                )

            await self._session.delete(user)
            await self._session.commit()

            return DeleteUserResponse(
                is_success = True,
                message = "User deleted successfully",
                response_codes_json= 200,
                user_dto = UserMapper.map_user(user)
            )
        except Exception as e:
            return DeleteUserResponse(
                is_success = False,
                message = str(f"unexpected error in delete-user repository: {e}"),
                response_codes_json= 500,
            )

    async def update_user(self, update_user_request: UpdateUserRequest) -> UpdateUserResponse:
        try:
            user = await self._session.query(User).filter_by(email = update_user_request.email).first()
            if user is None:
                return UpdateUserResponse(
                    is_success = False,
                    message = "No user found with that email",
                    response_codes_json= 404,
                )

            user.username = update_user_request.new_username if update_user_request.new_username != "" else user.username
            user.surname = update_user_request.new_surname if update_user_request.new_surname != "" else user.surname
            user.email = update_user_request.new_email if update_user_request.new_email != "" else user.email
            user.dni = update_user_request.new_dni if update_user_request.new_dni != "" else user.dni

            await self._session.commit()

            return UpdateUserResponse(
                is_success = True,
                message = "User updated successfully",
                response_codes_json= 200,
                user_dto = UserMapper.map_user(user)
            )
        except Exception as e:
            return UpdateUserResponse(
                is_success = False,
                message = str(f"unexpected error in update-user repository: {e}"),
                response_codes_json= 500,
            )

    async def create_google_user(self, create_google_user_request: CreateGoogleUserRequest) -> CreateGoogleUserResponse:
        try:
            if MailUtils.is_email_valid(create_google_user_request.email):
                return CreateGoogleUserResponse(
                    is_success = False,
                    message = "Email is not valid",
                    response_codes_json= 404,
                )

            existing_user = await self._session.query(User).filter_by(email = create_google_user_request.email).exists()
            if existing_user:
                return CreateGoogleUserResponse(
                    is_success = False,
                    message = "User already exists",
                    response_codes_json= 404,
                )

            unique_friend_code = GenericUtils.create_friend_code()
            exist_friend_code = await self._session.query(User).filter_by(friend_code = unique_friend_code).exist()
            while True:
                if not exist_friend_code:
                    break
                unique_friend_code = GenericUtils.create_friend_code()

            user = User(
                dni = create_google_user_request.dni,
                username = create_google_user_request.username,
                surname = create_google_user_request.surname,
                friend_code = unique_friend_code,
                password = PasswordUtils.encrypt_password(create_google_user_request.password),
                email = create_google_user_request.email,
                role = GenericUtils.rol_tostring(create_google_user_request.role),
                inscription_date = datetime.now(),
            )

            await self._session.add(user)
            await self._session.commit()

            MailUtils.send_email_after_created_google_account_by_google(user.username, user.email)

            return CreateGoogleUserResponse(
                is_success = True,
                message = "User created successfully",
                response_codes_json= 200,
                user_dto = UserMapper.map_user(user)
            )
        except Exception as e:
            return CreateGoogleUserResponse(
                is_success = False,
                message = str(f"unexpected error in create-google-user repository: {e}"),
                response_codes_json= 500,
            )

    async def create_new_password(self, create_new_password_request: CreateNewPasswordRequest) -> CreateNewPasswordResponse:
        try:
            user = await self._session.query(User).filter_by(email = create_new_password_request.email).first()
            if user is None:
                return CreateNewPasswordResponse(
                    is_success = False,
                    message = "No user found with that email",
                    response_codes_json= 404,
                )

            new_password = PasswordUtils.create_password()
            while True:
                if PasswordUtils.decrypt_password(user.password) == new_password:
                    new_password = PasswordUtils.create_password()
                    continue
                break

            password_hash = PasswordUtils.encrypt_password(new_password)

            user.password = password_hash
            MailUtils.send_password_email(user.username, user.email, new_password)
            await self._session.commit()

            return CreateNewPasswordResponse(
                is_success = True,
                message = "New password created successfully",
                response_codes_json= 200,
                user_dto = UserMapper.map_user(user)
            )
        except Exception as e:
            return CreateNewPasswordResponse(
                is_success = False,
                message = str(f"unexpected error in create-new-password repository: {e}"),
                response_codes_json= 500,
            )

    async def create_new_password_with_email_and_password(self, create_new_password_request: CreateNewPasswordWithEmailAndPasswordRequest) -> CreateNewPasswordWithEmailAndPasswordResponse:
        try:
            user = await self._session.query(User).filter_by(email = create_new_password_request.email).first()
            if user is None:
                return CreateNewPasswordWithEmailAndPasswordResponse(
                    is_success = False,
                    message = "No user found with that email",
                    response_codes_json= 404,
                )

            if PasswordUtils.decrypt_password(user.password) != create_new_password_request.old_password:
                return CreateNewPasswordWithEmailAndPasswordResponse(
                    is_success = False,
                    message = "Old password does not match",
                    response_codes_json= 404,
                )

            if not PasswordUtils.is_password_valid(create_new_password_request.new_password):
                return CreateNewPasswordWithEmailAndPasswordResponse(
                    is_success = False,
                    message = "new password is not valid",
                    response_codes_json= 404,
                )

            if PasswordUtils.decrypt_password(user.password) == create_new_password_request.new_password \
                    or create_new_password_request.old_password == create_new_password_request.new_password:
                return CreateNewPasswordWithEmailAndPasswordResponse(
                    is_success = False,
                    message = "new password is equals to old password",
                    response_codes_json= 404,
                )

            user.password = PasswordUtils.encrypt_password(create_new_password_request.new_password)
            MailUtils.send_password_email(user.username, user.email, create_new_password_request.new_password)
            await self._session.commit()

            return CreateNewPasswordWithEmailAndPasswordResponse(
                is_success = True,
                message = "New password created successfully",
                response_codes_json= 200,
                user_dto = UserMapper.map_user(user)
            )
        except Exception as e:
            return CreateNewPasswordWithEmailAndPasswordResponse(
                is_success = False,
                message = str(f"unexpected error in create-new-password-with-email-and-password repository: {e}"),
                response_codes_json= 500,
            )