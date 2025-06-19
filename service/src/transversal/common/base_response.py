from pydantic import BaseModel


class BaseResponse(BaseModel):
    message: str
    is_success: bool
    response_codes_json: int