from app.db.dao.base import BaseDAO
from app.db.models.item import ItemDB, ItemSketchDB, KitDB, KitSketchDB, CraftDB

class ItemDAO(BaseDAO):
    model = ItemDB
    
class ItemSketchDAO(BaseDAO):
    model = ItemSketchDB


class KitDAO(BaseDAO):
    model = KitDB
    
class KitSketchDAO(BaseDAO):
    model = KitSketchDB

class CraftDAO(BaseDAO):
    model = CraftDB