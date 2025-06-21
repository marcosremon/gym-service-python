from src.core.interfaces.repository.abstract_auth_repository import AbstractAuthRepository
from src.core.model.entities import User, UserFriend
from src.transversal.request_response.auth.check_token_status.check_token_status_request import CheckTokenStatusRequest
from src.transversal.request_response.auth.check_token_status.check_token_status_response import \
    CheckTokenStatusResponse
from src.transversal.request_response.auth.login.login_request import LoginRequest
from src.transversal.request_response.auth.login.login_response import LoginResponse
from src.transversal.request_response.auth.login_web.login_web_request import LoginWebRequest
from src.transversal.request_response.auth.login_web.login_web_response import LoginWebResponse
from src.transversal.security.jwt_utils import JWTUtils

class AuthRepository(AbstractAuthRepository):
    def __init__(self, session):
        self._session = session

    async def login(self, login_request: LoginRequest) -> LoginResponse:
        try:
            user = await self._session.query(User).filter_by(email = login_request.email).first()
            if user is None:
                return LoginResponse(
                    is_success = False,
                    message = "user not found",
                    response_codes_json = 404
                )

            jwt_utils = JWTUtils()
            token_data = {
                "sub": str(user.user_id),
                "email": user.email,
                "role": user.role
            }

            is_admin = str(user.is_admin).lower() == "admin"

            return LoginResponse(
                is_success = True,
                message = "admin found" if is_admin else "user found",
                response_codes_json = 200,
                is_admin = is_admin,
                token = jwt_utils.create_admin_token(token_data) if is_admin else jwt_utils.create_user_token(token_data),
            )
        except Exception as e:
            return LoginResponse(
                is_success=False,
                message= f"unexpected error in login repository: {e}",
                response_codes_json = 500
            )

    async def login_web(self, login_web_request: LoginWebRequest) -> LoginWebResponse:
        try:
            user = await self._session.query(User).filter_by(email = login_web_request.email).first()
            if user is None:
                return LoginWebResponse(
                    is_success = False,
                    message = "user not found",
                    response_codes_json = 404
                )

            is_admin = str(user.is_admin).lower() == "admin"
            if not is_admin:
                return LoginWebResponse(
                    is_success = False,
                    message = "web is only admins",
                    response_codes_json = 401
                )

            jwt_utils = JWTUtils()
            token_data = {
                "sub": str(user.user_id),
                "email": user.email,
                "role": user.role
            }

            return LoginWebResponse(
                is_success = True,
                message = "admin found",
                response_codes_json = 200,
                is_admin = is_admin,
                token = jwt_utils.create_admin_token(token_data),
            )
        except Exception as e:
            return LoginWebResponse(
                is_success=False,
                message=f"unexpected error in login-web repository: {e}",
                response_codes_json=500
            )

    async def check_token_status(self, check_token_status_request: CheckTokenStatusRequest) -> CheckTokenStatusResponse:
        try:
            jwt_utils = JWTUtils()
            token_is_valid = jwt_utils.is_token_valid(check_token_status_request.token)
            if not token_is_valid:
                return CheckTokenStatusResponse(
                    is_success = False,
                    message = "token is invalid",
                    response_codes_json = 401
                )

            return CheckTokenStatusResponse(
                is_success = True,
                message = "token is valid",
                response_codes_json = 200,
                is_valid = token_is_valid,
            )
        except Exception as e:
            return CheckTokenStatusResponse(
                is_success = False,
                message = f"unexpected error in check-token-status repository: {e}",
                response_codes_json = 500
            )