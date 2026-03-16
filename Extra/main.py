from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
import Database.models as models, Database.schema as schema
from Database.database import SessionLocal
from Extra.operations import CRUD  

app = FastAPI()

crud_worker = CRUD(models.Worker, schema.WorkerCreate, schema.WorkerRead, schema.WorkerBase)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create
@app.post("/workers/create", response_model=schema.WorkerRead)
async def create_worker(worker: schema.WorkerCreate, db: Session = Depends(get_db)):
    return crud_worker.create_entity(worker, db)

# Read all
@app.get("/workers", response_model=List[schema.WorkerRead])
async def get_all_workers(db: Session = Depends(get_db)):
    return crud_worker.get_all_entities(db)

# Read one
@app.get("/worker/{worker_id}", response_model=schema.WorkerRead)
async def get_worker(worker_id: int, db: Session = Depends(get_db)):
    return crud_worker.get_entity(worker_id, db)

# Update
@app.put("/worker/{worker_id}", response_model=schema.WorkerRead)
async def update_worker(worker_id: int, worker: schema.WorkerBase, db: Session = Depends(get_db)):
    return crud_worker.update_entity(worker_id, worker, db)

# Delete
@app.delete("/worker/{worker_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    crud_worker.delete_entity(worker_id, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
