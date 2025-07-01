from select import select

from src.application.mappers.user_mapper import UserMapper
from src.core.interfaces.repository.abstract_friend_repository import AbstractFriendRepository
from src.core.model.entities import User, UserFriend
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


class FriendRepository(AbstractFriendRepository):
    def __init__(self, session):
        self._session = session

    async def get_all_user_friends(self, get_all_user_friends_request: GetAllUserFriendsRequest) -> GetAllUserFriendsResponse:
        try:
            user = await self._session.query(User).filter_by(email = get_all_user_friends_request.email).first()
            if user is None:
                get_all_user_friends_response = GetAllUserFriendsResponse(
                    is_success = False,
                    message = str(f"user not found"),
                    response_codes_json = ResponseCodesJson.NOT_FOUND,
                )
            else:
                user_friends = await self._session.query(UserFriend).filter_by(user_id = user.id).all()
                if len(user_friends) == 0:
                    get_all_user_friends_response = GetAllUserFriendsResponse(
                        is_success = False,
                        message = str(f"user not have any friends"),
                        response_codes_json = ResponseCodesJson.NOT_FOUND
                    )
                else:
                    get_all_user_friends_response = GetAllUserFriendsResponse(
                        is_success = True,
                        message = str(f"user has friends"),
                        response_codes_json = ResponseCodesJson.OK,
                        friends = UserMapper.map_user_list(user_friends)
                    )
        except Exception as e:
            get_all_user_friends_response = GetAllUserFriendsResponse(
                is_success = False,
                message = str(f"unexpected error in get_all_user_friends repository: {e}"),
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR
            )

        return get_all_user_friends_response

    async def add_new_user_friend(self, add_new_user_friend_request: AddNewUserFriendRequest) -> AddNewUserFriendResponse:
        try:
            user = await self._session.query(User).filter_by(email = add_new_user_friend_request.email).first()
            if user is None:
                add_new_user_friend_response = AddNewUserFriendResponse(
                    is_success = False,
                    message = str(f"user not found"),
                    response_codes_json = ResponseCodesJson.NOT_FOUND
                )
            else:
                friend = await self._session.query(User).filter_by(friend_code = add_new_user_friend_request.friend_code).first()
                if friend is None:
                    add_new_user_friend_response = AddNewUserFriendResponse(
                        is_success = False,
                        message = str(f"user not have any friends"),
                        response_codes_json = ResponseCodesJson.NOT_FOUND
                    )
                else:
                    user_friend = UserFriend(
                        user_id = user.id,
                        friend_id = friend.id,
                    )

                    await self._session.add(user_friend)
                    await self._session.commit()

                    add_new_user_friend_response = AddNewUserFriendResponse(
                        is_success = True,
                        message = str(f"user added friend"),
                        response_codes_json = ResponseCodesJson.OK,
                        friend_dto = UserMapper.map_user(friend)
                    )
        except Exception as e:
            add_new_user_friend_response = AddNewUserFriendResponse(
                is_success = False,
                message = str(f"unexpected error in add_new_user_friend repository {e}"),
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR
            )

        return add_new_user_friend_response

    async def delete_friend(self, friend_request: DeleteFriendRequest) -> DeleteFriendResponse:
        try:
            user = await self._session.query(User).filter_by(email = friend_request.email).first()
            if user is None:
                delete_friend_response = DeleteFriendResponse(
                    is_success = False,
                    message = str(f"user not found"),
                    response_codes_json = ResponseCodesJson.NOT_FOUND
                )
            else:
                friend = await self._session.query(User).filter_by(email = friend_request.friend_email).first()
                if friend is None:
                    delete_friend_response = DeleteFriendResponse(
                        is_success = False,
                        message = str(f"friend not found"),
                        response_codes_json = ResponseCodesJson.NOT_FOUND
                    )
                else:
                    user_friend = (await self._session.execute(
                        select(UserFriend).where(
                            (UserFriend.user_id == friend.user_id) &
                            (UserFriend.friend_id == friend.friend_id)
                        )
                    )).scalars().first()
                    if user_friend is None:
                        delete_friend_response = DeleteFriendResponse(
                            is_success = False,
                            message = str(f"they are not friends"),
                            response_codes_json = ResponseCodesJson.NOT_FOUND
                        )
                    else:
                        await self._session.delete(user_friend)
                        await self._session.commit()

                        delete_friend_response = DeleteFriendResponse(
                            is_success = True,
                            message = str(f"friend deleted"),
                            response_codes_json = ResponseCodesJson.OK,
                            user_dto = UserMapper.map_user(user)
                        )
        except Exception as e:
            delete_friend_response = DeleteFriendResponse(
                is_success = False,
                message = str(f"unexpected error in delete_friend repository {e}"),
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR
            )

        return delete_friend_response