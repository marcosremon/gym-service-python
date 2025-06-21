from typing import Optional
from pydantic import BaseModel
from src.application.dto.split_day_dto import SplitDayDTO

class GetAllUserRoutinesRequest(BaseModel):
    email: str