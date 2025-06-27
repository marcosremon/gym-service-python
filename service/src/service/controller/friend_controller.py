from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.infraestructure.dependency.dependency_injection import get_user_application
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

http = APIRouter(prefix="/api/friend")

@http.post("/get-all-user-friends", response_model = GetAllUserFriendsResponse)
async def get_all_user_friends(get_all_user_friends_request: GetAllUserFriendsRequest, application = Depends(get_user_application)):
    try:
        get_all_user_friends_response = await application.get_all_user_friends(get_all_user_friends_request)
        if get_all_user_friends_response.is_success:
            return JSONResponse(
                content = get_all_user_friends_response.to_dict(),
                status_code = get_all_user_friends_response.response_codes_json
            )

        return JSONResponse(
            content = get_all_user_friends_response.to_dict(),
            status_code = get_all_user_friends_response.response_codes_json
        )
    except Exception as e:
        error_response = GetAllUserFriendsResponse(
            is_success = False,
            message = f"unexpected error in get-all-user-friends in controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/add-new-user-friend", response_model = AddNewUserFriendResponse)
async def add_new_user_friend(add_new_user_friend_request: AddNewUserFriendRequest, application = Depends(get_user_application)):
    try:
        add_new_user_friend_response = await application.get_all_user_friends(add_new_user_friend_request)
        if add_new_user_friend_response.is_success:
            return JSONResponse(
                content = add_new_user_friend_response.to_dict(),
                status_code = add_new_user_friend_response.response_codes_json
            )

        return JSONResponse(
            content = add_new_user_friend_response.to_dict(),
            status_code = add_new_user_friend_response.response_codes_json
        )
    except Exception as e:
        error_response = AddNewUserFriendResponse(
            is_success = False,
            message = f"unexpected error in add-new-user-friend in controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/delete-friend", response_model = DeleteFriendResponse)
async def get_all_user_friends(delete_friend_request: DeleteFriendRequest, application = Depends(get_user_application)):
    try:
        delete_friend_response = await application.get_all_user_friends(delete_friend_request)
        if delete_friend_response.is_success:
            return JSONResponse(
                content = delete_friend_response.to_dict(),
                status_code = delete_friend_response.response_codes_json
            )

        return JSONResponse(
            content = delete_friend_response.to_dict(),
            status_code = delete_friend_response.response_codes_json
        )
    except Exception as e:
        error_response = DeleteFriendResponse(
            is_success = False,
            message = f"unexpected error in delete-friend in controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )