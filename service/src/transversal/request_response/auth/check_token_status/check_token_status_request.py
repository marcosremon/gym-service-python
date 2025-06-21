from pydantic import BaseModel

class CheckTokenStatusRequest(BaseModel):
    token: str