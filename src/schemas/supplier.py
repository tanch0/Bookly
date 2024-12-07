from pydantic import BaseModel,EmailStr
from uuid import UUID
from datetime import datetime


class Supplier(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: str
    address: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SupplierCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

    class Config:
        from_attributes = True

class SupplierUpdate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str

    class Config:
        from_attributes = True