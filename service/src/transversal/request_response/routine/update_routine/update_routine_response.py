from typing import Optional

from src.application.dto.routine_dto import RoutineDTO
from src.transversal.common.base_response import BaseResponse

class UpdateRoutineResponse(BaseResponse):
    routine_dto: Optional[RoutineDTO] = None