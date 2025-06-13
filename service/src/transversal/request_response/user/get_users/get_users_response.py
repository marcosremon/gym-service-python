from dataclasses import dataclass
from typing import List

from src.application.dto.user_dto import UserDTO
from src.transversal.utils.base_response import BaseResponse

class GetUsersResponse(BaseResponse):
    users: List[UserDTO]