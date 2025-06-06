from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from manga.schemas import PublisherBase, MangaImageBase

class Volume_MangaBase(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class MangaVolumeBase(BaseModel):
    id: int
    volume_number: int
    title: str
    manga: Volume_MangaBase
    print_length: int
    language: str
    price: float
    release_date: Optional[date]
    isbn_10: str
    isbn_13: str
    publisher: PublisherBase
    images: list[MangaImageBase] = []

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    id: int
    quantity: int
    timestamp: datetime
    volume: MangaVolumeBase

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    volume_id: int
    quantity: int = 1

    class Config:
        from_attributes = True