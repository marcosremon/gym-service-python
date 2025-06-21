from typing import Optional, List

from src.application.dto.user_dto import UserDTO
from src.transversal.common.base_response import BaseResponse

class DeleteFriendResponse(BaseResponse):
    user_dto: Optional[UserDTO] = None