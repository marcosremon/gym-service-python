from pydantic import BaseModel
from src.core.model.enums.week_day import WeekDay

class ExerciseDTO(BaseModel):
    exercise_name: str
    routine_id: int
    day_name: WeekDay