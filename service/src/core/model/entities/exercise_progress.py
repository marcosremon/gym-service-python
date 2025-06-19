from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from src.core.model.enums.week_day import WeekDay
from src.transversal.common.base import Base

class ExerciseProgress(Base):
    __tablename__ = "exercise_progress"
    
    progress_id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_id = Column(Integer, ForeignKey('exercises.exercise_id'), nullable=False)
    routine_id = Column(Integer, ForeignKey('routines.routine_id'), nullable=False)
    day_name = Column(Enum(WeekDay), nullable=False)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    performed_at = Column(DateTime, nullable=False)
    
    exercise = relationship("Exercise", back_populates="progress_entries")
    routine = relationship("Routine", back_populates="progress_entries")