from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from app.validate.api.characters import CharSketchInfo
from app.validate.info.characters import CharacterInfo
from app.validate.sketchs.item_sketchs import ItemSketch
from app.enum_type.char import Gender
import ast

class BaseAPIValidate(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class CreateCharSkecth(BaseAPIValidate):
    first_name: str = Field(max_length=50)
    last_name: str | None = Field(max_length=50, default=None)
    sketch: CharSketchInfo
    description: str | None = Field(max_length=200, default=None)
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        elif self.first_name:
            return self.first_name
        else:
            raise ValueError(f"This character({self.id}) hasn't first name")
 
class QueryBody(BaseAPIValidate):
    platform: Literal['tg']
    platform_id: int 

class QueryAddChar(QueryBody):
    create_sketch: CreateCharSkecth

class QueryGetSketchs(QueryBody):
    gender: str

    @field_validator('gender')
    @classmethod
    def serialization_gender(cls, g: str):
        if g in Gender:
            return g 
        else:
            raise ValueError(f'This value({g}) is not Gender')
        
class QueryChar(QueryBody):
    chars: list[CharacterInfo] | None = None
    main_id: int | None
    no_chars: bool = False

class QueryCharToMain(QueryBody):
    main_id: int 

class QueryCharID(QueryBody):
    char_id: int 

class QueryItem(QueryCharID):
    item_id: int

class QueryItemCreate(QueryCharID):
    item :ItemSketch

class QueryItemSellorGift(QueryCharID):
    puplure_id: int
    moneys: int | None = None
