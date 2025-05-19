from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from cart.models import Cart
from manga.models import MangaVolume
from fastapi import HTTPException, status
from cart.schemas import CartCreate

async def get_user_cart(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Cart)
        .filter_by(user_id=user_id)
        .options(joinedload(Cart.volume).joinedload(MangaVolume.images))
    )
    return result.scalars().all()

async def add_to_cart(db: AsyncSession, user_id: int, cart_data: CartCreate):
    result = await db.execute(select(MangaVolume).filter_by(id=cart_data.volume_id))
    volume = result.scalars().all()
    if not volume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volume not found")
    
    result = await db.execute(
        select(Cart)
        .filter_by(user_id=user_id, volume_id=cart_data.volume_id)
    )
    cart_item = result.scalars().all()

    if cart_item:
        # Update quantity
        cart_item.quantity += cart_data.quantity
    else:
        # Create new cart item
        cart_item = Cart(
            user_id=user_id,
            volume_id=cart_data.volume_id,
            quantity=cart_data.quantity
        )
        db.add(cart_item)

        await db.commit()
        await db.refresh(cart_item)
        return cart_item