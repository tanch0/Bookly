from src.schemas.category import CategoryUpdate, CategoryCreate
from fastapi import HTTPException, status
from datetime import datetime
from uuid import uuid4, UUID
from src.models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


# Asynchronous function to fetch all categories
async def get_all_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()


# Asynchronous function to fetch a category by ID
async def get_category_by_id(category_id: UUID, db: AsyncSession):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


# Asynchronous function to create a category
async def create_category(category: CategoryCreate, db: AsyncSession):
    category_id = str(uuid4())
    current_time = datetime.now()

    new_category = Category(
        id=category_id,
        name=category.name,
        created_at=current_time,
        updated_at=current_time,
    )

    db.add(new_category)
    await db.commit()  
    await db.refresh(new_category)  

    return new_category


# Asynchronous function to update a category
async def update_category(
    category_id: UUID, category_data: CategoryUpdate, db: AsyncSession
):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category = result.scalars().first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    if category_data.name:
        category.name = category_data.name

    category.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    await db.commit()
    await db.refresh(category)

    return category


# Asynchronous function to delete a category
async def delete_category(category_id: UUID, db: AsyncSession):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category = result.scalars().first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    await db.delete(category)  # Delete the category
    await db.commit()  # Commit the transaction

    return {"detail": "Category deleted successfully"}
