from pydantic import BaseModel

class SplitDayDTO(BaseModel):
    day_name: str
    routine_id: int
    day_exercises_description: str