from pydantic import BaseModel
from datetime import date

class StageRead(BaseModel):
    id: int
    name: str
    date: date
    length: float
    country: str
    visitors: int

    class Config:
        from_attributes = True


class StageBase(BaseModel):
    name: str
    country: str
    date: date
    attendance: int
    lap_length: float


class StageCreate(StageBase):
    pass


class StageRead(StageBase):
    id: int

    class Config:
        orm_mode = True