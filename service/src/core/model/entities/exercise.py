from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from src.transversal.utils.base import Base

class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_name = Column(String(100), nullable=True)
    routine_id = Column(Integer, ForeignKey('routines.routine_id'))

    split_day_id = Column(Integer, ForeignKey('split_days.split_day_id'))

    split_day = relationship(
        "SplitDay",
        back_populates="exercises"
    )

    routine = relationship("Routine", back_populates="exercises")

    progress_entries = relationship("ExerciseProgress", back_populates="exercise")