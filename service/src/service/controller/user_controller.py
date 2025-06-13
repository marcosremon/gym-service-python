from fastapi import APIRouter, logger, Depends
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

http = APIRouter(prefix="/api/user")
_user_application = IUserApplication = Depends()

@http.get("/get-users", response_model=GetUsersResponse)
async def get_users():
    get_users_response: GetUsersResponse

    try:
        return await _user_application.get_users()
    except Exception as e:
        #logger.error(f"unexpected error in get_users: {e}")
        return get_users_response  