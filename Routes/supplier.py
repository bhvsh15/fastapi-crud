from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
import Database.schema as schema
from typing import Annotated, List
import Database.models as models
from Database.database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/supplier/create")
async def create_supplier(supplier: schema.SupplierCreate, db: db_dependency):
    db_supplier = models.Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return {
        "msg": "Supplier created successfully",
        "data": {"id": db_supplier.id}
    }


@router.get("/supplier/{supplier_id}")
async def read_supplier(supplier_id: int, db: db_dependency):
    fetch_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not fetch_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {
        "msg": "Supplier fetched successfully",
        "data": fetch_supplier
    }


@router.get("/suppliers/")
async def read_suppliers(db: db_dependency):
    fetch_suppliers = db.query(models.Supplier).all()
    if not fetch_suppliers:
        raise HTTPException(status_code=404, detail="No suppliers found")
    return {
        "msg": "Suppliers fetched successfully",
        "data": fetch_suppliers
    }


@router.delete("/supplier/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_supplier(supplier_id: int, db: db_dependency):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(supplier)
    db.commit()
    return {
        "Supplier Delete"
        }


@router.put("/supplier/{supplier_id}")
async def update_supplier(supplier_id: int, user_in: schema.SupplierCreate, db: db_dependency):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    for key, value in user_in.dict().items():
        setattr(supplier, key, value)

    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return {
        "msg": "Supplier updated successfully",
        "data": supplier
    }
