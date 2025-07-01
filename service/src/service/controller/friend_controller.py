from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.infraestructure.dependency.dependency_injection import get_user_application
from src.transversal.common.response_codes_json import ResponseCodesJson
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
        if get_all_user_friends_request is None or get_all_user_friends_request.email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = GetAllUserFriendsResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, email is required")
                )
            )
        else:
            get_all_user_friends_response = await application.get_all_user_friends(get_all_user_friends_request)
            if get_all_user_friends_response.is_success:
                json_response = JSONResponse(
                    status_code = get_all_user_friends_response.response_codes_json,
                    content = GetAllUserFriendsResponse(
                        response_codes_json = get_all_user_friends_response.response_codes_json,
                        is_success = get_all_user_friends_response.is_success,
                        message = get_all_user_friends_response.message,
                        friends = get_all_user_friends_response.friends,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = get_all_user_friends_response.response_codes_json,
                    content = GetAllUserFriendsResponse(
                        response_codes_json = get_all_user_friends_response.response_codes_json,
                        is_success = get_all_user_friends_response.is_success,
                        message = get_all_user_friends_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = GetAllUserFriendsResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on get-all-user-friend controller: {e}")
            )
        )

    return json_response

@http.post("/add-new-user-friend", response_model = AddNewUserFriendResponse)
async def add_new_user_friend(add_new_user_friend_request: AddNewUserFriendRequest, application = Depends(get_user_application)):
    try:
        if add_new_user_friend_request is None or add_new_user_friend_request.email is None or add_new_user_friend_request.friend_code is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = AddNewUserFriendResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, email or friend code are required")
                )
            )
        else:
            add_new_user_friend_response = await application.get_all_user_friends(add_new_user_friend_request)
            if add_new_user_friend_response.is_success:
                json_response = JSONResponse(
                    status_code = add_new_user_friend_response.response_codes_json,
                    content = AddNewUserFriendResponse(
                        response_codes_json = add_new_user_friend_response.response_codes_json,
                        is_success = add_new_user_friend_response.is_success,
                        message = add_new_user_friend_response.message,
                        friend_dto = add_new_user_friend_response.friend_dto,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = add_new_user_friend_response.response_codes_json,
                    content = AddNewUserFriendResponse(
                        response_codes_json = add_new_user_friend_response.response_codes_json,
                        is_success = add_new_user_friend_response.is_success,
                        message = add_new_user_friend_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = AddNewUserFriendResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on add-new-user-friend controller: {e}")
            )
        )

    return json_response

@http.post("/delete-friend", response_model = DeleteFriendResponse)
async def get_all_user_friends(delete_friend_request: DeleteFriendRequest, application = Depends(get_user_application)):
    try:
        if delete_friend_request is None or delete_friend_request.email is None or delete_friend_request.friend_email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = DeleteFriendResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, email or friend code are required")
                )
            )
        else:
            delete_friend_response = await application.get_all_user_friends(delete_friend_request)
            if delete_friend_response.is_success:
                json_response = JSONResponse(
                    status_code = delete_friend_response.response_codes_json,
                    content = DeleteFriendResponse(
                        response_codes_json = delete_friend_response.response_codes_json,
                        is_success = delete_friend_response.is_success,
                        message = delete_friend_response.message,
                        user_dto = delete_friend_response.user_dto,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = delete_friend_response.response_codes_json,
                    content = DeleteFriendResponse(
                        response_codes_json = delete_friend_response.response_codes_json,
                        is_success = delete_friend_response.is_success,
                        message = delete_friend_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = DeleteFriendResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on delete-friend: {e}")
            )
        )

    return json_response