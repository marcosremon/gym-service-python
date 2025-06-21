from typing import Optional

from src.transversal.common.base_response import BaseResponse

class LoginResponse(BaseResponse):
    token: Optional[str] = None
    is_admin: Optional[bool] = None