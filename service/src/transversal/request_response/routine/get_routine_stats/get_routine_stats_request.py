from typing import Optional
from pydantic import BaseModel
from src.application.dto.split_day_dto import SplitDayDTO

class GetRoutineStatsRequest(BaseModel):
    email: str