from typing import Optional
from pydantic import BaseModel
from src.application.dto.split_day_dto import SplitDayDTO

class CreateRoutineRequest(BaseModel):
    email: str
    routine_name: str
    routine_description: str
    splits_days: Optional[SplitDayDTO] = None