import pandas as pd
import sqlalchemy
import os
import requests

# Obter variáveis de ambiente
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from app import models, schema, crud
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

@app.post("/orders/", response_model=schema.Order)
def create_order(order: schema.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)

@app.get("/orders/{order_id}", response_model=schema.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order