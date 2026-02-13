from enum import Enum

class ItemTransferStatusEnum(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    REJECTED = 'rejected'

class ItemTransferType(str, Enum):
    TRADE = 'trade'
