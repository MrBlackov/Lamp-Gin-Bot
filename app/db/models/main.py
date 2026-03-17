from sqlalchemy import String, ARRAY, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import List
from app.enum_type.bd import TgType, WorkType
from datetime import datetime

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
    setting_id: Mapped[int] = mapped_column(ForeignKey('usersettingdb.id'), nullable=True)

    def add_setting(self, setting: 'UserSettingDB') -> 'UserDB':
        self.setting = setting
        return self

class ChatDB(Base):
    tg_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, default=None)
    tg_chat: Mapped[TgChatDB | None] = relationship(TgChatDB, uselist=False, lazy='joined', primaryjoin="foreign(TgChatDB.tg_id) == ChatDB.tg_id")
    is_ban: Mapped[bool] = mapped_column(default=False)
    setting_id: Mapped[int] = mapped_column(ForeignKey('chatsettingdb.id'), nullable=True)

    def add_setting(self, setting: 'ChatSettingDB') -> 'ChatDB':
        self.setting = setting
        return self

class ChatSettingDB(Base):
    chat_id: Mapped[int] = mapped_column(ForeignKey('chatdb.id'))
    msg_delete_time: Mapped[int] = mapped_column(default=360)
    is_msg_delete: Mapped[bool] = mapped_column(default=False)

class UserSettingDB(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('userdb.id'))

class MessageDB(Base):
    chat_tg_id: Mapped[int] = mapped_column(BigInteger)
    msg_id: Mapped[int] = mapped_column(BigInteger)
    is_delete: Mapped[bool] = mapped_column(default=True)
    time_delete: Mapped[datetime] = mapped_column(index=True)

