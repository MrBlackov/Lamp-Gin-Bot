from pydantic import BaseModel, ConfigDict
from app.enum_type.bd import WorkType, TgType

class CraftValide(BaseModel):
    ingredients: list
    tools: list
    results: list
    time: int = 0
    is_hide: bool

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class TestValide(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
