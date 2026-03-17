from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
import db.schema as schema
from typing import Annotated
import db.models as models
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
@router.post("/outwardslip/create")
async def create_outwardslip(outwardslip: schema.OutwardSlipCreate, db: db_dependency):
    db_outwardslip = models.OutwardSlip(**outwardslip.dict())
    db.add(db_outwardslip)

    item = db.query(models.Item).filter(models.Item.id == db_outwardslip.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_outwardslip.quantity >0:
        item.stock -= db_outwardslip.quantity
    else:
        raise HTTPException(status_code=404, detail="Negative quantity")
    db.commit()
    db.refresh(db_outwardslip)
    return {
        "msg": "OutwardSlip created successfully",
        "data": {"id": db_outwardslip.id}
    }

@router.get("/outwardslip/{outwardslip_id}")
async def read_outwardslip(outwardslip_id: int, db: db_dependency):
    fetch_outwardslip = db.query(models.OutwardSlip).filter(models.OutwardSlip.id == outwardslip_id).first()
    if not fetch_outwardslip:
        raise HTTPException(status_code=404, detail="OutwardSlip not found")
    return {
        "msg": "OutwardSlip fetched successfully",
        "data": fetch_outwardslip
    }

@router.get("/outwardslips/")
async def read_outwardslips(db: db_dependency):
    fetch_outwardslips = db.query(models.OutwardSlip).all()
    if not fetch_outwardslips:
        raise HTTPException(status_code=404, detail="No outwardslips found")
    return {
        "msg": "All OutwardSlips fetched successfully",
        "data": fetch_outwardslips
    }

@router.delete("/outwardslip/{outwardslip_id}")
async def delete_outwardslip(outwardslip_id: int, db: db_dependency):
    outwardslip = db.query(models.OutwardSlip).filter(models.OutwardSlip.id == outwardslip_id).first()
    if not outwardslip:
        raise HTTPException(status_code=404, detail="OutwardSlip not found")
    db.delete(outwardslip)
    db.commit()
    return {
        "msg": "OutwardSlip deleted successfully"
    }

@router.put("/outwardslip/{outwardslip_id}")
async def update_outwardslip(outwardslip_id: int, user_in: schema.OutwardSlipCreate, db: db_dependency):
    outwardslip = db.query(models.OutwardSlip).filter(models.OutwardSlip.id == outwardslip_id).first()
    if not outwardslip:
        raise HTTPException(status_code=404, detail="OutwardSlip not found")

    for key, value in user_in.dict().items():
        setattr(outwardslip, key, value)

    db.add(outwardslip)
    db.commit()
    db.refresh(outwardslip)
    return {
        "msg": "OutwardSlip updated successfully",
        "data": outwardslip
    }
