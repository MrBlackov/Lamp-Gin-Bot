from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class ItemSketchDB(Base):
    name: Mapped[str] = mapped_column(String(30))
    emodzi: Mapped[str] = mapped_column(default='')
    description: Mapped[str | None] = mapped_column(default=None)
    size: Mapped[int] = mapped_column(default=100)
    items: Mapped[list['ItemDB']] = relationship('ItemDB', uselist=True, lazy='select', cascade='all', back_populates='sketch')
    image_id: Mapped[int | None] = mapped_column(default=None)
    creator_id: Mapped[int] = mapped_column(ForeignKey('userdb.id'))

class ItemDB(Base):
    inventory_id: Mapped[int] = mapped_column(ForeignKey('inventorydb.id'))
    #transfer_id: Mapped[int | None] = mapped_column(ForeignKey('transferdb.id'), default=None)
    sketch_id: Mapped[int] = mapped_column(ForeignKey('itemsketchdb.id'))
    quantity: Mapped[int] = mapped_column(default=1)
    sketch: Mapped[ItemSketchDB] = relationship(ItemSketchDB, uselist=False, lazy='joined', back_populates='items')
    inventory: Mapped[Base] = relationship('InventoryDB', uselist=False, lazy='select', back_populates='items')


