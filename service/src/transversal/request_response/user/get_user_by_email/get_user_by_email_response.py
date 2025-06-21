from typing import Optional

from src.application.dto.user_dto import UserDTO
from src.transversal.common.base_response import BaseResponse

class GetUserByEmailResponse(BaseResponse):
    user_dto: Optional[UserDTO] = None
    routines_count: int = 0
    friends_count: int = 0