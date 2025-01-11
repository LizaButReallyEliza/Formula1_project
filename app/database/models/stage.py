from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Stage(Base):
    __tablename__ = 'stages'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    lap_length = Column(Float, nullable=False)
    attendance = Column(Integer, nullable=True)

    results = relationship("Result", back_populates="stage")