from pydantic import BaseModel

class GetAllUserFriendsRequest(BaseModel):
    email: str