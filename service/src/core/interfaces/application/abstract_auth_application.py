from abc import ABC, abstractmethod

from src.transversal.request_response.auth.check_token_status.check_token_status_request import CheckTokenStatusRequest
from src.transversal.request_response.auth.check_token_status.check_token_status_response import \
    CheckTokenStatusResponse
from src.transversal.request_response.auth.login.login_request import LoginRequest
from src.transversal.request_response.auth.login.login_response import LoginResponse
from src.transversal.request_response.auth.login_web.login_web_request import LoginWebRequest
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

class AbstractAuthApplication(ABC):
    @abstractmethod
    async def login(self, login_request: LoginRequest) -> LoginResponse:
        pass

    @abstractmethod
    async def login_web(self, login_web_request: LoginWebRequest) -> LoginWebResponse:
        pass

    @abstractmethod
    async def check_token_status(self, check_token_status_request: CheckTokenStatusRequest) -> CheckTokenStatusResponse:
        pass