from src.schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException, status, UploadFile
from datetime import datetime
from uuid import uuid4, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.product import Product
import secrets
from PIL import Image
from pathlib import Path
import aiofiles
from src.utilities.fileupload import save_file, delete_file

UPLOAD_DIR = Path("../static/images")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)


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


async def create_product(product: ProductCreate, db: AsyncSession, file: UploadFile):
    product_id = str(uuid4())

    # Save the uploaded file and get the filename
    token_name = await save_file(file)

    # Create a new product instance
    new_product = Product(
        id=product_id,
        name=product.name,
        image=token_name,
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

    # Save to the database
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


# UPDATE an existing product
async def update_product(
    product_id: UUID, product: ProductUpdate, db: AsyncSession, file: UploadFile = None
):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product_to_update = result.scalars().first()

    if not product_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    # Update product fields
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

    # Handle file upload if a new file is provided
    if file:
        # Save the new file and delete the old one
        new_filename = await save_file(file)
        if product_to_update.image:
            delete_file(product_to_update.image)
        product_to_update.image = new_filename

    # Commit the changes to the database
    await db.commit()
    await db.refresh(product_to_update)

    return product_to_update


# DELETE a product
async def delete_product(product_id: UUID, db: AsyncSession):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product_to_delete = result.scalars().first()

    if product_to_delete:
        await db.delete(product_to_delete)
        await db.commit()
        return {"detail": "Product deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )
