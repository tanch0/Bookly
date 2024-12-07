from src.schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException, status, UploadFile
from datetime import datetime
from uuid import uuid4, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.product import Product
from typing import List
from src.utilities.fileupload import save_file, delete_file


# GET all products
async def get_all_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


# GET product by ID
async def get_product_by_id(product_id: UUID, db: AsyncSession):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )

# CREATE a new product
async def create_product(
    product: ProductCreate, db: AsyncSession, files: List[UploadFile] = None
):
    product_id = str(uuid4())

    image_filenames = []
    for file in files:
        filename = await save_file(file)
        image_filenames.append(filename)

    image_str = ",".join(image_filenames)
    new_product = Product(
        id=product_id,
        name=product.name,
        image=image_str,
        price=product.price,
        category_id=product.category_id,
        supplier_id=product.supplier_id,
        quantity=product.quantity,
        reorder_level=product.reorder_level,
        discount=product.discount,
        rating=product.rating,
        description=product.description,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


# UPDATE an existing product
async def update_product(
    product_id: UUID,
    product: ProductUpdate,
    db: AsyncSession,
    files: List[UploadFile] = None,
):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product_to_update = result.scalars().first()

    if not product_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    product_to_update.name = product.name
    product_to_update.price = product.price
    product_to_update.category_id = product.category_id
    product_to_update.supplier_id = product.supplier_id
    product_to_update.quantity = product.quantity
    product_to_update.reorder_level = product.reorder_level
    product_to_update.discount = product.discount
    product_to_update.rating = product.rating
    product_to_update.description = product.description
    product_to_update.updated_at = datetime.now()

    if files:
        new_filenames = []
        for file in files:
            new_filename = await save_file(file)
            new_filenames.append(new_filename)

        if product_to_update.image:
            old_images = product_to_update.image.split(",")
            for old_image in old_images:
                delete_file(old_image)

        product_to_update.image = ",".join(new_filenames)

    await db.commit()
    await db.refresh(product_to_update)

    return product_to_update


# DELETE a product
async def delete_product(product_id: UUID, db: AsyncSession):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product_to_delete = result.scalars().first()

    if not product_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    if product_to_delete.image:
        images = product_to_delete.image.split(",")
        for image in images:
            delete_file(image) 

    await db.delete(product_to_delete)
    await db.commit()

    return {"detail": "Product and associated images deleted successfully"}
