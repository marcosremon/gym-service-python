from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.service.configuration.dependency_injection import get_user_application
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

http = APIRouter(prefix="/api/user")

@http.get("/get-users", response_model=GetUsersResponse)
async def get_users(application = Depends(get_user_application)):
    try:
        get_users_response = await application.get_users()
        if get_users_response.is_success:
            return JSONResponse(
                content = get_users_response.dict(),
                status_code = get_users_response.response_codes_json
            )

        return JSONResponse(
            content = get_users_response.dict(),
            status_code = get_users_response.response_codes_json
        )
    except Exception as e:
        error_response = GetUsersResponse(
                is_success = False,
                message = str(f"unexpected error in get-users controller -->: {e}"),
                response_codes_json = 500,
                users=[]
        ),

        return JSONResponse(
            content = error_response.dict(),
            status_code = error_response.response_codes_json
        )