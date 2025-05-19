from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from auth import schemas, crud, utils

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut)
async def register_user(user:schemas.UserCreate, db:AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    return await crud.create_user(db, user)

@router.post("/login")
async def login_user(user: schemas.UserLogin, db:AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_username(db, user.username)
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = utils.create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}