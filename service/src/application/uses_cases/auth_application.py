from src.core.interfaces.application.abstract_auth_application import AbstractAuthApplication
from src.infraestructure.persistence.auth_repository import AuthRepository
from src.transversal.request_response.auth.check_token_status.check_token_status_request import CheckTokenStatusRequest
from src.transversal.request_response.auth.check_token_status.check_token_status_response import \
    CheckTokenStatusResponse
from src.transversal.request_response.auth.login.login_request import LoginRequest
from src.transversal.request_response.auth.login.login_response import LoginResponse
from src.transversal.request_response.auth.login_web.login_web_request import LoginWebRequest
from src.transversal.request_response.auth.login_web.login_web_response import LoginWebResponse

class AuthApplication(AbstractAuthApplication):
    def __init__(self, repository: AuthRepository):
        self._repository = repository

    async def login(self, login_request: LoginRequest) -> LoginResponse:
        if login_request.email is None or login_request.password is None:
            return LoginResponse(
                is_success = False,
                message = "email or password is required",
                response_codes_json = 400
            )

        return await self._repository.login(login_request)

    async def login_web(self, login_web_request: LoginWebRequest) -> LoginWebResponse:
        if login_web_request.email is None or login_web_request.password is None:
            return LoginWebResponse(
                is_success = False,
                message = "email or password is required",
                response_codes_json = 400
            )

        return await self._repository.login_web(login_web_request)

    async def check_token_status(self, check_token_status_request: CheckTokenStatusRequest) -> CheckTokenStatusResponse:
        if check_token_status_request.token is None:
            return CheckTokenStatusResponse(
                is_success = False,
                message = "token is required",
                response_codes_json = 400
            )

        return await self._repository.check_token_status(check_token_status_request)