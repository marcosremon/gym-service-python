from typing import Optional
from src.application.dto.user_dto import UserDTO
from src.transversal.common.base_response import BaseResponse

class CreateGoogleUserResponse(BaseResponse):
    user_dto: Optional[UserDTO] = None