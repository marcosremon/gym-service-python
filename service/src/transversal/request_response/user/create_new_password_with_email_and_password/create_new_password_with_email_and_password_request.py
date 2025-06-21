from pydantic import BaseModel

class CreateNewPasswordWithEmailAndPasswordRequest(BaseModel):
    email: str
    old_password: str
    new_password: str
    confirm_new_password: str