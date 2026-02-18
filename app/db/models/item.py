from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON, Integer
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
    is_delete: Mapped[bool] = mapped_column(default=True)
    rarity: Mapped[float] = mapped_column(default=0.1)
    min_drop: Mapped[int] = mapped_column(default=1)
    max_drop: Mapped[int] = mapped_column(default=1)
    nbt: Mapped[dict] = mapped_column(JSON, default={})

class ItemDB(Base):
    inventory_id: Mapped[int | None] = mapped_column(ForeignKey('inventorydb.id'), nullable=True)
    transfer_id: Mapped[int | None] = mapped_column(ForeignKey('transferdb.id'), nullable=True)
    kitsketch_id: Mapped[int] = mapped_column(ForeignKey('kitsketchdb.id'), nullable=True)
    from_char_transfers: Mapped[bool | None] = mapped_column(default=None)
    sketch_id: Mapped[int] = mapped_column(ForeignKey('itemsketchdb.id'))
    quantity: Mapped[int] = mapped_column(default=1)
    sketch: Mapped[ItemSketchDB] = relationship(ItemSketchDB, uselist=False, lazy='joined', back_populates='items')
    inventory: Mapped[Base] = relationship('InventoryDB', uselist=False, lazy='joined', back_populates='items')
    
    @property
    def to_char_transfer(self):
        return False if self.from_char_transfers else True

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
