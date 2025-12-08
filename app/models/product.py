from pydantic import BaseModel

class Product(BaseModel):
    """товар"""
    id: int
    name: str
    price: float
    seller_id: int
    description: str