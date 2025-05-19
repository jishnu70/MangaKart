from pydantic import BaseModel
from typing import Optional
from datetime import date
from manga.schemas import PublisherBase, MangaImageBase

class MangaVolumeBase(BaseModel):
    id: int
    volume_number: int
    title: str
    print_length: int
    language: str
    price: float
    release_date: Optional[date]
    isbn_10: str
    isbn_13: str
    manga_publisher: PublisherBase
    images: list[MangaImageBase] = []

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    id: int
    quantity: int
    volume: MangaVolumeBase

    class Config:
        orm_mode = True

class CartCreate(BaseModel):
    volume_id: int
    quantity: int = 1