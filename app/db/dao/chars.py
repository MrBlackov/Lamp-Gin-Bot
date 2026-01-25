from app.db.models.char import CharacterDB, SavingDB, ExistenceDB, InventoryDB, AttributePointDB
from app.db.dao.base import BaseDAO

class CharacterDAO(BaseDAO):
    model = CharacterDB

class SavingDAO(BaseDAO):
    model = SavingDB

class ExistenceDAO(BaseDAO):
    model = ExistenceDB

class InventoryDAO(BaseDAO):
    model = InventoryDB

class AttributePointDAO(BaseDAO):
    model = AttributePointDB