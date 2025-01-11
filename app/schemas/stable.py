from pydantic import BaseModel


class StableBase(BaseModel):
    name: str
    country: str
    motor: str | None = None
    tire: str | None = None


class StableCreate(StableBase):
    pass


class StableRead(StableBase):
    id: int

    class Config:
        orm_mode = True