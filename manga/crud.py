from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import or_
from manga.models import Manga, MangaVolume, MangaImage
from fastapi import HTTPException, status
from typing import Optional

async def get_manga_by_id(db: AsyncSession, manga_id:int):
    result = await db.execute(
        select(Manga)
        .filter_by(id=manga_id)
        .options(
            joinedload(Manga.volumes)
            .joinedload(MangaVolume.images),
            joinedload(Manga.volumes)
            .joinedload(MangaVolume.publisher)
            )
        )
    manga = result.unique().scalars().first()
    if not manga:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manga not found")
    return manga

async def get_volume_by_id(db: AsyncSession, volume_id: int):
    result = await db.execute(
        select(MangaVolume)
        .filter_by(id=volume_id)
        .options(
            joinedload(MangaVolume.images),
            joinedload(MangaVolume.publisher),
            joinedload(MangaVolume.manga)
        )
    )
    volume = result.unique().scalars().first()
    if not volume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manga not found")
    return volume

async def get_volume_by_manga_id(db: AsyncSession, manga_id: int):
    result = await db.execute(
        select(MangaVolume)
        .filter_by(manga_id=manga_id)
        .options(
            joinedload(MangaVolume.images),
            joinedload(MangaVolume.publisher),
            joinedload(MangaVolume.manga)
        )
    )
    volumes = result.unique().scalars().all()
    if not volumes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manga not found")
    return volumes

async def add_volume_image(db: AsyncSession, volume_id: int, public_id: str, image_url: str, caption: Optional[str]):
    volume = await get_volume_by_id(db, volume_id)
    image = MangaImage(volume_id=volume_id, image=public_id, image_url=image_url, caption=caption)
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image

async def search_manga(db: AsyncSession, query: str):
    if not query:
        result = await db.execute(
            select(Manga)
            .options(
                joinedload(Manga.volumes)
                .joinedload(MangaVolume.images),
                joinedload(Manga.volumes)
                .joinedload(MangaVolume.publisher)
            )
        )
        return result.unique().scalars().all()
    
    query_like = f"%{query}%"
    response = []

    manga_result = await db.execute(
        select(Manga)
        .options(
            joinedload(Manga.volumes).joinedload(MangaVolume.images),
            joinedload(Manga.volumes).joinedload(MangaVolume.publisher)
        )
        .where(
            Manga.title.ilike(query_like) |
            Manga.author.ilike(query_like)
        )
    )
    mangas = manga_result.unique().scalars().all()

    for manga in mangas:
        response.append({"manga": manga, "volume": None})

    volume_result = await db.execute(
        select(MangaVolume)
        .options(
            joinedload(MangaVolume.images),
            joinedload(MangaVolume.publisher),
            joinedload(MangaVolume.manga)
        )
        .where(
            MangaVolume.title.ilike(query_like)
        )
    )
    volumes = volume_result.unique().scalars().all()

    for volume in volumes:
        if not any(manga.id == volume.manga_id for manga in mangas):
            response.append({"manga": None, "volume": volume})

    return response