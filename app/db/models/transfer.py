from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.item import ItemDB, ItemSketchDB
from app.db.models.char import CharacterDB
from app.db.base import Base
from datetime import datetime
from app.enum_type.transfer import ItemTransferStatusEnum, ItemTransferType

class TransferDB(Base):
    seller_id: Mapped[int | None] = mapped_column(ForeignKey('characterdb.id', ondelete='SET NULL'), nullable=True)
    buyer_id: Mapped[int | None] = mapped_column(ForeignKey('characterdb.id', ondelete='SET NULL'), nullable=True)
    
    seller: Mapped[CharacterDB | None] = relationship('CharacterDB', uselist=False, lazy='joined', foreign_keys=[seller_id])
    buyer: Mapped[CharacterDB | None] = relationship('CharacterDB', uselist=False, lazy='joined', foreign_keys=[buyer_id])

    seller_agree: Mapped[bool] = mapped_column(default=True)
    buyer_agree: Mapped[bool] = mapped_column(default=False)

    seller_items: Mapped[list[int] | None] = mapped_column(ARRAY(Integer, ForeignKey('itemdb.id')), default=None)
    buyer_items: Mapped[list[int] | None] = mapped_column(ARRAY(Integer, ForeignKey('itemdb.id')), default=None)

    type: Mapped[str] = mapped_column(default=ItemTransferType.TRADE.value)
    status: Mapped[str]
    data_completion: Mapped[datetime | None] = mapped_column(default=None)
