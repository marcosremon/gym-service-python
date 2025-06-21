from typing import Optional, List

from src.application.dto.routine_dto import RoutineDTO
from src.transversal.common.base_response import BaseResponse

class GetRoutineStatsResponse(BaseResponse):
    routines_count: int = 0
    exercises_count: int = 0
    splits_count: int  = 0