from app.db.models.char import CharacterDB
from app.db.dao.base import BaseDAO

class CharacterDAO(BaseDAO):
    model = CharacterDB

