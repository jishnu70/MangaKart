from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from cart.models import Cart
from manga.models import MangaVolume
from fastapi import HTTPException, status
from cart.schemas import CartCreate

async def get_user_cart(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Cart)
        .filter_by(user_id=user_id)
        .options(
            joinedload(Cart.volume)
            .joinedload(MangaVolume.images),
            joinedload(Cart.volume)
            .joinedload(MangaVolume.publisher),
            joinedload(Cart.volume)
            .joinedload(MangaVolume.manga)
        )
    )
    return result.unique().scalars().all()

async def add_to_cart(db: AsyncSession, user_id: int, cart_data: CartCreate):
    result = await db.execute(
        select(MangaVolume)
        .filter_by(id=cart_data.volume_id)
        .options(
            joinedload(MangaVolume.images),
            joinedload(MangaVolume.publisher),
            joinedload(MangaVolume.manga)
        )
    )
    volume = result.scalars().first()
    if not volume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volume not found")
    
    result = await db.execute(
        select(Cart)
        .options(
            selectinload(Cart.volume)
            .selectinload(MangaVolume.images),
            selectinload(Cart.volume)
            .selectinload(MangaVolume.publisher),
            selectinload(Cart.volume)
            .selectinload(MangaVolume.manga),
        )
        .filter_by(user_id=user_id, volume_id=cart_data.volume_id)
    )
    cart_item = result.scalars().first()

    if cart_item:
        cart_item.quantity += cart_data.quantity
        await db.commit()
        await db.refresh(cart_item)
        return cart_item
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
    
    result = await db.execute(
        select(Cart)
        .options(
            joinedload(Cart.volume)
            .joinedload(MangaVolume.images),
            joinedload(Cart.volume)
            .joinedload(MangaVolume.publisher),
            joinedload(Cart.volume)
            .joinedload(MangaVolume.manga)
        )
    )
    cart_item = result.unique().scalars().first()

    return cart_item