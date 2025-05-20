from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from auth.models import User
from manga.models import MangaVolume

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    volume_id = Column(Integer, ForeignKey("manga_volume.id"))
    quantity = Column(Integer, default=1)

    user = relationship(User)
    volume = relationship(MangaVolume, back_populates="in_carts")