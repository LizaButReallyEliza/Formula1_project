from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Result(Base):
    """
    Represents a race result in the Formula 1 database.

    Attributes:
        id (int): Primary key, unique identifier for the result.
        stage_id (int): Foreign key referencing the `stages` table, 
                        represents the stage/race the result is associated with.
        stable_id (int): Foreign key referencing the `stables` table,
                         represents the stable/team the result is associated with.
        driver_name (str): Name of the driver who participated in the race.
        race_time (float): Total time taken by the driver to complete the race (in minutes).
        laps (int): Number of laps completed by the driver.
        pit_stops (int, optional): Number of pit stops made by the driver during the race.
        position (int, optional): Final position of the driver in the race.

    Relationships:
        stage: A SQLAlchemy relationship to the `Stage` model, representing
               the stage/race associated with this result.
        stable: A SQLAlchemy relationship to the `Stable` model, representing
                the stable/team associated with this result.

    Table:
        Name: `results`
    """
    __tablename__ = 'results'

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    stage_id = Column(Integer, ForeignKey('stages.id'), nullable=False)
    stable_id = Column(Integer, ForeignKey('stables.id'), nullable=False)
    driver_name = Column(String, nullable=False)
    race_time = Column(Float, nullable=False)
    laps = Column(Integer, nullable=False)
    pit_stops = Column(Integer, nullable=True)
    position = Column(Integer, nullable=True)

    # Relationships
    stage = relationship("Stage", back_populates="results")
    stable = relationship("Stable", back_populates="results")