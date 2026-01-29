from app.db.models.char import CharacterDB, ExistenceDB, InventoryDB, AttributePointDB
from app.db.dao.base import BaseDAO

class CharacterDAO(BaseDAO):
    model = CharacterDB

class ExistenceDAO(BaseDAO):
    model = ExistenceDB

class InventoryDAO(BaseDAO):
    model = InventoryDB

class AttributePointDAO(BaseDAO):
    model = AttributePointDB