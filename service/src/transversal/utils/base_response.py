from pydantic import BaseModel

from src.transversal.utils.response_codes_json import ResponseCodesJson

class BaseResponse(BaseModel):
    message: str
    is_success: bool
    response_codes_json: int