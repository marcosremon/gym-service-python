from select import select
from src.application.mappers.routine_mapper import RoutineMapper
from src.core.interfaces.repository.abstract_routine_repository import AbstractRoutineRepository
from src.core.model.entities import User, Routine
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

class RoutineRepository(AbstractRoutineRepository):
    def __init__(self, session):
        self._session = session

    async def create_routine(self, create_routine_request: CreateRoutineRequest) -> CreateRoutineResponse:
        try:
            user = await self._session.query(User).filter_by(email=create_routine_request.email).first()
            if user is None:
                return CreateRoutineResponse(
                    is_success = False,
                    message = "No user found with that email",
                    response_codes_json = 404,
                )

            exists_routine = await self._session.scalar(
                select(Routine).where(
                    Routine.routine_name == create_routine_request.routine_name,
                    Routine.user_id == user.user_id
                ).exists()
            )

            if exists_routine:
                return CreateRoutineResponse(
                    is_success = False,
                    message = "Routine already exists",
                    response_codes_json = 404,
                )

            routine = Routine(
                routine_name = create_routine_request.routine_name,
                routine_description = create_routine_request.routine_description if create_routine_request.routine_description else "Rutina sin descripcion",
                user_id = user.user_id,
            )

            await self._session.add(routine)
            await self._session.commit()

            return CreateRoutineResponse(
                is_success = True,
                message = "Routine created successfully",
                response_codes_json = 200,
                routine_dto = RoutineMapper.map_routine(routine)
            )
        except Exception as e:
            return CreateRoutineResponse(
                is_success = False,
                message = f"unexpected error in create-routine-repository {e}",
                response_codes_json = 500,
            )

    async def update_routine(self, update_routine_request: UpdateRoutineRequest) -> UpdateRoutineResponse:
        try:
            routine = await self._session.query(Routine).filter_by(routine_id = update_routine_request.routine_id).first()
            if routine is None:
                return UpdateRoutineResponse(
                    is_success = False,
                    message = "Routine not found",
                    response_codes_json = 404,
                )

            routine.routine_name = update_routine_request.routine_name
            routine.routine_description = update_routine_request.routine_description

            await self._session.commit()

            return UpdateRoutineResponse(
                is_success = True,
                message = "Routine updated successfully",
                response_codes_json = 200,
                routine_dto = RoutineMapper.map_routine(routine)
            )
        except Exception as e:
            return UpdateRoutineResponse(
                is_success = False,
                message = f"unexpected error in update-routine-repository {e}",
                response_codes_json = 500,
            )

    async def delete_routine(self, delete_routine_request: DeleteRoutineRequest) -> DeleteRoutineResponse:
        try:
            user = await self._session.query(User).filter_by(email = delete_routine_request.email).first()
            if user is None:
                return DeleteRoutineResponse(
                    is_success = False,
                    message = "No user found with that email",
                    response_codes_json = 404,
                )

            routine = await self._session.query(Routine).filter_by(routine_id = delete_routine_request.routine_id).first()
            if routine is None:
                return DeleteRoutineResponse(
                    is_success = False,
                    message = "Routine not found",
                    response_codes_json = 404,
                )

            exist_routine_in_user_list = user.routines.filter(routine_id = delete_routine_request.routine_id).exists()
            if not exist_routine_in_user_list:
                return DeleteRoutineResponse(
                    is_success = False,
                    message = "Routine not found",
                    response_codes_json = 404,
                )

            if routine in user.routines:
                user.routines.remove(routine)

            await self._session.delete(routine)
            await self._session.commit()

            return DeleteRoutineResponse(
                is_success = True,
                message = "Routine deleted successfully",
                response_codes_json = 200,
                routine_dto = RoutineMapper.map_routine(routine)
            )
        except Exception as e:
            return DeleteRoutineResponse(
                is_success = False,
                message = f"unexpected error in delete-routine-repository {e}",
                response_codes_json = 500,
            )

    async def get_all_user_routines(self, get_all_user_routines_request: GetAllUserRoutinesRequest) -> GetAllUserRoutinesResponse:
        try:
            user = await self._session.query(User).filter_by(email = get_all_user_routines_request.email).first()
            if user is None:
                return GetAllUserRoutinesResponse(
                    is_success = False,
                    message = "No user found with that email",
                    response_codes_json = 404,
                )

            if user.routines.count() == 0:
                return GetAllUserRoutinesResponse(
                    is_success = False,
                    message = "user routine not found",
                    response_codes_json = 404,
                )

            return GetAllUserRoutinesResponse(
                is_success = True,
                message = "get user routines successfully",
                response_codes_json = 200,
                routines_dto = RoutineMapper.map_routine_list(user.routines),
            )
        except Exception as e:
            return GetAllUserRoutinesResponse(
                is_success = False,
                message = f"unexpected error in get-all-user-routines-repository {e}",
                response_codes_json = 500,
            )

    async def get_routine_stats(self, get_routine_stats_request: GetRoutineStatsRequest) -> GetRoutineStatsResponse:
        try:
            user = await self._session.query(User).filter_by(email = get_routine_stats_request.email).first()
            if user is None:
                return GetRoutineStatsResponse(
                    is_success = False,
                    message = "No user found with that email",
                    response_codes_json = 404,
                )

            splits = []
            for routine in user.routines:
                splits.append(routine.split_days)

            exercises = []
            for split_day in splits:
                exercises.append(split_day.exercises)

            return GetRoutineStatsResponse(
                is_success = True,
                message = "get routine stats successfully",
                response_codes_json = 200,
                routines_count = len(user.routines),
                splits_count = len(splits),
                exercises_count = len(exercises),
            )
        except Exception as e:
            return GetRoutineStatsResponse(
                is_success = False,
                message = f"unexpected error in get-routine-stats-repository {e}",
                response_codes_json = 500,
            )

    async def get_routine_by_id(self, get_routine_by_id: GetRoutineByIdRequest) -> GetRoutineByIdResponse:
        try:
            routine = await self._session.query(Routine).filter_by(id = get_routine_by_id.id).first()
            if routine is None:
                return GetRoutineByIdResponse(
                    is_success = False,
                    message = "routine not found",
                    response_codes_json = 404,
                )

            return GetRoutineByIdResponse(
                is_success = True,
                message = "get routine by id successfully",
                response_codes_json = 200,
                routine_dto = RoutineMapper.map_routine(routine)
            )
        except Exception as e:
            return GetRoutineByIdResponse(
                is_success = False,
                message = f"unexpected error in get-routine-by-id-repository {e}",
                response_codes_json = 500,
            )