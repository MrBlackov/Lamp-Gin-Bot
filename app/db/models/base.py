from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import List
from app.enum_type.bd import TgType, WorkType

class TgUserDB(Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    #user_id: Mapped[int] = mapped_column(ForeignKey("userdb.id"))
    fullname: Mapped[str]
    username: Mapped[str | None] = mapped_column(String, default=None)
    data: Mapped[dict] = mapped_column(JSON)
    bans: Mapped[bool] = mapped_column(default=False)

class TgChatDB(Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    tg_type: Mapped[TgType]
    work_type: Mapped[WorkType] = mapped_column(default=WorkType.USUAL.value)
    fullname: Mapped[str]
    username: Mapped[str | None]
    invite_self: Mapped[str | None ] = mapped_column(default=None)
    data: Mapped[dict] = mapped_column(JSON)

class DonateDB(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('userdb.id'))
    chaos_coins: Mapped[int] = mapped_column(default=0)
    char_quantity: Mapped[int] = mapped_column(default=1)
    char_regeneration: Mapped[int] = mapped_column(default=3)

class UserDB(Base):
    tg_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, default=None)
    name: Mapped[str | None] = mapped_column(default=None)
    bans: Mapped[bool] = mapped_column(default=False)
    donates: Mapped[DonateDB | None] = relationship(DonateDB, uselist=False, lazy='joined', primaryjoin="foreign(DonateDB.user_id) == UserDB.id")
    main_char: Mapped[int | None] = mapped_column(ForeignKey("characterdb.id", ondelete='SET NULL'), default=None)
    tg_user: Mapped[TgUserDB | None] = relationship(TgUserDB, uselist=False, lazy='joined', primaryjoin="foreign(TgUserDB.tg_id) == UserDB.tg_id")
    
