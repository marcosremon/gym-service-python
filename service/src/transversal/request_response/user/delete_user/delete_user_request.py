from pydantic import BaseModel

class DeleteUserRequest(BaseModel):
    email: str