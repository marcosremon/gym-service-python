from src.core.interfaces.application.abstract_friend_application import AbstractFriendApplication
from src.infraestructure.persistence.friend_repository import FriendRepository
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

class FriendApplication(AbstractFriendApplication):
    def __init__(self, repository: FriendRepository):
        self._repository = repository

    async def get_all_user_friends(self, get_all_user_friends_request: GetAllUserFriendsRequest) -> GetAllUserFriendsResponse:
        if get_all_user_friends_request.email is None:
            return GetAllUserFriendsResponse(
                is_success = False,
                message = "email is required",
                response_codes_json = 400
            )

        return await self._repository.get_all_user_friends(get_all_user_friends_request)

    async def add_new_user_friend(self, add_new_user_friend_request: AddNewUserFriendRequest) -> AddNewUserFriendResponse:
        if add_new_user_friend_request.email is None or add_new_user_friend_request.friends is None:
            return AddNewUserFriendResponse(
                is_success = False,
                message = "email is required",
                response_codes_json = 400
            )

        return await self._repository.add_new_user_friend(add_new_user_friend_request)

    async def delete_friend(self, friend_request: DeleteFriendRequest) -> DeleteFriendResponse:
        if friend_request.email is None or friend_request.friend_email is None:
            return DeleteFriendResponse(
                is_success = False,
                message = "email or friend email is required",
                response_codes_json = 400
            )

        return await self._repository.delete_friend(friend_request)