from app.db.models.transfer import TransferDB, ItemDB
from enum import Enum

class TransferStatus:
    def __init__(self, name: str, level: int, emodzi: str, text: str):
        self.name = name
        self.level = level
        self.emodzi = emodzi
        self._text = text

    @property
    def text(self):
        return self.emodzi + ' ' + self._text

class MyTransfers:
    def __init__(self, 
                 from_me: list[TransferDB] | None = None, 
                 to_me: list[TransferDB] | None = None, 
                 from_me_items: list[ItemDB] | None = None, 
                 to_me_items: list[ItemDB] | None = None):
        self.from_me: list[TransferDB] | None = from_me
        self.to_me: list[TransferDB] | None = [ t for t in to_me if t.status != 'created'] if to_me else []
        self.from_me_items: list[ItemDB] | None = from_me_items
        self.to_me_items: list[ItemDB] | None = to_me_items

    @property
    def quantity(self):
        return len(self.from_me) + len(self.to_me)

    @property
    def all(self):
        return self.from_me + self.to_me

    @property
    def all_for_id(self) -> dict[int, TransferDB]:
        return {t.id:t for t in self.all}

    def get_status(self, name: str | Enum):
        if type(name) == Enum:
            name = name.value
        return {'confirmed':self.CONFIRMED,
                'completed':self.COMPLETED,
                'rejected':self.REJECTED, 
                'created':self.CREATED,
                'pending':self.CREATED,
                'received':self.RECEIVED,}[name]

    CONFIRMED = TransferStatus('confirmed', 1, '⌛', 'Сделки, ожидающие подтверждения')
    RECEIVED = TransferStatus('received', 1, '⌛', 'Полученные сделки')
    COMPLETED = TransferStatus('completed', 2, '✅', 'Завершенные сделки')
    REJECTED = TransferStatus('rejected', 3, '❌', 'Отклоненные сделки')
    CREATED = TransferStatus('created', 0, '📝', 'Черновики')
