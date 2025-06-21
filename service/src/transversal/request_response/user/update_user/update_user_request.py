from pydantic import BaseModel

class UpdateUserRequest(BaseModel):
    email: str
    new_dni: str
    new_username: str
    new_surname: str
    new_email: str