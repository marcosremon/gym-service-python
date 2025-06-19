from dataclasses import dataclass

from src.core.model.enums.role import Role

@dataclass
class CreateGenericUserRequest:
    dni: str
    username: str
    surname: str
    email: str
    password: str
    confirm_password: str
    role: Role