from pydantic import BaseModel

class CreateNewPasswordRequest(BaseModel):
    email: str