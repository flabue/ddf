from pydantic import BaseModel

class DataBase(BaseModel):
    key: str
    value: float

class DataCreate(DataBase):
    pass

class Data(DataBase):
    id: int

    class Config:
        orm_mode = True