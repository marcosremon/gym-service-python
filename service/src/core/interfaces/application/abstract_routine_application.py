from abc import ABC, abstractmethod

from src.application.dto.routine_dto import RoutineDTO
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


class AbstractRoutineApplication(ABC):
    @abstractmethod
    async def create_routine(self, create_routine_request: CreateRoutineRequest) -> CreateRoutineResponse:
        pass

    @abstractmethod
    async def update_routine(self, update_routine_request: UpdateRoutineRequest) -> UpdateRoutineResponse:
        pass

    @abstractmethod
    async def delete_routine(self, delete_routine_request: DeleteRoutineRequest) -> DeleteRoutineResponse:
        pass

    @abstractmethod
    async def get_all_user_routines(self, get_all_user_routines_request: GetAllUserRoutinesRequest) -> GetAllUserRoutinesResponse:
        pass

    @abstractmethod
    async def get_routine_stats(self, get_routine_stats_request: GetRoutineStatsRequest) -> GetRoutineStatsResponse:
        pass

    @abstractmethod
    async def get_routine_by_id(self, get_routine_by_id: GetRoutineByIdRequest) -> GetRoutineByIdResponse:
        pass