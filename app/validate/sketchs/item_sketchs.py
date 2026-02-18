from app.validate.sketchs.base import SketchsBasevalidate
from pydantic import Field, field_validator
from app.exeption.item import NotNameItemSketchError, NameNoValideError, EmodziNoValideError, SizeNotIntItemSketchError

class ItemSketchValide(SketchsBasevalidate):
    name: str | None = None
    emodzi: str | None = None
    descriprtion: str | None = None
    size: int = 500
    image_id: int | None = None
    creator_id: int
    is_delete: bool = True
    rarity: float = 0.1
    min_drop: int = 1
    max_drop: int = 1
    nbt: dict = {}

    @field_validator('name', mode='before')
    @classmethod
    def name_valid(cls, name: str | None = None):
        if name == None:
            raise NotNameItemSketchError('User dont enter name to item sketch')
        if len(name) > 30:
            raise NameNoValideError('This user enter name and len(name) > 30')
        return name

    @field_validator('emodzi', mode='before')
    @classmethod
    def name_valid(cls, emodzi: str | None = None):
        if  emodzi != None:
            if len(emodzi) != 1:
                raise EmodziNoValideError('This user enter emodzi and len(emodzi) > 1')
        return emodzi    
    
    @field_validator('size', mode='after')
    @classmethod
    def name_valid(cls, size: str = '100'):
        is_size = str(size)
        if is_size.isdigit() == False:
            raise SizeNotIntItemSketchError('This user enter size, but size no int')
        return size
    
class ItemValide(SketchsBasevalidate):
    inventory_id: int | None = None
    sketch_id: int
    quantity: int = 1
    transfer_id: int | None = None
    from_char_transfers: bool | None = None

