from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.item import ItemDB, ItemSketchDB
from app.db.base import Base
from datetime import datetime
from app.enum_type.transfer import ItemTransferStatusEnum, ItemTransferType

class TransferDB(Base):
    seller_id: Mapped[int | None] = mapped_column(ForeignKey('characterdb.id', ondelete='SET NULL'), nullable=True)
    buyer_id: Mapped[int | None] = mapped_column(ForeignKey('characterdb.id', ondelete='SET NULL'), nullable=True)

    seller_agree: Mapped[bool] = mapped_column(default=True)
    buyer_agree: Mapped[bool] = mapped_column(default=False)

    seller_items: Mapped[list[ItemDB] | None] = relationship('ItemDB', uselist=True, lazy='joined', cascade='all')
    buyer_items: Mapped[list[ItemDB] | None] = relationship('ItemDB', uselist=True, lazy='joined', cascade='all')

    type: Mapped[str] = mapped_column(default=ItemTransferType.TRADE.value)
    status: Mapped[str] = mapped_column(default=ItemTransferStatusEnum.PENDING.value)
    data_completion: Mapped[datetime | None] = mapped_column(default=None)
