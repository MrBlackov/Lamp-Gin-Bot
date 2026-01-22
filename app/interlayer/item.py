from typing import Literal
from app.service.utils import str_to_json
from app.validate.sketchs.item_sketchs import ItemSketch
from app.logic.item import Items, ItemSketchs

class ItemLayer:
    def create(self, sketch: str, type_sketch: Literal['str', 'doc', 'json']):
        if type_sketch == 'str':
            item = ItemSketch(**str_to_json(sketch))
   

