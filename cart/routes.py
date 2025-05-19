from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from cart import schemas, crud
from auth.routes import get_current_user
from auth.models import User

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=list[schemas.CartBase])
async def get_cart(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await crud.get_user_cart(db, user.id)

@router.post("/add/", response_model=schemas.CartBase)
async def add_to_cart(
    cart: schemas.CartCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await crud.add_to_cart(db, user.id, cart)