from fastapi import APIRouter, HTTPException, Depends, status
import db.schema as schema
import db.models as models
from typing import Annotated, List
from db.database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/outward/create")
async def create_outward(user: schema.OutwardCreate, db: db_dependency):
    db_outward = models.Outward(**user.dict())
    db.add(db_outward)
    a = db.query(models.OutwardSlip).filter(models.OutwardSlip.id == db_outward.slip_id).first()
    if a is None:
        raise HTTPException(status_code=404, detail="OutwardSlip not found")
    a.status = "Completed"  
    item = db.query(models.Item).filter(models.Item.id == a.item_id).first()
    item.stock-=a.quantity
    
    db.commit()
    db.refresh(db_outward)
    return {
        "msg": "Outward created successfully",
        "data": {"id": db_outward.id}
    }


@router.get("/outward/{outward_id}")
async def read_outward(outward_id: int, db: db_dependency):
    fetch_outward = db.query(models.Outward).filter(models.Outward.id == outward_id).first()
    if not fetch_outward:
        raise HTTPException(status_code=404, detail="Outward not found")
    return {
        "msg": "Outward fetched successfully",
        "data": fetch_outward
    }

@router.get("/outwards/")
async def read_outwards(db: db_dependency):
    fetch_outwards = db.query(models.Outward).all()
    if not fetch_outwards:
        raise HTTPException(status_code=404, detail="No outwards found")
    return {
        "msg": "All Outwards fetched successfully",
        "data": fetch_outwards
    }

