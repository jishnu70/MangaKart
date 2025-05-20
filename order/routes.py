from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from order import schemas, crud
from auth.routes import get_current_user
from auth.models import User

router = APIRouter(prefix="/order", tags=["order"])

@router.get("/", response_model=list[schemas.OrderBase])
async def get_order(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.get_user_orders(db, user.id)

@router.post("/add/", response_model=schemas.OrderBase)
async def place_order(
    order: schemas.OrderCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await crud.place_order(db, user.id, order)