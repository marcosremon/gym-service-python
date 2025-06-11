from fastapi import APIRouter, logger
from src.core.interfaces import IUserApplication as _userApplication
from src.transversal.utils.response_codes_json import ResponseCodesJson

http = APIRouter(prefix="/api/user")


@http.get("/get-users", response_model=GetUsersResponse)
def get_users():
    get_users_response: GetUsersResponse()
    
    try:
        return get_users_response
    except Exception as e:
        logger.error(f"unexpected error in get_users: {e}")
        return get_users_response  