from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Stable(Base):
    __tablename__ = 'stables'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    motor = Column(String, nullable=True)
    tire = Column(String, nullable=True)

    results = relationship("Result", back_populates="stable")