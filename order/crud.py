from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from order.models import Order
from manga.models import MangaVolume
from fastapi import HTTPException, status
from order.schemas import OrderCreate

async def get_user_orders(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Order)
        .filter_by(user_id = user_id)
        .options(
            joinedload(Order.volume)
            .joinedload(MangaVolume.images),
            joinedload(Order.volume)
            .joinedload(MangaVolume.publisher),
            joinedload(Order.volume)
            .joinedload(MangaVolume.manga)
        )
    )
    return result.unique().scalars().all()

async def place_order(db: AsyncSession, user_id: int, order_data: OrderCreate):
    # Validate volume exists
    result = await db.execute(
        select(MangaVolume)
        .options(
            joinedload(MangaVolume.images),
            joinedload(MangaVolume.publisher),
            joinedload(MangaVolume.manga)
        )
        .filter_by(id=order_data.volume_id)
    )
    volume = result.scalars().first()
    if not volume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Volume not found")
    
    # Create order
    order = Order(
        user_id = user_id,
        volume_id = order_data.volume_id,
        quantity = order_data.quantity
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)

    result = await db.execute(
        select(Order)
        .options(
            joinedload(Order.volume)
            .joinedload(MangaVolume.images),
            joinedload(Order.volume)
            .joinedload(MangaVolume.publisher),
            joinedload(Order.volume)
            .joinedload(MangaVolume.manga)
        )
    )
    order_item = result.unique().scalars().first()

    return order_item