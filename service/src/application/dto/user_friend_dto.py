from pydantic import BaseModel

class UserFriendDTO(BaseModel):
    user_id: int
    friend_id: int