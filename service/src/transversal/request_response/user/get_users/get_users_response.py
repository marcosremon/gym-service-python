from typing import List, Optional

from src.application.dto.user_dto import UserDTO
from src.transversal.common.base_response import BaseResponse

class GetUsersResponse(BaseResponse):
    users: Optional[List[UserDTO]] = None