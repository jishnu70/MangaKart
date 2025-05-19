from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import relationship
from database.database import Base

class Manga(Base):
    __tablename__ = "manga"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, index=True)
    author = Column(String(100))
    description = Column(Text, nullable=True)

    volumes = relationship("MangaVolume", back_populates="manga")

class Publisher(Base):
    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True, index=True)
    publisher_name = Column(String(25))

    manga_publisher = relationship("MangaVolume", back_populates="publisher")

class MangaVolume(Base):
    __tablename__ = "manga_volume"

    id = Column(Integer, primary_key=True, index=True)
    manga_id = Column(Integer, ForeignKey("manga.id"))
    volume_number = Column(Integer)
    title = Column(String(100))
    print_length = Column(Integer, default=187)
    language = Column(String(25))
    price = Column(DECIMAL(7, 2))
    release_date = Column(Date, nullable=True)
    isbn_10 = Column(String(20))
    isbn_13 = Column(String(20))
    manga_publisher_id = Column(Integer, ForeignKey("publisher.id"))

    manga = relationship("Manga", back_populates="volumes")
    publisher = relationship("Publisher", back_populates="manga_publisher")
    images = relationship("MangaImage", back_populates="volume")
    in_carts = relationship("Cart", back_populates="volume")
    orders = relationship("Order", back_populates="volume")

class MangaImage(Base):
    __tablename__ = "manga_image"

    id = Column(Integer, primary_key=True, index=True)
    volume_id = Column(Integer, ForeignKey("manga_volume.id"))
    image = Column(String(255), nullable=True)  # Store Cloudinary public_id
    image_url = Column(String(255), nullable=True)
    caption = Column(String(255), nullable=True)

    volume = relationship("MangaVolume", back_populates="images")