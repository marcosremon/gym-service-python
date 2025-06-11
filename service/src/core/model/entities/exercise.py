from dataclasses import dataclass
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from src.core.model.enums.week_day import WeekDay

@dataclass
class Exercise:
    __tablename__ = "exercises"
    
    exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_name = Column(String(100), nullable=True)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)    
    routine_id = Column(Integer, ForeignKey('routines.routine_id'))
    day_name = Column(Enum(WeekDay), ForeignKey('split_days.day_name'))
    
    split_day = relationship(
        "SplitDay", 
        foreign_keys=[routine_id, day_name],
        back_populates="exercises"
    )
    
    routine = relationship("Routine", back_populates="exercises")
    progress_entries = relationship("ExerciseProgress", back_populates="exercise")
