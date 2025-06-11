from abc import ABC, abstractmethod

class UserInterface(ABC):
    @abstractmethod
    async def get_users(self):
        pass