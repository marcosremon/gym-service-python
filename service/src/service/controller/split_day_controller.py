from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.infraestructure.dependency.dependency_injection import get_user_application
from src.transversal.common.response_codes_json import ResponseCodesJson
from src.transversal.request_response.split_day.update_split_day.update_split_day_request import UpdateSplitDayRequest
from src.transversal.request_response.split_day.update_split_day.update_split_day_response import UpdateSplitDayResponse

http = APIRouter(prefix="/api/split-day")

@http.post("/update-split-day", response_model = UpdateSplitDayResponse)
async def update_split_day(update_split_day_request: UpdateSplitDayRequest, application = Depends(get_user_application)):
    try:
        if update_split_day_request is None or update_split_day_request.routine_id is None or update_split_day_request.email is None:
           json_response = JSONResponse(
               status_code = ResponseCodesJson.BAD_REQUEST,
               content = UpdateSplitDayResponse(
                   response_codes_json = ResponseCodesJson.BAD_REQUEST,
                   is_success = False,
                   message = str(f"invalid data routine id and email is required"),
               )
           )
        else:
            update_split_day_response = await application.update_split_day(update_split_day_request)
            if update_split_day_response.is_success:
                json_response = JSONResponse(
                    status_code = update_split_day_response.response_codes_json,
                    content = UpdateSplitDayResponse(
                        response_codes_json = update_split_day_response.response_codes_json,
                        is_success = update_split_day_response.is_success,
                        message = update_split_day_response.is_success,
                        user_dto = update_split_day_response.user_dto,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = update_split_day_response.response_codes_json,
                    content = UpdateSplitDayResponse(
                        response_codes_json = update_split_day_response.response_codes_json,
                        is_success = update_split_day_response.is_success,
                        message = update_split_day_response.is_success,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = UpdateSplitDayResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on update-split-day controller: {e}"),
            ),
        )

    return json_response