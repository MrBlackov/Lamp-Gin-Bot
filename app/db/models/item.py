from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.db.models.map import LocationDB  # noqa: F401
from datetime import datetime
from app.db.models.kit import KitDB, KitSketchDB
from app.db.models.skill import SkillDB, SkillSketchDB

class ItemSketchDB(Base):
    name: Mapped[str] = mapped_column(String(30))
    tag: Mapped[str] = mapped_column(nullable=True)
    action: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True, default=['throw'])
    _emodzi: Mapped[str] = mapped_column(default='')
    custom_emodzi_id: Mapped[str | None] = mapped_column(default=None)
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
    is_hide: Mapped[bool] = mapped_column(default=False, nullable=True)

    @property
    def emodzi(self):
        return f'<tg-emoji emoji-id="{self.custom_emodzi_id}">{self._emodzi}</tg-emoji>' if self.custom_emodzi_id else self._emodzi

    @property
    def text(self):
        return f'{self.emodzi} {self.name}'
    
    @property
    def button_text(self):
        if self.custom_emodzi_id:
            return {'text':self.name, 'icon_custom_emoji_id':str(self.custom_emodzi_id)}
        return {'text':self.text}

class ItemDB(Base):
    inventory_id: Mapped[int | None] = mapped_column(ForeignKey('inventorydb.id'), nullable=True)
    transfer_id: Mapped[int | None] = mapped_column(ForeignKey('transferdb.id'), nullable=True)
    kitsketch_id: Mapped[int] = mapped_column(ForeignKey('kitsketchdb.id'), nullable=True)
    craft_id: Mapped[int] = mapped_column(ForeignKey('craftdb.id'), nullable=True)
    location_id: Mapped[int] = mapped_column(ForeignKey('locationdb.id'), nullable=True)
    #from_char_transfers: Mapped[bool | None] = mapped_column(default=None)
    sketch_id: Mapped[int] = mapped_column(ForeignKey('itemsketchdb.id'))
    quantity: Mapped[int] = mapped_column(default=1)
    sketch: Mapped[ItemSketchDB] = relationship(ItemSketchDB, uselist=False, lazy='joined', back_populates='items')
    inventory: Mapped[Base] = relationship('InventoryDB', uselist=False, lazy='joined')
    nbt: Mapped[dict] = mapped_column(JSON, default={})

    @property
    def from_char_transfers(self) -> bool | None:
        return self.nbt.get('from_char_transfers')

    @property
    def is_pick_up(self) -> bool | None:
        return self.nbt.get('is_pick_up')
    
    @property
    def to_char_transfer(self):
        return False if self.from_char_transfers else True

    def to_text(self, quantity: int | None = None):
        return f'{self.sketch.text}{f' ({quantity} шт.)' if quantity and quantity > 1 else ''}'
    
    @property
    def text(self):
        return self.to_text(self.quantity)
    
    def to_button_text(self, quantity: int | None = None):
        if self.sketch.custom_emodzi_id:
            return self.sketch.button_text | {'text':f'{self.sketch.name}{f' ({quantity} шт.)' if quantity and quantity > 1 else ''}'}
        return {'text':self.to_text(quantity)}
    
    @property
    def button_text(self):
        return self.to_button_text(self.quantity)

class CraftDB(Base):
    ingredient_ids: Mapped[list[int] | None] = mapped_column(ARRAY(Integer, ForeignKey('itemdb.id')), default=None)
    result_ids: Mapped[list[int] | None] = mapped_column(ARRAY(Integer, ForeignKey('itemdb.id')), default=None)
    tool_ids: Mapped[list[int] | None] = mapped_column(ARRAY(Integer, ForeignKey('itemdb.id')), default=None)
    is_hide: Mapped[bool] = mapped_column(default=True)
    is_create: Mapped[bool] = mapped_column(default=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('userdb.id'), default=1)
    time: Mapped[int] = mapped_column(default=0)

    def add_items(self, items: list[ItemDB]):
        self.items = items
        return self

    @property
    def ingredients(self) -> list[ItemDB]:
        item_ids = {i.id:i for i in self.items}
        item_dict = []
        for item_id in self.ingredient_ids:
            item = item_ids.get(item_id)
            if item:
                item_dict.append(item)
        return item_dict
    
    @property
    def tools(self) -> list[ItemDB]:
        item_ids = {i.id:i for i in self.items}
        item_dict= []
        for item_id in self.tool_ids:
            item = item_ids.get(item_id)
            if item:
                item_dict.append(item)
        return item_dict
    
    @property
    def results(self) -> list[ItemDB]:
        item_ids = {i.id:i for i in self.items}
        item_dict = []
        for item_id in self.result_ids:
            item = item_ids.get(item_id)
            if item:
                item_dict.append(item)
        return item_dict

    def ingredients_emodzi(self, to_str: bool = False, sep: str = ''):
        emodzi_list = [i.sketch._emodzi for i in self.ingredients] if self.ingredients else []
        if len(emodzi_list) == 0:
            return '💮'
        return sep.join(emodzi_list) if to_str else emodzi_list
    
    def results_emodzi(self, to_str: bool = False, sep: str = ''):
        emodzi_list = [i.sketch._emodzi for i in self.results] if self.results else []
        if len(emodzi_list) == 0:
            return '⚗️'
        return sep.join(emodzi_list) if to_str else emodzi_list
    
    def tools_emodzi(self, to_str: bool = False, sep: str = ''):
        emodzi_list = [i.sketch.emodzi for i in self.tools] if self.tools else []
        if len(emodzi_list) == 0:
            return '🛠️'
        return sep.join(emodzi_list) if to_str else emodzi_list  
    
    def to_mini_text(self, text: str, max_size: int):
        if max_size > len(text) or len(text) - max_size < 4:
            return text
        return text[:max_size] + '.'
    
    def result_text(self, max_simvols: int = 7):
        return self.to_mini_text(self.results[0].sketch.name, max_simvols)
    
    def ingredient_text(self, max_simvols: int = 7):
        return self.to_mini_text(self.ingredients[0].sketch.name, max_simvols)

