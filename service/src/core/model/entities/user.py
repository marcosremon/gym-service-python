from dataclasses import dataclass
import datetime
from enum import Enum
from enums.role import Role
from sqlalchemy import BigInteger, Column, LargeBinary, String  
from sqlalchemy.orm import relationship

@dataclass
class User:
    __tablename__ = "users"
    
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    dni = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    friend_code = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    role = Column(Enum(Role), nullable=False)
    inscription_date = Column(datetime)

    routines = relationship("Routine", back_populates="user", cascade="all, delete-orphan")