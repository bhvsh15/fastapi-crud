from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db import models
from db.schema import UserCreate

from auth.password_handler import verify_password,hash_password
from auth.jwt_handler import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    print("Entered password:", form_data.password)

    if user:
        print("DB hash:", user.hashed_password)
        from auth.password_handler import verify_password
        print("Verify result:", verify_password(form_data.password, user.hashed_password))

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(
        data={
            "sub": user.username,
            "role": user.role
        }
    )
   

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    # check if username already exists
    existing_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # hash password
    hashed_password = hash_password(user.password)

    # create user
    new_user = models.User(
        username=user.username.strip(),
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "username": new_user.username
    }
