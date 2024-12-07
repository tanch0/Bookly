from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from datetime import datetime


class Category(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: Optional[str]

    class Config:
        from_attributes = True
