from app.enum_type.char import Gender
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
import ast

class BaseInfoValid(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class PointsInfo(BaseInfoValid):
    dexterity: int
    strength: int
    health: int
    intelligence: int
    speed_value: int = 0
    spirituality: int = 0
        
    @property
    def speed(self):
        return (self.dexterity + self.health)/4 + self.speed_value
    
class CharSketchInfo(BaseInfoValid):
    points: PointsInfo
    age: int
    amount_life: int
    gender: str
    penny: int

    @field_validator('points', mode='before')
    @classmethod
    def validate_points(cls, v: dict):
        return PointsInfo.model_validate(v)    
    
    @field_validator('gender')
    @classmethod
    def serialization_gender(cls, g: str):
        if g in Gender:
            return g 
        else:
            raise ValueError(f'This value({g}) is not Gender')

    
class GetSketchsInfo(BaseInfoValid):
    first_names: list[str]
    last_names: list[str]
    sketchs: list[CharSketchInfo]

#    @field_validator('first_names', 'last_names', mode='before')
#    @classmethod
#    def validate_names(cls, v: str):
#        print(v)
#        return ast.literal_eval(v)
#
#    @field_validator('sketchs', mode='before')
#    @classmethod
#    def validate_sketches(cls, v: str) -> list[CharSketchInfo]:
#        return [CharSketchInfo.model_validate(ast.literal_eval(d)) for d in ast.literal_eval(v)]