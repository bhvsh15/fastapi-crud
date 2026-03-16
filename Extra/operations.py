@router.delete("/outward/{outward_id}")
async def delete_outward(outward_id: int, db: db_dependency):
    outward = db.query(models.Outward).filter(models.Outward.id == outward_id).first()
    if not outward:
        raise HTTPException(status_code=404, detail="Outward not found")
    db.delete(outward)
    db.commit()
    return {
        "msg": "Outward deleted successfully"
    }

@router.put("/outward/{outward_id}")
async def update_outward(outward_id: int, user_in: schema.OutwardCreate, db: db_dependency):
    outward = db.query(models.Outward).filter(models.Outward.id == outward_id).first()
    if not outward:
        raise HTTPException(status_code=404, detail="Outward not found")

    for key, value in user_in.dict().items():
        setattr(outward, key, value)

    db.add(outward)
    db.commit()
    db.refresh(outward)
    return {
        "msg": "Outward updated successfully",
        "data": outward
    }
