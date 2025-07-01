from pydantic import BaseModel

class LoginWebRequest(BaseModel):
    email: str
    password: str