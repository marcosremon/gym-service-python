from pydantic import BaseModel

class AddNewUserFriendRequest(BaseModel):
    email: str
    friend_code: str