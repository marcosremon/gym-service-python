from typing import List

from src.application.dto.routine_dto import RoutineDTO
from src.core.model.entities import Routine

class RoutineMapper:
    @staticmethod
    def map_routine(routine: Routine) -> RoutineDTO:
        return RoutineDTO(
            routine_name = routine.routine_name,
            routine_description = routine.routine_description,
            user_id = routine.user_id,
        )

    @staticmethod
    def map_routine_list(routines: List[Routine]) -> List[RoutineDTO]:
        return list(
            map(lambda routine: RoutineDTO(
                routine_name = routine.routine_name,
                routine_description = routine.routine_description,
                user_id = routine.user_id,
            ), routines)
        )