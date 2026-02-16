from enum import Enum


class ItemTransferStatusEnum(str, Enum):
    CONFIRMED = 'confirmed'
    COMPLETED = 'completed'
    REJECTED = 'rejected'
    CREATED = 'created'


class ItemTransferType(str, Enum):
    TRADE = 'trade'
