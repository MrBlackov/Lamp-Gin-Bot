from pydantic import BaseModel, ConfigDict
from app.enum_type.bd import WorkType, TgType

class Users_add(BaseModel):
    tg_id: int
    fullname: str
    username: str | None
    bans: bool = False
    data: dict = {}

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class Chats_add(BaseModel):
    tg_id: int
    fullname: str
    username: str | None
    tg_type: str 
    work_type: str = WorkType.USUAL.value
    data: dict = {}
    invite_self: str | None = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)