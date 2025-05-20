from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
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

class OrderBase(BaseModel):
    id: int
    quantity: int
    timestamp: datetime
    volume: MangaVolumeBase

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    volume_id: int
    quantity: int = 1

    class Config:
        orm_mode = True