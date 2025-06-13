from datetime import datetime
from src.core.model.enums.role import Role
from pydantic import BaseModel

class UserDTO(BaseModel):
    dni: str
    username: str
    email: str
    friend_code: str
    password: str
    role: Role
    inscription_date: datetime