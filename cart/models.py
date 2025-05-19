from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    volume_id = Column(Integer, ForeignKey("manga_volume.id"))
    quantity = Column(Integer, default=1)

    user = relationship("auth.models.User")
    volume = relationship("manga.models.MangaVolume", back_populates="in_carts")