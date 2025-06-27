from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.infraestructure.dependency.dependency_injection import get_user_application
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
        create_routine_response = await application.create_routine(create_routine_request)
        if create_routine_response.is_success:
            return JSONResponse(
                content = create_routine_response.to_dict(),
                status_code = create_routine_response.response_codes_json
            )

        return JSONResponse(
            content = create_routine_response.to_dict(),
            status_code = create_routine_response.response_codes_json
        )
    except Exception as e:
        error_response = CreateRoutineResponse(
            is_success = False,
            message = f"Unexpected error in create-routine controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/update-routine", response_model = UpdateRoutineResponse)
async def update_routine(update_routine_request: UpdateRoutineRequest, application = Depends(get_user_application)):
    try:
        update_routine_response = await application.update_routine(update_routine_request)
        if update_routine_response.is_success:
            return JSONResponse(
                content = update_routine_response.to_dict(),
                status_code = update_routine_response.response_codes_json
            )

        return JSONResponse(
            content = update_routine_response.to_dict(),
            status_code = update_routine_response.response_codes_json
        )
    except Exception as e:
        error_response = UpdateRoutineResponse(
            is_success = False,
            message = f"Unexpected error in update-routine controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/delete-routine", response_model = DeleteRoutineResponse)
async def delete_routine(delete_routine_request: DeleteRoutineRequest, application = Depends(get_user_application)):
    try:
        delete_routine_response = await application.delete_routine(delete_routine_request)
        if delete_routine_response.is_success:
            return JSONResponse(
                content = delete_routine_response.to_dict(),
                status_code = delete_routine_response.response_codes_json
            )

        return JSONResponse(
            content = delete_routine_response.to_dict(),
            status_code = delete_routine_response.response_codes_json
        )
    except Exception as e:
        error_response = DeleteRoutineResponse(
            is_success = False,
            message = f"Unexpected error in delete-routine controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/get-all-user-routines", response_model = GetAllUserRoutinesResponse)
async def get_all_user_routines(get_all_user_routines_request: GetAllUserRoutinesRequest, application = Depends(get_user_application)):
    try:
        get_all_user_routines_response = await application.get_all_user_routines(get_all_user_routines_request)
        if get_all_user_routines_response.is_success:
            return JSONResponse(
                content = await get_all_user_routines_response.to_dict(),
                status_code = get_all_user_routines_response.response_codes_json
            )

        return JSONResponse(
            content = await get_all_user_routines_response.to_dict(),
            status_code = get_all_user_routines_response.response_codes_json
        )
    except Exception as e:
        error_response = GetAllUserRoutinesResponse(
            is_success = False,
            message = f"Unexpected error in get-all-user-routines controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/get-routine-stats", response_model = GetRoutineStatsResponse)
async def get_routine_stats(get_routine_stats_request: GetRoutineStatsRequest, application = Depends(get_user_application)):
    try:
        get_routine_stats_response = await application.get_routine_stats(get_routine_stats_request)
        if get_routine_stats_response.is_success:
            return JSONResponse(
                content = await get_routine_stats_response.to_dict(),
                status_code = get_routine_stats_response.response_codes_json
            )

        return JSONResponse(
            content = await get_routine_stats_response.to_dict(),
            status_code = get_routine_stats_response.response_codes_json
        )
    except Exception as e:
        error_response = GetRoutineStatsResponse(
            is_success = False,
            message = f"Unexpected error in get-routine-stats controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )

@http.post("/get-routine-by-id", response_model = GetRoutineByIdResponse)
async def get_routine_by_id(get_routine_by_id_request: GetRoutineByIdRequest, application = Depends(get_user_application)):
    try:
        get_routine_by_id_response = await application.get_routine_by_id(get_routine_by_id_request)
        if get_routine_by_id_response.is_success:
            return JSONResponse(
                content = await get_routine_by_id_response.to_dict(),
                status_code = get_routine_by_id_response.response_codes_json
            )

        return JSONResponse(
            content = await get_routine_by_id_response.to_dict(),
            status_code = get_routine_by_id_response.response_codes_json
        )
    except Exception as e:
        error_response = GetRoutineByIdResponse(
            is_success = False,
            message = f"Unexpected error in get-routine-by-id controller: {e}",
            response_codes_json = 500
        )

        return JSONResponse(
            content = error_response.to_dict(),
            status_code = error_response.response_codes_json
        )