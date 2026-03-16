from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
import Database.schema as schema
from typing import Annotated
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

@router.post("/outwardbarcode/create")
async def create_outwardbarcode(outwardbarcode: schema.OutwardBarcodeCreate, db: db_dependency):
    db_outwardbarcode = models.OutwardBarcode(**outwardbarcode.dict())
    db.add(db_outwardbarcode)
    db.commit()
    db.refresh(db_outwardbarcode)
    return {
        "msg": "OutwardBarcode created successfully",
        "data": {"id": db_outwardbarcode.id}
    }

@router.get("/outwardbarcode/{outwardbarcode_id}")
async def read_outwardbarcode(outwardbarcode_id: int, db: db_dependency):
    fetch_outwardbarcode = db.query(models.OutwardBarcode).filter(models.OutwardBarcode.id == outwardbarcode_id).first()
    if not fetch_outwardbarcode:
        raise HTTPException(status_code=404, detail="OutwardBarcode not found")
    return {
        "msg": "OutwardBarcode fetched successfully",
        "data": fetch_outwardbarcode
    }

@router.get("/outwardbarcodes/")
async def read_outwardbarcodes(db: db_dependency):
    fetch_outwardbarcodes = db.query(models.OutwardBarcode).all()
    if not fetch_outwardbarcodes:
        raise HTTPException(status_code=404, detail="No outwardbarcodes found")
    return {
        "msg": "All OutwardBarcodes fetched successfully",
        "data": fetch_outwardbarcodes
    }

