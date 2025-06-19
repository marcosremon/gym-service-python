from sqlalchemy import BigInteger, Column, String, LargeBinary, Enum, DateTime
from sqlalchemy.orm import relationship
from src.core.model.enums.role import Role
from src.transversal.utils.base import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    dni = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    friend_code = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    role = Column(Enum(Role), nullable=False)
    inscription_date = Column(DateTime, nullable=False)

    routines = relationship(
        "Routine",
        back_populates = "user",
        cascade = "all, delete-orphan",
        lazy = "selectin"
    )
    friendships_as_user = relationship(
        "UserFriend",
        foreign_keys = "[UserFriend.user_id]",
        back_populates = "user",
        lazy = "selectin"
    )

    friendships_as_friend = relationship(
        "UserFriend",
        foreign_keys = "[UserFriend.friend_id]",
        back_populates = "friend",
        lazy = "selectin"
    )