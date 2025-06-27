from typing import List
from src.core.model.entities.user import User
from src.application.dto.user_dto import UserDTO
from src.transversal.utils.generic_utils import GenericUtils


class UserMapper:
    @staticmethod
    def map_user_list(users: List[User]) -> List[UserDTO]:
        return list(
            map(lambda user: UserDTO(
                dni = user.dni,
                username = user.username,
                surname = user.surname,
                email = user.email,
                friend_code = user.friend_code,
                password = "*********",
                role = user.role,
                inscription_date = str(user.inscription_date),
            ), users)
        )

    @staticmethod
    def map_user(user: User) -> UserDTO:
        return UserDTO(
            dni = user.dni,
            username = user.username,
            surname = user.surname,
            email = user.email,
            friend_code = user.friend_code,
            password="*********",
            role = user.role,
            inscription_date = str(user.inscription_date),
        )