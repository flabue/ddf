from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True)
    value = Column(Float)