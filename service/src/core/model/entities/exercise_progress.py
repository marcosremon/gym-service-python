from dataclasses import dataclass
from sqlalchemy import Column, Integer, Float, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

from src.core.model.enums.week_day import WeekDay

@dataclass
class ExerciseProgress:
    __tablename__ = "exercise_progress"
    
    progress_id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_id = Column(Integer, ForeignKey('exercises.exercise_id'), nullable=False)
    routine_id = Column(Integer, ForeignKey('routines.routine_id'), nullable=False)
    day_name = Column(WeekDay, nullable=False)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    performed_at = Column(datetime, nullable=False)
    
    exercise = relationship("Exercise", back_populates="progress_entries")
    routine = relationship("Routine", back_populates="progress_entries")