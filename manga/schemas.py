from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class PublisherBase(BaseModel):
    id: int
    publisher_name: str

    class Config:
        from_attributes = True

class Volume_MangaBase(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class MangaImageBase(BaseModel):
    id: int
    image_url: Optional[str] = None
    caption: Optional[str] = None

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
    images: List[MangaImageBase] = []

    class Config:
        from_attributes = True

class MangaBase(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    volumes: List[MangaVolumeBase] = []

    class Config:
        from_attributes = True

class MangaVolumeCreate(BaseModel):
    manga_id: int
    volume_number: int
    title: str
    print_length: int = 187
    language: str
    price: float
    release_date: Optional[date] = None
    isbn_10: str
    isbn_13: str
    manga_publisher_id: int

    class Config:
        from_attributes = True


class SearchMangaBase(BaseModel):
    manga: Optional[MangaBase]
    volume: Optional[MangaVolumeBase]