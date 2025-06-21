from abc import ABC, abstractmethod

from src.transversal.request_response.split_day.update_split_day.update_split_day_request import UpdateSplitDayRequest
from src.transversal.request_response.split_day.update_split_day.update_split_day_response import UpdateSplitDayResponse

class AbstractSplitDayApplication(ABC):
    @abstractmethod
    async def update_split_day(self, update_split_day_request: UpdateSplitDayRequest) -> UpdateSplitDayResponse:
        pass