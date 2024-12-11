from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from datetime import datetime


class Category(BaseModel):
    id: UUID
    name: str
    status: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    status: int


class CategoryUpdate(BaseModel):
    name: Optional[str]
    status: Optional[int]

    class Config:
        from_attributes = True

class PaginatedCategory(BaseModel):
    categories: list[Category]
    total: int
