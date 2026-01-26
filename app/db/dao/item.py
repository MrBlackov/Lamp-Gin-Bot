from app.db.dao.base import BaseDAO
from app.db.models.item import ItemDB, ItemSketchDB

class ItemDAO(BaseDAO):
    model = ItemDB
    
class ItemSketchDAO(BaseDAO):
    model = ItemSketchDB