from app.validate.info.base import BaseInfoValid
from app.enum_type.char import Gender
from app.validate.info.items import ItemInfo
from app.exeption.char import CharHastNameError

class SavingInfo(BaseInfoValid):
    exist_id: int
    penny: int

#class InventoryInfo(BaseInfoValid):
#    exist_id: int
#    items: list[ItemInfo] | None = None

class AttributePointsInfo(BaseInfoValid):
    exist_id: int
    strength: int
    dexterity: int
    intelligence: int
    health: int
    spirituality: int
    speed_value: int 
    
    @property
    def speed(self):
        return (self.dexterity + self.health)/4 + self.speed_value

class EXistanceInfo(BaseInfoValid):
    first_name: str
    last_name: str | None = None
    gender: Gender
    age: int
    amount_life: int
    saving: SavingInfo
#    inventory: InventoryInfo
    attibute_point: AttributePointsInfo
    location: None = None
    die: bool
    
    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        elif self.first_name:
            return self.first_name
        else:
            raise CharHastNameError(f"This character({self.id}) hasn't first name")

class CharacterInfo(BaseInfoValid):
    user_id: int
    exist: EXistanceInfo
    description: str | None



