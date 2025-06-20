import string
import random

from src.core.model.enums.role import Role
from src.core.model.enums.week_day import WeekDay


class GenericUtils:
    @staticmethod
    def rol_tostring(role: Role) -> str:
        match role:
            case Role.USER:
                return 'USER'
            case Role.ADMIN:
                return 'ADMIN'
            case _:
                return "unexpected role"

    @staticmethod
    def week_day_tostring(week_day: WeekDay) -> str:
        match (week_day):
            case WeekDay.MONDAY:
                return 'monday'
            case WeekDay.TUESDAY:
                return 'tuesday'
            case WeekDay.WEDNESDAY:
                return 'wednesday'
            case WeekDay.THURSDAY:
                return 'thursday'
            case WeekDay.FRIDAY:
                return 'friday'
            case WeekDay.SATURDAY:
                return 'saturday'
            case WeekDay.SUNDAY:
                return 'sunday'
            case _:
                return "unexpected week day"

    @staticmethod
    def create_friend_code() -> str:
        chars = string.ascii_letters + string.digits
        friend_code = ""
        for _ in range(8):
            index = random.randint(0, len(chars) - 1)
            friend_code += chars[index]

        return friend_code