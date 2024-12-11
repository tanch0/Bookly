from fastapi import APIRouter, status, Depends
from uuid import UUID
from src.modules.categories.service import (
    get_all_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category
)
from src.schemas.category import Category, CategoryUpdate, CategoryCreate, PaginatedCategory
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.config import get_db
from typing_extensions import Annotated

categories_router = APIRouter()
db_dependency = Annotated[AsyncSession, Depends(get_db)]

@categories_router.get("/", response_model=PaginatedCategory, status_code=status.HTTP_200_OK)
async def get_all(db: db_dependency, skip: int = 0, limit: int = 10):
    return await get_all_categories(db, skip, limit)

@categories_router.get("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def get(category_id: UUID, db: db_dependency):
    return await get_category_by_id(category_id, db)

@categories_router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create(category: CategoryCreate, db: db_dependency):
    return await create_category(category, db)

@categories_router.put("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def update(category_id: UUID, category: CategoryUpdate, db: db_dependency):
    return await update_category(category_id, category, db)

@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(category_id: UUID, db: db_dependency):
    await delete_category(category_id, db)
    return None 
