from src.schemas.supplier import SupplierCreate, SupplierUpdate
from fastapi import HTTPException, status
from datetime import datetime
from uuid import uuid4, UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.supplier import Supplier

async def get_all_suppliers(db: AsyncSession):
    result = await db.execute(select(Supplier))
    return result.scalars().all()

async def get_supplier_by_id(supplier_id: UUID, db: AsyncSession):
    result = await db.execute(select(Supplier).filter(Supplier.id == supplier_id))
    supplier = result.scalars().first()
    if supplier:
        return supplier
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found"
    )

async def create_supplier(supplier: SupplierCreate, db: AsyncSession):
    new_supplier = Supplier(
        id=uuid4(),
        name=supplier.name,
        email=supplier.email,
        phone=supplier.phone,
        address=supplier.address,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_supplier)
    await db.commit()
    await db.refresh(new_supplier)
    return new_supplier

async def update_supplier(supplier_id: UUID, supplier: SupplierUpdate, db: AsyncSession):
    result = await db.execute(select(Supplier).filter(Supplier.id == supplier_id))
    supplier_to_update = result.scalars().first()
    
    if supplier_to_update:
        supplier_to_update.name = supplier.name
        supplier_to_update.email = supplier.email
        supplier_to_update.phone = supplier.phone
        supplier_to_update.address = supplier.address
        supplier_to_update.updated_at = datetime.now()
        await db.commit()
        await db.refresh(supplier_to_update)
        return supplier_to_update
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found"
    )

async def delete_supplier(supplier_id: UUID, db: AsyncSession):
    result = await db.execute(select(Supplier).filter(Supplier.id == supplier_id))
    supplier_to_delete = result.scalars().first()
    
    if supplier_to_delete:
        await db.delete(supplier_to_delete)
        await db.commit()
        return {"detail": "Supplier deleted successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found"
    )
