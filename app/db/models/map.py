from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class LocationDB(Base):
    x: Mapped[int] = mapped_column(default=0)