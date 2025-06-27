from typing import Optional
from pydantic import BaseModel

class BaseResponse(BaseModel):
    message: Optional[str] = None
    is_success: Optional[bool] = None
    response_codes_json: Optional[int] = None