from fastapi.params import Depends
from sqlalchemy.testing.suite.test_reflection import users

from src.application.mappers.user_mapper import UserMapper
from src.core.interfaces.repository.abstract_user_repository import AbstractUserRepository
from src.core.model.entities.user import User
from src.infraestructure.context.application_db_context import ApplicationDbContext as context
from src.transversal.request_response.user.get_users.get_users_response import GetUsersResponse

class UserRepository(AbstractUserRepository):
    def __init__(self, session):
        self._session = session

    async def get_users(self) -> GetUsersResponse:
        try:
            users = self._session.query(User).all()
            if not users:
                return GetUsersResponse(
                    is_success = False,
                    message = "No users found",
                    response_codes_json= 404,
                    users = []
                )

            users_dto = UserMapper.map_user_list(users)
            return GetUsersResponse(
                is_success = True,
                message = "users found successfully",
                response_codes_json= 200,
                users = users_dto
            )
        except Exception as e:
            return GetUsersResponse(
                is_success = False,
                message = str(f"unexpected error in get-users repository: {e}"),
                response_codes_json= 500,
                users = []
            )