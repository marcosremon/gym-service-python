from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.service.configuration.dependency_injection import get_user_application
from src.transversal.request_response.auth.check_token_status.check_token_status_request import CheckTokenStatusRequest
from src.transversal.request_response.auth.check_token_status.check_token_status_response import \
    CheckTokenStatusResponse
from src.transversal.request_response.auth.login.login_request import LoginRequest
from src.transversal.request_response.auth.login.login_response import LoginResponse
from src.transversal.request_response.auth.login_web.login_web_response import LoginWebResponse
from src.transversal.request_response.friend.add_new_user_friend.add_new_user_friend_request import \
    AddNewUserFriendRequest
from src.transversal.request_response.friend.add_new_user_friend.add_new_user_friend_response import \
    AddNewUserFriendResponse
from src.transversal.request_response.friend.delete_friend.delete_friend_request import DeleteFriendRequest
from src.transversal.request_response.friend.delete_friend.delete_friend_response import DeleteFriendResponse
from src.transversal.request_response.friend.get_all_user_friends.get_all_user_friend_request import \
    GetAllUserFriendsRequest
from src.transversal.request_response.friend.get_all_user_friends.get_all_user_friend_response import \
    GetAllUserFriendsResponse
from src.transversal.request_response.split_day.update_split_day.update_split_day_request import UpdateSplitDayRequest
from src.transversal.request_response.split_day.update_split_day.update_split_day_response import UpdateSplitDayResponse

http = APIRouter(prefix="/api/auth")

@http.post("/login", response_model = LoginResponse)
async def login(login_request: LoginRequest, application = Depends(get_user_application)):
    try:
        login_response = await application.login(login_request)
        if login_response.is_success:
            return JSONResponse(
                content = login_response.to_dict(),
                status_code = login_response.response_codes_json
            )

        return JSONResponse(
            content = login_response.to_dict(),
            status_code = login_response.response_codes_json
        )
    except Exception as e:
        error_response = LoginResponse(
            is_success = False,
            message = f"unexpected error in login in controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/login-web", response_model = LoginWebResponse)
async def login_web(login_web_request: LoginWebResponse, application = Depends(get_user_application)):
    try:
        login_web_response = await application.login_web(login_web_request)
        if login_web_response.is_success:
            return JSONResponse(
                content = login_web_response.to_dict(),
                status_code = login_web_response.response_codes_json
            )

        return JSONResponse(
            content = login_web_response.to_dict(),
            status_code = login_web_response.response_codes_json
        )
    except Exception as e:
        error_response = LoginWebResponse(
            is_success = False,
            message = f"unexpected error in login-web in controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/check-token-status", response_model = CheckTokenStatusResponse)
async def login_web(check_login_status_request: CheckTokenStatusRequest, application = Depends(get_user_application)):
    try:
        check_login_status_response = await application.login_web(check_login_status_request)
        if check_login_status_response.is_success:
            return JSONResponse(
                content = check_login_status_response.to_dict(),
                status_code = check_login_status_response.response_codes_json
            )

        return JSONResponse(
            content = check_login_status_response.to_dict(),
            status_code = check_login_status_response.response_codes_json
        )
    except Exception as e:
        error_response = CheckTokenStatusResponse(
            is_success = False,
            message = f"unexpected error in check-token-status in controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )