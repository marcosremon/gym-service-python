from src.core.interfaces.application.abstract_split_day_application import AbstractSplitDayApplication
from src.infraestructure.persistence.split_day_repository import SplitDayRepository
from src.transversal.request_response.split_day.update_split_day.update_split_day_request import UpdateSplitDayRequest
from src.transversal.request_response.split_day.update_split_day.update_split_day_response import UpdateSplitDayResponse

class SplitDayApplication(AbstractSplitDayApplication):
    def __init__(self, repository: SplitDayRepository):
        self._repository = repository

    async def update_split_day(self, update_split_day_request: UpdateSplitDayRequest) -> UpdateSplitDayResponse:
        if update_split_day_request.email is None or update_split_day_request.routine_id is None:
            return UpdateSplitDayResponse(
                is_success = False,
                message = "email or routine id is required",
                response_codes_json = 400
            )

        return await self._repository.update_split_day(update_split_day_request)