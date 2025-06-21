from typing import Optional, List

from src.application.dto.routine_dto import RoutineDTO
from src.transversal.common.base_response import BaseResponse

class GetRoutineByIdResponse(BaseResponse):
    routine_dto: Optional[RoutineDTO] = None