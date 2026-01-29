from app.db.dao.base import BaseDAO
from app.db.models.transfer import TransferDB

class TransferDAO(BaseDAO):
    model = TransferDB


