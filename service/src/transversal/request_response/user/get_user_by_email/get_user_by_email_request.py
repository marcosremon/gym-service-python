from pydantic import BaseModel

class GetUserByEmailRequest(BaseModel):
    email: str