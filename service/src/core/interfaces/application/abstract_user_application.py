from abc import ABC, abstractmethod
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

class AbstractUserApplication(ABC):
    @abstractmethod
    async def get_users(self) -> GetUsersResponse:
        pass