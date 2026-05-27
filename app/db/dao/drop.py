from app.db.models.drop import DropDB
from app.db.dao.base import BaseDAO

class DropDAO(BaseDAO):
    model = DropDB


