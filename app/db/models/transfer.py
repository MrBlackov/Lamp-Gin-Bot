from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.item import ItemDB, ItemSketchDB
from app.db.base import Base

class TransferDB(Base):
    seller_id: Mapped[int | None] = mapped_column(ForeignKey('characterdb.id', ondelete='SET NULL'), default=None)
    buyer_id: Mapped[int | None] = mapped_column(ForeignKey('characterdb.id', ondelete='SET NULL'), default=None)
    seller_items: Mapped[list[ItemDB]] = relationship('ItemDB', uselist=True, lazy='join', cascade='all')
    buyer_items: Mapped[list[ItemDB]] = relationship('ItemDB', uselist=True, lazy='join', cascade='all')
    status: Mapped[bool | None] = mapped_column(default=None)

