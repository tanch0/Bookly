from fastapi import FastAPI
from src.database.config import SessionLocal, engine, Base
from src.routers.category import categories_router
from src.routers.supplier import suppliers_router
from src.routers.product import products_router
from src.models import *

version = "0.1.0"
app = FastAPI(version=version)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# async def delete_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

@app.on_event("startup")
async def on_startup():
    await create_db()

# @app.on_event("shutdown")
# async def on_shutdown():
#     await delete_db()

app.include_router(categories_router, prefix=f"/api/{version}/categories", tags=["Categories"])
app.include_router(products_router, prefix=f"/api/{version}/products", tags=["Products"])
app.include_router(suppliers_router, prefix=f"/api/{version}/suppliers", tags=["Suppliers"])
