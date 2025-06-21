from typing import List
from pydantic import BaseModel

class UpdateSplitDayRequest(BaseModel):
    routine_id: int
    email: str
    add_days: List[str]
    delete_days: List[str]