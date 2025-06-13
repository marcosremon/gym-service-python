from pydantic import BaseModel

class RoutineDTO(BaseModel):
    routine_name: str
    routine_description: str
    user_id: int