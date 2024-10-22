from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, crud, producer
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/data/", response_model=schemas.Data)
def create_data(data: schemas.DataCreate, db: Session = Depends(get_db)):
    producer.send_to_kafka(data)
    return crud.create_data(db=db, data=data)

@app.get("/data/{data_id}", response_model=schemas.Data)
def read_data(data_id: int, db: Session = Depends(get_db)):
    db_data = crud.get_data(db, data_id=data_id)
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return db_data