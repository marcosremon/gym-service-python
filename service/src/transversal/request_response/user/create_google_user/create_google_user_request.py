from pydantic import BaseModel

class CreateGoogleUserRequest(BaseModel):
    dni: str = ""
    username: str = ""
    surname: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""