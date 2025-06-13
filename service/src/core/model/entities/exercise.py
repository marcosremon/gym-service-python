from dataclasses import dataclass
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from src.core.model.enums.week_day import WeekDay

@dataclass
class Exercise:
    __tablename__ = "exercises"
    
    exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_name = Column(String(100), nullable=True)
    routine_id = Column(Integer, ForeignKey('routines.routine_id'))
    day_name = Column(WeekDay, ForeignKey('split_days.day_name'))
    
    split_day = relationship(
        "SplitDay", 
        foreign_keys=[routine_id, day_name],
        back_populates="exercises"
    )
    
    routine = relationship("Routine", back_populates="exercises")
    progress_entries = relationship("ExerciseProgress", back_populates="exercise")
