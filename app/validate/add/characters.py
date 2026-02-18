from app.enum_type.char import Gender
from app.db.models.char import ExistenceDB, AttributePointDB, InventoryDB
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.validate.add.base import BaseAddValid
from app.exeption.char import CharHastNameError
from app.db.models.item import ItemSketchDB



class Inventory_add(BaseAddValid):
    items: list['ItemValide']

class AttributePoint_add(BaseAddValid):
    exist_id: int
    dexterity: int
    strength: int
    health: int
    intelligence: int
    speed_value: int = 0
    spirituality: int = 0

class ItemValide(BaseAddValid):
    inventory_id: int | None = None
    sketch_id: int
    sketch: ItemSketchDB
    quantity: int = 1
    transfer_id: int | None = None
    from_char_transfers: bool | None = None

class Points(BaseAddValid):
    dexterity: int
    strength: int
    health: int
    intelligence: int
    speed_value: int = 0
    spirituality: int = 0
        
    @property
    def speed(self):
        return (self.dexterity + self.health)/4 + self.speed_value
    
class CharSketch(BaseAddValid):
    points: Points
    age: int
    amount_life: int
    gender: Gender
    items: list[ItemValide]

    @field_validator('gender', mode='before')
    @classmethod
    def validate_gender(cls, v):
        if isinstance(v, str):
            return Gender(v.upper())
        return v
    
    @field_validator('points', mode='before')
    @classmethod
    def validate_points(cls, v: dict):
        return Points.model_validate(v)    



class Existence_add(BaseAddValid):
    people_id: int | None = None
    first_name: str = Field(max_length=50)
    last_name: str | None = Field(max_length=50, default=None)
    gender: Gender
    inventory: Inventory_add | InventoryDB | None = None
    attibute_point: AttributePoint_add | AttributePointDB | Points | None = None
    age: int
    amount_life: int
    die: bool = False
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + self.last_name
        elif self.first_name:
            return self.first_name
        else:
            raise CharHastNameError(f"This character({self.id}) hasn't first name")
   
class Npc_add(BaseAddValid):
    exist: ExistenceDB

class Character_add(BaseAddValid):
    user_id: int
    exist: Existence_add | ExistenceDB 
    description: str | None = Field(max_length=200, default=None)

