from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from src.transversal.common.base import Base

class Routine(Base):
    __tablename__ = "routines"

    routine_id = Column(Integer, primary_key=True, autoincrement=True)
    routine_name = Column(String, unique=True, nullable=True)
    routine_description = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="routines")

    split_days = relationship("SplitDay", back_populates="routine", cascade="all, delete-orphan")
    progress_entries = relationship("ExerciseProgress", back_populates="routine")

    exercises = relationship("Exercise", back_populates="routine", cascade="all, delete-orphan")