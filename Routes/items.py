from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
import Database.schema as schema
from typing import Annotated, List
import Database.models as models
from Database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from Auth.dependencies import get_current_user, require_roles

router = APIRouter()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/item/create")
async def create_item(user: schema.ItemCreate, db: db_dependency):
    db_item = models.Item(**user.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {
        "msg": "Item created successfully",
        "data": {"id": db_item.id}
    }


@router.get("/item/{item_id}")
async def read_item(item_id: int, db: db_dependency):
    fetch_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not fetch_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "msg": "Item fetched successfully",
        "data": fetch_item
    }


@router.get("/items/")
async def read_items(
    db: db_dependency,
    user=Depends(get_current_user)
):
    fetch_items = db.query(models.Item).all()
    if not fetch_items:
        raise HTTPException(status_code=404, detail="No items found")
    return {
        "msg": "Items fetched successfully",
        "user": user,
        "data": fetch_items
    }


@router.delete("/item/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: db_dependency,
    user=Depends(require_roles(["admin"]))
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return None


@router.put("/item/{item_id}")
async def update_item(item_id: int, user_in: schema.ItemCreate, db: db_dependency):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in user_in.dict().items():
        setattr(item, key, value)

    db.add(item)
    db.commit()
    db.refresh(item)
    return {
        "msg": "Item updated successfully",
        "data": item
    }
