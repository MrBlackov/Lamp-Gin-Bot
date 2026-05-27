from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime, timedelta, time, date
from app.db.models.main import ChatDB

class DropDB(Base):
    open: Mapped[datetime]
    reset: Mapped[datetime] = mapped_column(default=datetime.combine(date.today() + timedelta(days=1), time.min))
    _items: Mapped[list[str]] = mapped_column(ARRAY(String))
    chat_id: Mapped[int] = mapped_column(ForeignKey('chatdb.id'))
    chat: Mapped[ChatDB] = relationship('ChatDB', uselist=False, lazy='joined')
    is_open: Mapped[bool] = mapped_column(default=False)

    @property
    def items(self) -> list[tuple[int, int]]:
        return [tuple(map(int, i.split(':'))) for i in self._items]
    