from fastapi import APIRouter, status, Depends
from uuid import UUID
from src.modules.supplier.service import (
    get_all_suppliers,
    get_supplier_by_id,
    create_supplier,
    update_supplier,
    delete_supplier,
)
from src.schemas.supplier import SupplierCreate, SupplierUpdate, Supplier
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.config import get_db
from typing_extensions import Annotated

suppliers_router = APIRouter()
db_dependency = Annotated[AsyncSession, Depends(get_db)]


@suppliers_router.get(
    "/", response_model=List[Supplier], status_code=status.HTTP_200_OK
)
async def getAll(db: db_dependency):
    return await get_all_suppliers(db)


@suppliers_router.get(
    "/{supplier_id}", response_model=Supplier, status_code=status.HTTP_200_OK
)
async def get(supplier_id: UUID, db: db_dependency):
    return await get_supplier_by_id(supplier_id, db)


@suppliers_router.post(
    "/", response_model=Supplier, status_code=status.HTTP_201_CREATED
)
async def create(supplier: SupplierCreate, db: db_dependency):
    return await create_supplier(supplier, db)


@suppliers_router.put("/", response_model=Supplier, status_code=status.HTTP_200_OK)
async def update(supplier_id: UUID, supplier: SupplierUpdate, db: db_dependency):
    return await update_supplier(supplier_id, supplier, db)


@suppliers_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(supplier_id: UUID, db: db_dependency):
    return await delete_supplier(supplier_id, db)
