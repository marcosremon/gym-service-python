from fastapi.params import Depends

from src.application.mappers.user_mapper import UserMapper
from src.core.interfaces.repository.abstract_user_repository import AbstractUserRepository
from src.core.model.entities.user import User
from src.infraestructure.context.application_db_context import ApplicationDbContext as context
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

_context = Depends(context.get_session)

class UserRepository(AbstractUserRepository):

    async def get_users(self) -> GetUsersResponse:
        response: GetUsersResponse
        try:
            users = await _context.query(User).all()
            if users.is_empty:
                response.is_success = False
                response.message = "No users found"
                return response

            users_dto = UserMapper.map_user_list(users)

            response.is_success = True
            response.message = "Successfully fetched users"
            response.users = users_dto
        except Exception as e:
            response.is_success = False
            response.message = "unexpected error in get_users repository"
            response.response_code = 500

        return response