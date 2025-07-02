from select import select
from src.application.mappers.routine_mapper import RoutineMapper
from src.core.interfaces.repository.abstract_routine_repository import AbstractRoutineRepository
from src.core.model.entities import User, Routine
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

class RoutineRepository(AbstractRoutineRepository):
    def __init__(self, session):
        self._session = session

    async def create_routine(self, create_routine_request: CreateRoutineRequest) -> CreateRoutineResponse:
        try:
            user = await self._session.query(User).filter_by(email=create_routine_request.email).first()
            if user is None:
                create_routine_response = CreateRoutineResponse(
                    is_success = False,
                    message = str(f"No user found with that email"),
                    response_codes_json = ResponseCodesJson.NOT_FOUND,
                )
            else:
                exists_routine = await self._session.scalar(
                    select(Routine).where(
                        Routine.routine_name == create_routine_request.routine_name,
                        Routine.user_id == user.user_id
                    ).exists()
                )
                if exists_routine:
                    create_routine_response = CreateRoutineResponse(
                        is_success = False,
                        message = str(f"Routine already exists"),
                        response_codes_json = ResponseCodesJson.NOT_FOUND,
                    )
                else:
                    routine = Routine(
                        routine_name = create_routine_request.routine_name,
                        routine_description = create_routine_request.routine_description if create_routine_request.routine_description else "Rutina sin descripcion",
                        user_id = user.user_id,
                    )

                    await self._session.add(routine)
                    await self._session.commit()

                    create_routine_response = CreateRoutineResponse(
                        is_success = True,
                        message = str(f"Routine created successfully"),
                        response_codes_json = ResponseCodesJson.OK,
                        routine_dto = RoutineMapper.map_routine(routine)
                    )
        except Exception as e:
            create_routine_response = CreateRoutineResponse(
                is_success = False,
                message = str(f"unexpected error in create-routine-repository {e}"),
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            )

        return create_routine_response

    async def update_routine(self, update_routine_request: UpdateRoutineRequest) -> UpdateRoutineResponse:
        try:
            routine = await self._session.query(Routine).filter_by(routine_id = update_routine_request.routine_id).first()
            if routine is None:
                update_routine_response = UpdateRoutineResponse(
                    is_success = False,
                    message = str(f"Routine not found"),
                    response_codes_json = ResponseCodesJson.NOT_FOUND,
                )
            else:
                routine.routine_name = update_routine_request.routine_name
                routine.routine_description = update_routine_request.routine_description

                await self._session.commit()

                update_routine_response = UpdateRoutineResponse(
                    is_success = True,
                    message = "Routine updated successfully",
                    response_codes_json = ResponseCodesJson.OK,
                    routine_dto = RoutineMapper.map_routine(routine)
                )
        except Exception as e:
            update_routine_response = UpdateRoutineResponse(
                is_success = False,
                message = str(f"unexpected error in update-routine-repository {e}"),
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            )

        return update_routine_response

    async def delete_routine(self, delete_routine_request: DeleteRoutineRequest) -> DeleteRoutineResponse:
        try:
            user = await self._session.query(User).filter_by(email = delete_routine_request.email).first()
            if user is None:
                delete_routine_response = DeleteRoutineResponse(
                    is_success = False,
                    message = str(f"No user found with that email"),
                    response_codes_json = ResponseCodesJson.NOT_FOUND,
                )
            else:
                routine = await self._session.query(Routine).filter_by(routine_id = delete_routine_request.routine_id).first()
                if routine is None:
                    delete_routine_response = DeleteRoutineResponse(
                        is_success = False,
                        message = str(f"Routine not found"),
                        response_codes_json = ResponseCodesJson.NOT_FOUND,
                    )
                else:
                    exist_routine_in_user_list = user.routines.filter(routine_id = delete_routine_request.routine_id).exists()
                    if not exist_routine_in_user_list:
                        delete_routine_response = DeleteRoutineResponse(
                            is_success = False,
                            message = str(f"Routine not found"),
                            response_codes_json = ResponseCodesJson.NOT_FOUND,
                        )
                    else:
                        user.routines.remove(routine)
                        await self._session.delete(routine)
                        await self._session.commit()

                        delete_routine_response = DeleteRoutineResponse(
                            is_success = True,
                            message = str(f"Routine deleted successfully"),
                            response_codes_json = ResponseCodesJson.OK,
                            routine_dto = RoutineMapper.map_routine(routine)
                        )
        except Exception as e:
            delete_routine_response = DeleteRoutineResponse(
                is_success = False,
                message = str(f"unexpected error in delete-routine-repository {e}"),
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            )

        return delete_routine_response

    async def get_all_user_routines(self, get_all_user_routines_request: GetAllUserRoutinesRequest) -> GetAllUserRoutinesResponse:
        try:
            user = await self._session.query(User).filter_by(email = get_all_user_routines_request.email).first()
            if user is None:
                get_all_user_routines_response = GetAllUserRoutinesResponse(
                    is_success = False,
                    message = str(f"No user found with that email"),
                    response_codes_json = ResponseCodesJson.NOT_FOUND,
                )
            else:
                if user.routines.count() == 0:
                    get_all_user_routines_response = GetAllUserRoutinesResponse(
                        is_success = False,
                        message = str(f"user routine not found"),
                        response_codes_json = ResponseCodesJson.NOT_FOUND,
                    )
                else:
                    get_all_user_routines_response = GetAllUserRoutinesResponse(
                        is_success = True,
                        message = str(f"get user routines successfully"),
                        response_codes_json = ResponseCodesJson.OK,
                        routines_dto = RoutineMapper.map_routine_list(user.routines),
                    )
        except Exception as e:
            get_all_user_routines_response = GetAllUserRoutinesResponse(
                is_success = False,
                message = str(f"unexpected error in get-all-user-routines-repository {e}"),
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            )

        return get_all_user_routines_response

    async def get_routine_stats(self, get_routine_stats_request: GetRoutineStatsRequest) -> GetRoutineStatsResponse:
        try:
            user = await self._session.query(User).filter_by(email = get_routine_stats_request.email).first()
            if user is None:
                get_routine_stats_response = GetRoutineStatsResponse(
                    is_success = False,
                    message = str(f"No user found with that email"),
                    response_codes_json = ResponseCodesJson.NOT_FOUND,
                )
            else:
                splits = []
                for routine in user.routines:
                    splits.append(routine.split_days)

                exercises = []
                for split_day in splits:
                    exercises.append(split_day.exercises)

                get_routine_stats_response = GetRoutineStatsResponse(
                    is_success = True,
                    message = str(f"get routine stats successfully"),
                    response_codes_json = ResponseCodesJson.OK,
                    routines_count = len(user.routines),
                    splits_count = len(splits),
                    exercises_count = len(exercises),
                )
        except Exception as e:
            get_routine_stats_response = GetRoutineStatsResponse(
                is_success = False,
                message = str(f"unexpected error in get-routine-stats-repository {e}"),
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            )

        return get_routine_stats_response

    async def get_routine_by_id(self, get_routine_by_id: GetRoutineByIdRequest) -> GetRoutineByIdResponse:
        try:
            routine = await self._session.query(Routine).filter_by(id = get_routine_by_id.id).first()
            if routine is None:
                get_routine_by_id_response = GetRoutineByIdResponse(
                    is_success = False,
                    message = str(f"routine not found"),
                    response_codes_json = ResponseCodesJson.NOT_FOUND,
                )
            else:
                get_routine_by_id_response = GetRoutineByIdResponse(
                    is_success = True,
                    message = str(f"get routine by id successfully"),
                    response_codes_json = ResponseCodesJson.OK,
                    routine_dto = RoutineMapper.map_routine(routine)
                )
        except Exception as e:
            get_routine_by_id_response = GetRoutineByIdResponse(
                is_success = False,
                message = str(f"unexpected error in get-routine-by-id {e}"),
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            )

        return get_routine_by_id_response