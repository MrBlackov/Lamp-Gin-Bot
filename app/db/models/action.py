from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime
from app.db.models.char import ExistenceDB
from app.db.models.main import ChatDB

class ActionStateDB(Base):
    tag: Mapped[str] = mapped_column(nullable=True)
    level: Mapped[int] = mapped_column(default=1)
    is_block_freedom: Mapped[bool] = mapped_column(default=False)
    reset: Mapped[int | None] = mapped_column(default=None)
    start: Mapped[datetime | None] = mapped_column(default=None)
    #check_datetime: Mapped[datetime | None] = mapped_column(default=None)
    end: Mapped[datetime | None] = mapped_column(default=None)
    nbt: Mapped[dict] = mapped_column(JSON, default={})
    exist_id: Mapped[int] = mapped_column(ForeignKey('existencedb.id'), nullable=True)
    exist: Mapped[ExistenceDB] = relationship('ExistenceDB', uselist=False, lazy='joined')
    chat_id: Mapped[int | None] = mapped_column(ForeignKey('chatdb.id'), nullable=True)
    chat: Mapped[ChatDB] = relationship('ChatDB', uselist=False, lazy='joined')