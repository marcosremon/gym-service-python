from typing import Optional

from src.transversal.common.base_response import BaseResponse

class CheckTokenStatusResponse(BaseResponse):
    is_valid: Optional[bool] = None