from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class ItemSketchDB:
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str]
    items: Mapped[list['ItemDB']] = relationship('ItemDB', uselist=True, lazy='select', cascade='all')

class ItemDB:
    inventory_id: Mapped[int] = mapped_column(ForeignKey('inventorydb.id'))
    quantity: Mapped[int]
    sketch: Mapped[ItemSketchDB] = relationship(ItemSketchDB, uselist=False, lazy='joined')

