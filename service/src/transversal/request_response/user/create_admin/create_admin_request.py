from pydantic import BaseModel

class CreateAdminRequest(BaseModel):
    dni: str
    username: str
    surname: str
    email: str
    password: str
    confirm_password: str