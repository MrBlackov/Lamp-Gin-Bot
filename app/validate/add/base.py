from pydantic import BaseModel, ConfigDict
from app.enum_type.bd import WorkType, TgType
from app.db.models.base import DonateDB

class BaseAddValid(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class TgUsers_add(BaseAddValid):
    tg_id: int
    fullname: str
    username: str | None
    bans: bool = False
    data: dict = {}

class TgChats_add(BaseAddValid):
    tg_id: int
    fullname: str
    username: str | None
    tg_type: TgType
    work_type: WorkType
    data: dict = {}
    invite_self: str | None = None

class Donates_add(BaseAddValid):
    user_id: int
    chaos_coins: int = 0
    char_quantity: int = 1
    char_regeneration: int = 3

class Users_add(BaseAddValid):
    tg_id: int | None = None
    name: str | None = None
    bans: bool = False
    donates: DonateDB | None = None

