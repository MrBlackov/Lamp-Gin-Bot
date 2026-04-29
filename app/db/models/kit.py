from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

class KitSketchDB(Base):
    name: Mapped[str | None] = mapped_column(default=None)
    code: Mapped[str | None] = mapped_column(default=None)
    all_item_skeths: Mapped[bool] = mapped_column(default=False)
    hide: Mapped[bool] = mapped_column(default=True)    
    item_skeths: Mapped[list[int] | None] = mapped_column(ARRAY(Integer, ForeignKey('itemsketchdb.id')), default=None)
    kits: Mapped[list['KitDB']] = relationship('KitDB', uselist=True, lazy='select', cascade='all', back_populates='sketch')

class KitDB(Base):
    get: Mapped[bool] = mapped_column(default=False)    
    sketch_id: Mapped[int] = mapped_column(ForeignKey('kitsketchdb.id'))
    inventory_id: Mapped[int | None] = mapped_column(ForeignKey('inventorydb.id'), nullable=True)
    sketch: Mapped[KitSketchDB] = relationship(KitSketchDB, uselist=False, lazy='joined', back_populates='kits')   
    inventory: Mapped[Base] = relationship('InventoryDB', uselist=False, lazy='select', back_populates='kit') 
