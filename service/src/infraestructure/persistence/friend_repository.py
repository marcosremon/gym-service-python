from select import select

from src.application.mappers.user_mapper import UserMapper
from src.core.interfaces.repository.abstract_friend_repository import AbstractFriendRepository
from src.core.model.entities import User, UserFriend
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


class FriendRepository(AbstractFriendRepository):
    def __init__(self, session):
        self._session = session

    async def get_all_user_friends(self, get_all_user_friends_request: GetAllUserFriendsRequest) -> GetAllUserFriendsResponse:
        try:
            user = await self._session.query(User).filter_by(email = get_all_user_friends_request.email).first()
            if user is None:
                return GetAllUserFriendsResponse(
                    is_success = False,
                    message = "user not found",
                    response_codes_json = 404
                )

            user_friends = await self._session.query(UserFriend).filter_by(user_id = user.id).all()
            if len(user_friends) == 0:
                return GetAllUserFriendsResponse(
                    is_success = False,
                    message = "user not have any friends",
                    response_codes_json = 404
                )

            return GetAllUserFriendsResponse(
                is_success = True,
                message = "user has friends",
                response_codes_json = 200,
                friends = UserMapper.map_user_list(user_friends)
            )
        except Exception as e:
            return GetAllUserFriendsResponse(
                is_success = False,
                message = f"unexpected error in get_all_user_friends repository: {e}",
                response_codes_json = 500
            )

    async def add_new_user_friend(self, add_new_user_friend_request: AddNewUserFriendRequest) -> AddNewUserFriendResponse:
        try:
            user = await self._session.query(User).filter_by(email = add_new_user_friend_request.email).first()
            if user is None:
                return AddNewUserFriendResponse(
                    is_success = False,
                    message = "user not found",
                    response_codes_json = 404
                )

            friend = await self._session.query(User).filter_by(friend_code = add_new_user_friend_request.friend_code).first()
            if friend is None:
                return AddNewUserFriendResponse(
                    is_success = False,
                    message = "user not have any friends",
                    response_codes_json = 404
                )

            user_friend = UserFriend(
                user_id = user.id,
                friend_id = friend.id,
            )

            await self._session.add(user_friend)
            await self._session.commit()

            return AddNewUserFriendResponse(
                is_success = True,
                message = "user added friend",
                response_codes_json = 200,
                friend_dto = UserMapper.map_user(friend)
            )
        except Exception as e:
            return AddNewUserFriendResponse(
                is_success = False,
                message = f"unexpected error in add_new_user_friend repository {e}",
                response_codes_json = 500
            )

    async def delete_friend(self, friend_request: DeleteFriendRequest) -> DeleteFriendResponse:
        try:
            user = await self._session.query(User).filter_by(email = friend_request.email).first()
            if user is None:
                return DeleteFriendResponse(
                    is_success = False,
                    message = "user not found",
                    response_codes_json = 404
                )

            friend = await self._session.query(User).filter_by(email = friend_request.friend_email).first()
            if friend is None:
                return DeleteFriendResponse(
                    is_success = False,
                    message = "friend not found",
                    response_codes_json = 404
                )

            user_friend = await self._session.scalars(
                select(UserFriend)
                .Where(
                    (UserFriend.user_id == friend.user_id) &
                    (UserFriend.friend_id == friend.friend_id)
                ).first()
            )
            if user_friend is None:
                return DeleteFriendResponse(
                    is_success = False,
                    message = "they are not friends",
                    response_codes_json = 404
                )

            await self._session.delete(user_friend)
            await self._session.commit()

            return DeleteFriendResponse(
                is_success = True,
                message = "friend deleted",
                response_codes_json = 200,
                user_dto = UserMapper.map_user(user)
            )
        except Exception as e:
            return DeleteFriendResponse(
                is_success = False,
                message = f"unexpected error in delete_friend repository {e}",
                response_codes_json = 500
            )