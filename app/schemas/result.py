from pydantic import BaseModel


class ResultBase(BaseModel):
    driver_name: str
    race_time: float
    laps: int
    position: int
    pit_stops: int
    stable_id: int
    stage_id: int


class ResultCreate(ResultBase):
    pass


class ResultRead(ResultBase):
    id: int

    class Config:
        from_attributes = True