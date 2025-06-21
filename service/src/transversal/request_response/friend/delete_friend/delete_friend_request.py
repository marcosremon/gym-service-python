from pydantic import BaseModel

class DeleteFriendRequest(BaseModel):
    email: str
    friend_email: str