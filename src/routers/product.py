from fastapi import APIRouter, status, Depends, HTTPException, File, UploadFile, Form
from uuid import UUID
from typing import List, Optional
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.products.service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
)
from src.schemas.product import ProductCreate, ProductUpdate, Product
from src.database.config import get_db

products_router = APIRouter()
db_dependency = Annotated[AsyncSession, Depends(get_db)]


# GET all products
@products_router.get("/", response_model=List[Product])
async def get_all(db: db_dependency):
    products = await get_all_products(db)
    return products


# GET product by ID
@products_router.get(
    "/{product_id}", response_model=ProductCreate, status_code=status.HTTP_200_OK
)
async def get(product_id: UUID, db: db_dependency):
    product = await get_product_by_id(product_id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# POST create a new product
@products_router.post(
    "/", response_model=ProductCreate, status_code=status.HTTP_201_CREATED
)
async def create(
    db: db_dependency,
    name: str = Form(...),
    price: float = Form(...),
    category_id: UUID = Form(...),
    supplier_id: UUID = Form(...),
    quantity: int = Form(...),
    reorder_level: int = Form(...),
    discount: float = Form(...),
    rating: float = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(...),
):
    product_data = ProductCreate(
        name=name,
        price=price,
        category_id=category_id,
        supplier_id=supplier_id,
        quantity=quantity,
        reorder_level=reorder_level,
        discount=discount,
        rating=rating,
        description=description,
        image=None,
    )

    return await create_product(product_data, db, files)


# PUT update an existing product
@products_router.put(
    "/{product_id}", response_model=Product, status_code=status.HTTP_200_OK
)
async def update(
    product_id: UUID,
    db: db_dependency,
    name: str = Form(...),
    price: float = Form(...),
    category_id: UUID = Form(...),
    supplier_id: UUID = Form(...),
    quantity: int = Form(...),
    reorder_level: int = Form(...),
    discount: float = Form(...),
    rating: float = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(None),
):
    product_data = ProductUpdate(
        name=name,
        price=price,
        category_id=category_id,
        supplier_id=supplier_id,
        quantity=quantity,
        reorder_level=reorder_level,
        discount=discount,
        rating=rating,
        description=description,
        image=None,
    )

    return await update_product(product_id, product_data, db, files)


# DELETE a product
@products_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(product_id: UUID, db: db_dependency):
    success = await delete_product(product_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
