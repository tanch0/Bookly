from src.schemas.category import CategoryUpdate, CategoryCreate
from fastapi import HTTPException, status
from datetime import datetime
from uuid import uuid4, UUID
from src.models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.Enum.Status import StatusEnum
from src.schemas.category import PaginatedCategory
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError


# Asynchronous function to fetch all categories
async def get_all_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Category)
        .filter(Category.status == StatusEnum.ACTIVE)
        .offset(skip)
        .limit(limit)
    )
    categories = result.scalars().all()

    count_result = await db.execute(
        select(func.count())
        .select_from(Category)
        .filter(Category.status == StatusEnum.ACTIVE)
    )
    total = count_result.scalar_one()

    return PaginatedCategory(categories=categories, total=total)


# Asynchronous function to fetch a category by ID
async def get_category_by_id(category_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Category).filter(
            Category.id == category_id and Category.status == StatusEnum.ACTIVE.value
        )
    )
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


# Asynchronous function to create a category
async def create_category(category: CategoryCreate, db: AsyncSession):
    category_id = uuid4()
    current_time = datetime.utcnow()

    try:
        status = StatusEnum(category.status)
    except ValueError:
        raise ValueError(f"Invalid status value: {category.status}")

    new_category = Category(
        id=category_id,
        name=category.name,
        status=status,
        created_at=current_time,
        updated_at=current_time,
    )

    db.add(new_category)
    try:
        await db.commit()
        await db.refresh(new_category)
    except IntegrityError as e:
        await db.rollback()
        raise e

    return new_category


# Asynchronous function to update a category
async def update_category(
    category_id: UUID, category_data: CategoryUpdate, db: AsyncSession
):
    result = await db.execute(
        select(Category).filter(
            Category.id == category_id, Category.status == StatusEnum.ACTIVE
        )
    )
    category = result.scalars().first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    if category_data.status is not None:
        try:
            category.status = StatusEnum(category_data.status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status value: {category_data.status}",
            )

    if category_data.name:
        category.name = category_data.name

    category.updated_at = datetime.utcnow()

    # Commit the changes
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
