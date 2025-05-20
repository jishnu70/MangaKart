from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base
from auth.models import User
from manga.models import MangaVolume

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    volume_id = Column(Integer, ForeignKey("manga_volume.id"))
    quantity = Column(Integer, default=1)
    timestamp = Column(DateTime, server_default=func.now())

    user = relationship(User)
    volume = relationship(MangaVolume, back_populates="orders")