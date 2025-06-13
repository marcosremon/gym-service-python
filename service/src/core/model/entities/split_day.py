from sqlalchemy import Column, ForeignKey, Integer, String
from src.core.model.enums.week_day import WeekDay
from sqlalchemy.orm import relationship

class SplitDay:
    __tablename__ = "split_days"

    split_day_id = Column(Integer, primary_key=True, autoincrement=True)
    day_name = Column(WeekDay, nullable=True)
    routine_id = Column(Integer, ForeignKey('routines.routine_id'))
    day_exercises_description = Column(String, default="")
    
    routine = relationship("Routine", back_populates="split_days")
    
    exercises = relationship(
        "Exercise", 
        back_populates="split_day", 
        cascade="all, delete-orphan", 
        lazy="dynamic" 
    )