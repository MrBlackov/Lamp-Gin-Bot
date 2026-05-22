from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

class SkillSketchDB(Base):
    name: Mapped[str]
    tag: Mapped[str]
    _emodzi: Mapped[str] = mapped_column(default='💡')
    custom_emodzi_id: Mapped[str | None] = mapped_column(default=None)
    description: Mapped[str | None] = mapped_column(default=None)

    default_level: Mapped[int] = mapped_column(default=1)
    min_level: Mapped[int] = mapped_column(default=1, nullable=True)
    default_coins: Mapped[int] = mapped_column(default=0)
    xmod: Mapped[float] = mapped_column(default=1.0)
    price: Mapped[int | None] = mapped_column(default=None)
    is_activate: Mapped[bool] = mapped_column(default=False)
    action_tag: Mapped[str | None] = mapped_column(default=None)
    is_product: Mapped[bool] = mapped_column(default=False)
    is_base: Mapped[bool] = mapped_column(default=False)
    is_hide: Mapped[bool] = mapped_column(default=False)
    explore_iq: Mapped[int | None] = mapped_column(default=None)
    level_formula: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)
    up_level_formula: Mapped[dict[str, float] | None] = mapped_column(JSON, default=None)
    
    @property
    def emodzi(self):
        return f'<tg-emoji emoji-id="{self.custom_emodzi_id}">{self._emodzi}</tg-emoji>' if self.custom_emodzi_id else self._emodzi

    @property
    def text(self):
        return f'{self.emodzi} {self.name}'

class SkillDB(Base):
    level: Mapped[float]
    coins: Mapped[float] = mapped_column(default=0.0)
    sketch_id: Mapped[int] = mapped_column(ForeignKey('skillsketchdb.id'))
    sketch_tag: Mapped[str]
    sketch: Mapped[SkillSketchDB] = relationship(SkillSketchDB, uselist=False, lazy='joined')
    attribute_point_id: Mapped[int] = mapped_column(ForeignKey('attributepointdb.id'), default=0)

    @property
    def max_coins(self):
        return self.sketch.default_coins*(self.level/10)
    
    @property
    def text(self):
        return f'{self.sketch.text} ({self.level} ур.)'