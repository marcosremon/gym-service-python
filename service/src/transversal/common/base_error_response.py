from pydantic import BaseModel

from src.transversal.common.response_codes_json import ResponseCodesJson

class BaseErrorResponse(BaseModel):
    is_success: bool = False
    response_codes_json: ResponseCodesJson = ResponseCodesJson.BAD_REQUEST
    message: str = str("error, invalid data, the data is null or empty")

    def dict(self, **kwargs):
        return super().dict(**kwargs)