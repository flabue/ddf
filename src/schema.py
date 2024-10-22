from pydantic import BaseModel

class OrderBase(BaseModel):
    customer_name: str
    product_name: str
    quantity: int
    price: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True