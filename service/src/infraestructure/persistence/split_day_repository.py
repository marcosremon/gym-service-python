from sqlalchemy import delete

from src.application.mappers.user_mapper import UserMapper
from src.core.interfaces.repository.abstract_split_day_repository import AbstractSplitDayRepository
from src.core.model.entities import User, SplitDay, ExerciseProgress, Exercise
from src.core.model.enums.week_day import WeekDay
from src.transversal.common.response_codes_json import ResponseCodesJson
from src.transversal.request_response.split_day.update_split_day.update_split_day_request import UpdateSplitDayRequest
from src.transversal.request_response.split_day.update_split_day.update_split_day_response import UpdateSplitDayResponse
from src.transversal.utils.generic_utils import GenericUtils

class SplitDayRepository(AbstractSplitDayRepository):
    def __init__(self, session):
        self._session = session

    async def update_split_day(self, update_split_day_request: UpdateSplitDayRequest) -> UpdateSplitDayResponse:
        try:
            user = await self._session.query(User).filter_by(email = update_split_day_request.email).first()
            if user is None:
                update_split_day_response = UpdateSplitDayResponse(
                    is_success = False,
                    message = str(f"User not found"),
                    response_codes_json = ResponseCodesJson.BAD_REQUEST
                )
            else:
                routine = await self._session.query(UpdateSplitDayResponse).filter_by(routine_id = update_split_day_request.routine_id).first()
                if routine is None:
                    update_split_day_response = UpdateSplitDayResponse(
                        is_success = False,
                        message = str(f"Routine not found"),
                        response_codes_json = ResponseCodesJson.NOT_FOUND
                    )
                else:
                    if routine not in user.routines:
                        update_split_day_response = UpdateSplitDayResponse(
                            is_success = False,
                            message = str(f"Routine not found"),
                            response_codes_json = ResponseCodesJson.NOT_FOUND
                        )
                    else:
                        if len(update_split_day_request.add_days) == 0 and len(update_split_day_request.remove_days) == 0:
                            update_split_day_response = UpdateSplitDayResponse(
                                is_success = False,
                                message = str(f"No days left to update"),
                                response_codes_json = ResponseCodesJson.NOT_FOUND
                            )
                        else:
                            if len(update_split_day_request.remove_days) > 0:
                                for delete_day in update_split_day_request.delete_days:
                                    day_name = GenericUtils.change_week_day_language(delete_day)
                                    split = await self._session.query(SplitDay).filter_by(day_name = day_name).first()
                                    if split is not None:
                                        exercise_ids = [exercise.exercise_id for exercise in split.exercises]

                                        await self._session.execute(
                                            delete(ExerciseProgress)
                                            .where(ExerciseProgress.exercise_id.in_(exercise_ids))
                                        )

                                        await self._session.execute(
                                            delete(Exercise)
                                            .where(Exercise.split_day_id == split.split_day_id))

                                        await self._session.delete(split)

                            if len(update_split_day_request.add_days) > 0:
                                for add_day in update_split_day_request.add_days:
                                    week_day = WeekDay(GenericUtils.change_week_day_language(add_day))
                                    split_day = SplitDay(
                                        day_name = week_day,
                                        routine_id = update_split_day_request.routine_id,
                                    )
                                    routine.split_days.append(split_day)

                            await self._session.commit()

                            update_split_day_response = UpdateSplitDayResponse(
                                is_success = True,
                                message = str(f"Updated split day"),
                                response_codes_json = ResponseCodesJson.OK,
                                user_dto = UserMapper.map_user(user)
                            )
        except Exception as e:
            update_split_day_response = UpdateSplitDayResponse(
                is_success = False,
                message = str(f"Failed to update split day {e}"),
                response_codes_json = ResponseCodesJson.INTERNAL_SERVER_ERROR,
            )

        return update_split_day_response