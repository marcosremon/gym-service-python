from dataclasses import dataclass

from src.transversal.utils.response_codes_json import ResponseCodesJson

@dataclass
class BaseResponse:
    message: str
    isSuccess: bool
    responseCodeJson: ResponseCodesJson