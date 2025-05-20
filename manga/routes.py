from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from database.database import get_db
from manga import schemas, crud
from manga.models import Manga, MangaVolume  # Added explicit imports for clarity
from cloudinary.uploader import upload
import cloudinary

router = APIRouter(prefix="/manga", tags=["manga"])

@router.get("/", response_model=list[schemas.MangaBase])
async def get_all_mange(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(Manga)
            .options(
                joinedload(Manga.volumes)
                .joinedload(MangaVolume.images),
                joinedload(Manga.volumes)
                .joinedload(MangaVolume.publisher)  # <-- Ensure publisher is loaded
            )
        )
        return result.unique().scalars().all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str(e)})

@router.get("/volumes", response_model=list[schemas.MangaVolumeBase])
async def get_all_volumes(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(MangaVolume)
            .options(
                joinedload(MangaVolume.manga),
                joinedload(MangaVolume.publisher),
                joinedload(MangaVolume.images)
            )
        )
        return result.unique().scalars().all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str(e)})

@router.get("/search", response_model=list[schemas.SearchMangaBase])
async def search_manga(q: str = "", db: AsyncSession = Depends(get_db)):
    return await crud.search_manga(db, q)

@router.get("/{manga_id}/volume/", response_model=list[schemas.MangaVolumeBase])
async def get_manga_volumes(manga_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_volume_by_manga_id(db, manga_id)

@router.get("/volume/{volume_id}/", response_model=schemas.MangaVolumeBase)
async def get_volume_detail(volume_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_volume_by_id(db, volume_id)

@router.post("/volume/{volume_id}/images/", response_model=schemas.MangaImageBase)
async def upload_volume_image(
    volume_id: int,
    file: UploadFile = File(...),
    caption: str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    await crud.get_volume_by_id(db, volume_id)  # Validate volume exists
    try:
        upload_response = upload(file.file)
        image_url = upload_response['secure_url']
        public_id = upload_response['public_id']
        image = await crud.add_volume_image(db, volume_id, public_id, image_url, caption)
        return image
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
