from typing import Optional
from pydantic import BaseModel
from src.application.dto.split_day_dto import SplitDayDTO

class DeleteRoutineRequest(BaseModel):
    email: str
    routine_id: int