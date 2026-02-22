from app.validate.sketchs.base import SketchsBasevalidate
from pydantic import Field, field_validator
from app.exeption.item import NotNameItemSketchError, NameNoValideError, EmodziNoValideError, SizeNotIntItemSketchError, DropNotIntItemSketchError, DropLessZeroItemSketchError, SizeLessOneItemSketchError, RariryValideError

class ItemSketchValide(SketchsBasevalidate):
    name: str | None = None
    emodzi: str | None = None
    description: str | None = None
    size: int = 500
    image_id: int | None = None
    creator_id: int = 1
    is_delete: bool = True
    rarity: float = 0.1
    min_drop: int = 1
    max_drop: int = 1
    nbt: dict = {}
    is_hide: bool = True

    @field_validator('name', mode='before')
    @classmethod
    def name_valid(cls, name: str | None = None):
        if name == None:
            raise NotNameItemSketchError('User dont enter name to item sketch')
        if len(name) > 30:
            raise NameNoValideError('This user enter name and len(name) > 30')
        return name
    
    @field_validator('description', mode='before')
    @classmethod
    def description_valid(cls, description: str | None = None):
        if description:
            if len(description) > 200:
                raise NameNoValideError('This user enter description and len(description) > 200')
        return description
    
    @field_validator('emodzi', mode='before')
    @classmethod
    def emodzi_valid(cls, emodzi: str | None = None):
        if  emodzi != None:
            if len(emodzi) != 1:
                raise EmodziNoValideError('This user enter emodzi and len(emodzi) > 1')
        return emodzi    
    
    @field_validator('size', mode='before')
    @classmethod
    def size_valid(cls, size: str = '100'):
        is_size = str(size)
        if is_size.isdigit() == False:
            raise SizeNotIntItemSketchError('This user enter size, but size no int')
        if int(size) < 1:
            raise SizeLessOneItemSketchError('This user enter size, but size < 1')
        return int(size)
    
    @field_validator('rarity', mode='before')
    @classmethod
    def rarity_valid(cls, rarity: str = '0.1'):
        try:
            rarity = float(rarity)
        except (ValueError, TypeError):
            raise RariryValideError('Rarity must be a float')
        if not 0 <= rarity <= 1:
            raise RariryValideError('Rarity must be between 0 and 1')
        return rarity

    @field_validator('min_drop', mode='before')
    @classmethod
    def min_drop_valid(cls, min_drop: int = 1):
        try:
            min_drop = int(min_drop)
        except (ValueError, TypeError):
            raise DropNotIntItemSketchError('min_drop must be an integer')
        if min_drop < 0:
            raise DropLessZeroItemSketchError('min_drop must be a positive integer')
        return min_drop

    @field_validator('max_drop', mode='before')
    @classmethod
    def max_drop_valid(cls, max_drop: int = 1):
        try:
            max_drop = int(max_drop)
        except (ValueError, TypeError):
            raise DropNotIntItemSketchError('max_drop must be an integer')
        if max_drop < 0:
            raise DropLessZeroItemSketchError('max_drop must be a positive integer')
        return max_drop
    



class ItemValide(SketchsBasevalidate):
    inventory_id: int | None = None
    sketch_id: int
    quantity: int = 1
    transfer_id: int | None = None
    from_char_transfers: bool | None = None

