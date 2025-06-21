from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.service.configuration.dependency_injection import get_user_application
from src.transversal.request_response.split_day.update_split_day.update_split_day_request import UpdateSplitDayRequest
from src.transversal.request_response.split_day.update_split_day.update_split_day_response import UpdateSplitDayResponse

http = APIRouter(prefix="/api/split-day")

@http.post("/update-split-day", response_model = UpdateSplitDayResponse)
async def update_split_day(update_split_day_request: UpdateSplitDayRequest, application = Depends(get_user_application)):
    try:
        update_split_day_response = await application.update_split_day(update_split_day_request)
        if update_split_day_response.is_success:
            return JSONResponse(
                content = update_split_day_response.to_dict(),
                status_code = update_split_day_response.status_code,
            )

        return JSONResponse(
            content = update_split_day_response.to_dict(),
            status_code = update_split_day_response.status_code,
        )
    except Exception as e:
        error_response = UpdateSplitDayResponse(
            is_success = False,
            message = f"unexpected error in update-split-day controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.status_code,
        )