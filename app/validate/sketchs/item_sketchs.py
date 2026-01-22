from app.validate.sketchs.base import SketchsBasevalidate
from pydantic import Field, field_validator
from app.exeption.item import NotNameItemSketchError, NameNoValideError

class ItemSketch(SketchsBasevalidate):
    name: str | None = None
    descriprtion: str | None = None

    @field_validator('name', mode='before')
    @classmethod
    def name_valid(cls, name: str | None = None):
        if name == None:
            raise NotNameItemSketchError('User dont enter name to item sketch')
        if len(name) > 30:
            raise NameNoValideError('This user enter name and len(name) > 30')
        return name
