from fastapi import FastAPI, HTTPException, Depends, status, Response, APIRouter, Form, UploadFile, File
from typing import Annotated, List
import Database.schema as schema
import Database.models as models
from Database.database import engine, SessionLocal
from sqlalchemy.orm import Session
import os

router = APIRouter()

models.Base.metadata.create_all(bind=engine)

Upload_Dir = "/Users/bhaveshmandwani/Code/Python/INTERNSHIP/Crud_FastAPI/Uploads"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/worker/create")
async def create_worker(
    name: str = Form(...),
    type: str = Form(...),
    contact: str = Form(...),
    image: UploadFile = File(...),
    db: db_dependency = Session
):
    output_dir = 'Uploads/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = image.filename
    file_path = os.path.join(output_dir, filename)
    with open(file_path, "wb+") as file:
        file.write(image.file.read())

    db_worker = models.Worker(
        name=name,
        type=type,
        contact=contact,
        image=file_path  
    )

    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)

    return {
        "msg": "Worker created successfully",
        "data": {"id": db_worker.id}
    }


@router.get("/worker/{worker_id}")
async def read_worker(worker_id: int, db: db_dependency):
    fetch_worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not fetch_worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")
    return {
        "msg": "Worker fetched successfully",
        "data": fetch_worker
    }


@router.get("/workers")
async def read_workers(db: db_dependency):
    fetch_workers = db.query(models.Worker).all()
    return {
        "msg": "Workers fetched successfully",
        "data": fetch_workers
    }


@router.delete("/worker/{worker_id}")
async def delete_worker(worker_id: int, db: db_dependency):
    worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")
    db.delete(worker)
    db.commit()
    return {
        "msg": "Worker deleted successfully"
    }


@router.put("/worker/{worker_id}")
async def update_worker(worker_id: int, worker_update_data: schema.WorkerCreate, db: db_dependency):
    worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Worker not found")

    for key, value in worker_update_data.dict(exclude_unset=True).items():
        setattr(worker, key, value)

    db.add(worker)
    db.commit()
    db.refresh(worker)
    return {
        "msg": "Worker updated successfully",
        "data": worker
    }
