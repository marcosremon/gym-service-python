from typing import Optional
from pydantic import BaseModel
from src.application.dto.split_day_dto import SplitDayDTO

class UpdateRoutineRequest(BaseModel):
    routine_id: int
    routine_name: str
    routine_description: str