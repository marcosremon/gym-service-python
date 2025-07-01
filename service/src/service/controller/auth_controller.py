from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from src.infraestructure.dependency.dependency_injection import get_user_application
from src.transversal.common.response_codes_json import ResponseCodesJson
from src.transversal.request_response.auth.check_token_status.check_token_status_request import CheckTokenStatusRequest
from src.transversal.request_response.auth.check_token_status.check_token_status_response import \
    CheckTokenStatusResponse
from src.transversal.request_response.auth.login.login_request import LoginRequest
from src.transversal.request_response.auth.login.login_response import LoginResponse
from src.transversal.request_response.auth.login_web.login_web_request import LoginWebRequest
from src.transversal.request_response.auth.login_web.login_web_response import LoginWebResponse

http = APIRouter(prefix="/api/auth")

@http.post("/login", response_model = LoginResponse)
async def login(login_request: LoginRequest, application = Depends(get_user_application)):
    try:
        if login_request is None or login_request.email is None or login_request.password is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = LoginResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, the inputs parameters are null or empty"),
                ).dict()
            )
        else:
            login_response = await application.login(login_request)
            if login_response.is_success:
                json_response = JSONResponse(
                    status_code = login_response.response_codes_json,
                    content = LoginResponse(
                        is_success = login_response.is_success,
                        message = login_response.message,
                        response_codes_json = login_response.response_codes_json,
                        is_admin = login_response.is_admin,
                        token = login_response.token,
                    ).dict(),
                )
            else:
                json_response = JSONResponse(
                    status_code = login_response.response_codes_json,
                    content = LoginResponse(
                        is_success = login_response.is_success,
                        message = login_response.message,
                        response_codes_json = login_response.response_codes_json,
                        is_admin = login_response.is_admin,
                        token = login_response.token,
                    ).dict(),
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content=LoginResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on login controller: {e}"),
            ).dict(),
        )

    return json_response

@http.post("/login-web", response_model = LoginWebResponse)
async def login_web(login_web_request: LoginWebRequest, application = Depends(get_user_application)):
    try:
        if login_web_request is None or login_web_request.email is None or login_web_request.password is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = LoginWebResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, the inputs parameters are null or empty"),
                ).dict()
            )
        else:
            login_web_response = await application.login_web(login_web_request)
            if login_web_response.is_success:
                json_response = JSONResponse(
                    status_code = login_web_response.response_codes_json,
                    content = LoginWebResponse(
                        response_codes_json = login_web_response.response_codes_json,
                        is_success = login_web_response.is_success,
                        message = login_web_response.message,
                        is_admin = login_web_response.is_admin,
                        token = login_web_response.token,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = login_web_response.response_codes_json,
                    content = LoginWebResponse(
                        response_codes_json = login_web_response.response_codes_json,
                        is_success = login_web_response.is_success,
                        message = login_web_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = LoginWebResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on login web controller: {e}"),
            )
        )

    return json_response

@http.post("/check-token-status", response_model = CheckTokenStatusResponse)
async def login_web(check_login_status_request: CheckTokenStatusRequest, application = Depends(get_user_application)):
    try:
        if check_login_status_request is None or check_login_status_request.token is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = CheckTokenStatusResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, the inputs parameters are null or empty"),
                )
            )
        else:
            check_login_status_response = await application.login_web(check_login_status_request)
            if check_login_status_response.is_success:
                json_response = JSONResponse(
                    status_code = check_login_status_response.response_codes_json,
                    content = CheckTokenStatusResponse(
                        response_codes_json = check_login_status_response.response_codes_json,
                        is_success = check_login_status_response.is_success,
                        message = check_login_status_response.message,
                        is_valid = check_login_status_response.is_valid,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = check_login_status_response.response_codes_json,
                    content = CheckTokenStatusResponse(
                        response_codes_json = check_login_status_response.response_codes_json,
                        is_success = check_login_status_response.is_success,
                        message = check_login_status_response.message,
                        is_valid = check_login_status_response.is_valid,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = CheckTokenStatusResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on login web controller: {e}"),
            )
        )

    return json_response