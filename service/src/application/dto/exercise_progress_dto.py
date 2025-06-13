from pydantic import BaseModel
from datetime import datetime
from src.core.model.enums.week_day import WeekDay

class ExerciseProgressDTO(BaseModel):
    exercise_id: int
    routine_id: int
    day_name: WeekDay
    sets: int
    reps: int
    weight: float
    performed_at: datetime