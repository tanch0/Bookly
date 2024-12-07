from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class Product(BaseModel):
    id: UUID
    name: str
    price: float
    image: Optional[str]
    category_id: UUID
    supplier_id: UUID
    quantity: int
    reorder_level: int
    discount: float
    rating: float
    description: str
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    price: float
    image: Optional[str]
    category_id: UUID
    supplier_id: UUID
    quantity: int
    reorder_level: int
    discount: float
    rating: float
    description: str
    
    class config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str
    price: float
    image: Optional[str]
    category_id: UUID
    supplier_id: UUID
    quantity: int
    reorder_level: int
    discount: float
    rating: float
    description: str

    class config:
        from_attributes = True