from dataclasses import dataclass
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String

@dataclass
class Routine:
    __tablename__ = "routines"
    
    routine_id = Column(Integer, primary_key=True, autoincrement=True)
    routine_name = Column(String, unique=True, nullable=True)
    routine_description = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="routines")
    
    split_days = relationship("SplitDay", back_populates="routine", cascade="all, delete-orphan")
    progress_entries = relationship("ExerciseProgress", back_populates="routine")
