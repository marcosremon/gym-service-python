from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.infraestructure.dependency.dependency_injection import get_user_application
from src.transversal.common.response_codes_json import ResponseCodesJson
from src.transversal.request_response.routine.create_routine.create_routine_request import CreateRoutineRequest
from src.transversal.request_response.routine.create_routine.create_routine_response import CreateRoutineResponse
from src.transversal.request_response.routine.delete_routine.delete_routine_request import DeleteRoutineRequest
from src.transversal.request_response.routine.delete_routine.delete_routine_response import DeleteRoutineResponse
from src.transversal.request_response.routine.get_all_user_routine.get_all_user_routines_request import \
    GetAllUserRoutinesRequest
from src.transversal.request_response.routine.get_all_user_routine.get_all_user_routines_response import \
    GetAllUserRoutinesResponse
from src.transversal.request_response.routine.get_routine_by_id.get_routine_by_id_request import GetRoutineByIdRequest
from src.transversal.request_response.routine.get_routine_by_id.get_routine_by_id_response import GetRoutineByIdResponse
from src.transversal.request_response.routine.get_routine_stats.get_routine_stats_request import GetRoutineStatsRequest
from src.transversal.request_response.routine.get_routine_stats.get_routine_stats_response import \
    GetRoutineStatsResponse
from src.transversal.request_response.routine.update_routine.update_routine_request import UpdateRoutineRequest
from src.transversal.request_response.routine.update_routine.update_routine_response import UpdateRoutineResponse

http = APIRouter(prefix="/api/routine")

@http.post("/create-routine", response_model = CreateRoutineResponse)
async def create_routine(create_routine_request: CreateRoutineRequest, application = Depends(get_user_application)):
    try:
        if (create_routine_request is None or create_routine_request.email is None
                or create_routine_request.routine_name is None or create_routine_request.routine_description is None):
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = CreateRoutineResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, email, routine_name or routine_description is null or empty")
                ).disc()
            )
        else:
            create_routine_response = await application.create_routine(create_routine_request)
            if create_routine_response.is_success:
                json_response = JSONResponse(
                    status_code = create_routine_response.response_codes_json,
                    content = CreateRoutineResponse(
                        response_codes_json = create_routine_response.response_codes_json,
                        is_success = create_routine_response.is_success,
                        message = create_routine_response.message,
                        routine_dto = create_routine_response.routine_dto
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = create_routine_response.response_codes_json,
                    content = CreateRoutineResponse(
                        response_codes_json = create_routine_response.response_codes_json,
                        is_success = create_routine_response.is_success,
                        message = create_routine_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = CreateRoutineResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on create-routine controller: {e}"),
            )
        )

    return json_response

@http.post("/update-routine", response_model = UpdateRoutineResponse)
async def update_routine(update_routine_request: UpdateRoutineRequest, application = Depends(get_user_application)):
    try:
        if update_routine_request is None or update_routine_request.routine_id or update_routine_request.routine_name is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = UpdateRoutineResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, routine_id or routine_name is null or empty")
                )
            )
        else:
            update_routine_response = await application.update_routine(update_routine_request)
            if update_routine_response.is_success:
                json_response = JSONResponse(
                    status_code = update_routine_response.response_codes_json,
                    content = UpdateRoutineResponse(
                        response_codes_json = update_routine_response.response_codes_json,
                        is_success = update_routine_response.is_success,
                        message = update_routine_response.message,
                        routine_dto = update_routine_response.routine_dto
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = update_routine_response.response_codes_json,
                    content = UpdateRoutineResponse(
                        response_codes_json = update_routine_response.response_codes_json,
                        is_success = update_routine_response.is_success,
                        message = update_routine_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = UpdateRoutineResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on update-routine controller: {e}"),
            )
        )

    return json_response

@http.post("/delete-routine", response_model = DeleteRoutineResponse)
async def delete_routine(delete_routine_request: DeleteRoutineRequest, application = Depends(get_user_application)):
    try:
        if delete_routine_request is None or delete_routine_request.routine_id or delete_routine_request.email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = DeleteRoutineResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, routine_id or email is null or empty")
                )
            )
        else:
            delete_routine_response = await application.delete_routine(delete_routine_request)
            if delete_routine_response.is_success:
                json_response = JSONResponse(
                    status_code = delete_routine_response.response_codes_json,
                    content = DeleteRoutineResponse(
                        response_codes_json = delete_routine_response.response_codes_json,
                        is_success = delete_routine_response.is_success,
                        message = delete_routine_response.message,
                        routine_dto = delete_routine_response.routine_dto
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = delete_routine_response.response_codes_json,
                    content = DeleteRoutineResponse(
                        response_codes_json = delete_routine_response.response_codes_json,
                        is_success = delete_routine_response.is_success,
                        message = delete_routine_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = DeleteRoutineResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on delete-routine controller: {e}"),
            )
        )

    return json_response

@http.post("/get-all-user-routines", response_model = GetAllUserRoutinesResponse)
async def get_all_user_routines(get_all_user_routines_request: GetAllUserRoutinesRequest, application = Depends(get_user_application)):
    try:
        if get_all_user_routines_request is None or get_all_user_routines_request.email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = GetAllUserRoutinesResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, routine_id or email is null or empty")
                )
            )
        else:
            get_all_user_routines_response = await application.get_all_user_routines(get_all_user_routines_request)
            if get_all_user_routines_response.is_success:
                json_response = JSONResponse(
                    status_code = get_all_user_routines_response.response_codes_json,
                    content = GetAllUserRoutinesResponse(
                        response_codes_json = get_all_user_routines_response.response_codes_json,
                        is_success = get_all_user_routines_response.is_success,
                        message = get_all_user_routines_response.message,
                        routines_dto = get_all_user_routines_response.routines_dto
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = get_all_user_routines_response.response_codes_json,
                    content = GetAllUserRoutinesResponse(
                        response_codes_json = get_all_user_routines_response.response_codes_json,
                        is_success = get_all_user_routines_response.is_success,
                        message = get_all_user_routines_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = GetAllUserRoutinesResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on get-all-user-routines controller: {e}"),
            )
        )

    return json_response

@http.post("/get-routine-stats", response_model = GetRoutineStatsResponse)
async def get_routine_stats(get_routine_stats_request: GetRoutineStatsRequest, application = Depends(get_user_application)):
    try:
        if get_routine_stats_request is None or get_routine_stats_request.email is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = GetRoutineStatsResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, routine_id or email is null or empty")
                )
            )
        else:
            get_routine_stats_response = await application.get_routine_stats(get_routine_stats_request)
            if get_routine_stats_response.is_success:
                json_response = JSONResponse(
                    status_code = get_routine_stats_response.response_codes_json,
                    content = GetRoutineStatsResponse(
                        response_codes_json = get_routine_stats_response.response_codes_json,
                        is_success = get_routine_stats_response.is_success,
                        message = get_routine_stats_response.message,
                        routines_count = get_routine_stats_response.routines_count,
                        exercises_count = get_routine_stats_response.exercises_count,
                        splits_count = get_routine_stats_response.splits_count,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = get_routine_stats_response.response_codes_json,
                    content = GetRoutineStatsResponse(
                        response_codes_json = get_routine_stats_response.response_codes_json,
                        is_success = get_routine_stats_response.is_success,
                        message = get_routine_stats_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = GetRoutineStatsResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on get-routine-stats controller: {e}"),
            )
        )

    return json_response

@http.post("/get-routine-by-id", response_model = GetRoutineByIdResponse)
async def get_routine_by_id(get_routine_by_id_request: GetRoutineByIdRequest, application = Depends(get_user_application)):
    try:
        if get_routine_by_id_request is None or get_routine_by_id_request.routine_id is None:
            json_response = JSONResponse(
                status_code = ResponseCodesJson.BAD_REQUEST,
                content = GetRoutineByIdResponse(
                    response_codes_json = ResponseCodesJson.BAD_REQUEST,
                    is_success = False,
                    message = str(f"invalid data, routine_id or email is null or empty")
                )
            )
        else:
            get_routine_by_id_response = await application.get_routine_by_id(get_routine_by_id_request)
            if get_routine_by_id_response.is_success:
                json_response = JSONResponse(
                    status_code = get_routine_by_id_response.response_codes_json,
                    content = GetRoutineByIdResponse(
                        response_codes_json = get_routine_by_id_response.response_codes_json,
                        is_success = get_routine_by_id_response.is_success,
                        message = get_routine_by_id_response.message,
                        routine_dto = get_routine_by_id_response.routine_dto,
                    )
                )
            else:
                json_response = JSONResponse(
                    status_code = get_routine_by_id_response.response_codes_json,
                    content = GetRoutineByIdResponse(
                        response_codes_json = get_routine_by_id_response.response_codes_json,
                        is_success = get_routine_by_id_response.is_success,
                        message = get_routine_by_id_response.message,
                    )
                )
    except Exception as e:
        json_response = JSONResponse(
            status_code = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            content = GetRoutineByIdResponse(
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
                is_success = False,
                message = str(f"unexpected error on get-routine-by-id: {e}"),
            )
        )

    return json_response