from sqlalchemy.orm import Session
from app import models, schemas

def get_data(db: Session, data_id: int):
    return db.query(models.Data).filter(models.Data.id == data_id).first()

def create_data(db: Session, data: schemas.DataCreate):
    db_data = models.Data(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data