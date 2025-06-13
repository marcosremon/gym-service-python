from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from src.core.model.enums.role import Role


@dataclass
class User:
    __tablename__ = "users"
    
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    dni = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    friend_code = Column(String, unique=True, nullable=False)
    password = Column(bytearray, nullable=False)
    role = Column(Role, nullable=False)
    inscription_date = Column(datetime)

    routines = relationship("Routine", back_populates="user", cascade="all, delete-orphan")