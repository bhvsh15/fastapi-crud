from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
import db.schema as schema
from typing import Annotated
import db.models as models
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()
models.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/inward/create")
async def create_inward(input_item: schema.InwardCreate, db: db_dependency):
    db_inward = models.Inward(**input_item.dict())
    db.add(db_inward)
    
    item = db.query(models.Item).filter(models.Item.id == input_item.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if input_item.quantity>0:
        item.stock += input_item.quantity
    else:
        raise HTTPException(status_code=404, detail= "Negative quanity added")
    
    db.commit()
    return {
        "message": "Inward entry added successfully",
        "id": db_inward.id,
        "updated_stock": item.stock
    }

@router.get("/inwards/")
async def read_inwards(db: db_dependency):
    fetch_inwards = db.query(models.Inward).all()
    if not fetch_inwards:
        raise HTTPException(status_code=404, detail="No inwards found")
    return {
        "msg": "Inwards fetched successfully",
        "data": fetch_inwards
    }


@router.get("/inward/{inward_id}")
async def read_inward(inward_id: int, db: db_dependency):
    fetch_inward = db.query(models.Inward).filter(models.Inward.id == inward_id).first()
    if not fetch_inward:
        raise HTTPException(status_code=404, detail="Inward not found")
    return {
        "msg": "Inward fetched successfully",
        "data": fetch_inward
    }


@router.put("/inward/{inward_id}")
async def update_inward(inward_id: int, user_in: schema.InwardCreate, db: db_dependency):
    inward = db.query(models.Inward).filter(models.Inward.id == inward_id).first()
    if not inward:
        raise HTTPException(status_code=404, detail="Inward not found")
    
    ob = db.query(models.OutwardBarcode).filter(models.OutwardBarcode.barcode == inward.barcode).first()  # ← add .first()
    if ob:
        raise HTTPException(status_code=400, detail="Inward cannot be updated because outward barcode exists")  # ← raise instead of return

    for key, value in user_in.dict().items():
        setattr(inward, key, value)

    db.add(inward)
    db.commit()
    db.refresh(inward)
    return {
        "msg": "Inward updated successfully",
        "data": inward
    }


@router.delete("/inward/{inward_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inward(inward_id: int, db: db_dependency):
    inward = db.query(models.Inward).filter(models.Inward.id == inward_id).first()
    if not inward:
        raise HTTPException(status_code=404, detail="Inward not found")
    
    ob = db.query(models.OutwardBarcode).filter(models.OutwardBarcode.barcode == inward.barcode).first()
    if ob:
        raise HTTPException(status_code=400, detail="Inward cannot be deleted because outward barcode exists")
    
    db.delete(inward)
    db.commit()
    return None