from pydantic import BaseModel, ConfigDict
from app.enum_type.bd import WorkType, TgType

class CraftValide(BaseModel):
    ingredients: list
    tools: list
    results: list
    time: int = 0
    is_hide: bool

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class BookValide(BaseModel):
    name: str
    author: str 
    author_char_id: int 
    is_close_setting: bool = False
    description: str = ''
    pages: list[str] = []

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class StudyValide(BaseModel):
    tag: str
    level: int
    iq: int = 10
    up_level: float = 0.01

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)



