from src.core.interfaces.application.abstract_routine_application import AbstractRoutineApplication
from src.infraestructure.persistence.routine_repository import RoutineRepository
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

class RoutineApplication(AbstractRoutineApplication):
    def __init__(self, repository: RoutineRepository):
        self._repository = repository

    async def create_routine(self, create_routine_request: CreateRoutineRequest) -> CreateRoutineResponse:
        if create_routine_request.email is None or create_routine_request.routine_name is None:
            return CreateRoutineResponse(
                is_success = False,
                message = "routine or email is required",
                response_codes_json = 400
            )

        return await self._repository.create_routine(create_routine_request)

    async def update_routine(self, update_routine_request: UpdateRoutineRequest) -> UpdateRoutineResponse:
        if update_routine_request.routine_id is None or update_routine_request.routine_name is None:
            return UpdateRoutineResponse(
                is_success = False,
                message = "routine or email is required",
                response_codes_json = 400
            )

        return await self._repository.update_routine(update_routine_request)

    async def delete_routine(self, delete_routine_request: DeleteRoutineRequest) -> DeleteRoutineResponse:
        if delete_routine_request.email is None or delete_routine_request.routine_name is None:
            return DeleteRoutineResponse(
                is_success = False,
                message = f"routine id or email is required",
            )

        return await self._repository.delete_routine(delete_routine_request)

    async def get_all_user_routines(self, get_all_user_routines_request: GetAllUserRoutinesRequest) -> GetAllUserRoutinesResponse:
        if get_all_user_routines_request.email is None:
            return GetAllUserRoutinesResponse(
                is_success = False,
                message = "routine or email is required",
                response_codes_json = 400
            )

        return await self._repository.get_all_user_routines(get_all_user_routines_request)

    async def get_routine_stats(self, get_routine_stats_request: GetRoutineStatsRequest) -> GetRoutineStatsResponse:
        if get_routine_stats_request.email is None:
            return GetRoutineStatsResponse(
                is_success = False,
                message = "email is required",
                response_codes_json = 400
            )

        return await self._repository.get_routine_stats(get_routine_stats_request)

    async def get_routine_by_id(self, get_routine_by_id: GetRoutineByIdRequest) -> GetRoutineByIdResponse:
        if get_routine_by_id.routine_id is None:
            return GetRoutineByIdResponse(
                is_success = False,
                message = "routine id or email is required",
                response_codes_json = 400
            )

        return await self._repository.get_routine_by_id(get_routine_by_id)