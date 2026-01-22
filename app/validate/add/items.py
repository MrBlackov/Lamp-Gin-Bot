from app.enum_type.item import ItemType
from app.db.models.game.items import ItemDB
from app.db.models.game.characters import SavingDB, ExistenceDB, InventoryDB, AttributePointDB
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.validate.add.base import BaseAddValid


class Item_add(BaseAddValid):
    inventory_id: int
    name: str
    quantity: float
    type: ItemType
    data: dict | None =None
    descriprtion: str | None = None

class ItemSketch_add(BaseAddValid):
    name: str
    quantity: float
    type: ItemType
    data: dict | None =None
    descriprtion: str | None = None