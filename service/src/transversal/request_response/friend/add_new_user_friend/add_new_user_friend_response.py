from typing import Optional

from src.application.dto.user_dto import UserDTO
from src.transversal.common.base_response import BaseResponse

class AddNewUserFriendResponse(BaseResponse):
    friend_dto: Optional[UserDTO] = None