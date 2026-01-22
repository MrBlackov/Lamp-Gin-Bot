from app.validate.info.base import BaseInfoValid

class ItemInfo(BaseInfoValid):
    inventory_id: int
    name: str
    eng: str
    quantity: float
    type: str
    data: dict | None = None
    descriprtion: str | None = None

class ItemSketchInfo(BaseInfoValid):
    name: str
    eng: str
    quantity: float
    type: str
    data: dict | None = None
    descriprtion: str | None = None
