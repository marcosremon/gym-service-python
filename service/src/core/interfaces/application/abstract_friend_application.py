from abc import ABC, abstractmethod

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


class AbstractFriendApplication(ABC):
    @abstractmethod
    async def get_all_user_friends(self, get_all_user_friends_request: GetAllUserFriendsRequest) -> GetAllUserFriendsResponse:
        pass

    @abstractmethod
    async def add_new_user_friend(self, add_new_user_friend_request: AddNewUserFriendRequest) -> AddNewUserFriendResponse:
        pass

    @abstractmethod
    async def delete_friend(self, friend_request: DeleteFriendRequest) -> DeleteFriendResponse:
        pass