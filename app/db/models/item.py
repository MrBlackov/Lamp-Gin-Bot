from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class ItemSketchDB(Base):
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str]
    items: Mapped[list['ItemDB']] = relationship('ItemDB', uselist=True, lazy='select', cascade='all', back_populates='sketch')

class ItemDB(Base):
    inventory_id: Mapped[int] = mapped_column(ForeignKey('inventorydb.id'))
    sketch_id: Mapped[int] = mapped_column(ForeignKey('itemsketchdb.id'))
    quantity: Mapped[int]
    sketch: Mapped[ItemSketchDB] = relationship(ItemSketchDB, uselist=False, lazy='joined', back_populates='items')

