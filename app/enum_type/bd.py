from enum import Enum

class TgType(Enum):
    PRIVATE = 'PRIVATE'
    SUPERGROUP = 'SUPERGROUP'    
    GROUP = 'GROUP'    
    CHANNEL = 'CHANNEL'

    def to_ru(self, type: 'TgType'):
        return {
            TgType.PRIVATE:"Личный",
            TgType.SUPERGROUP:"Супергруппа",
            TgType.GROUP:"Группа",
            TgType.CHANNEL:"Канал",
                }.get(type, 'Неизыестный тип')

class WorkType(Enum):
    BAN = 'BAN'
    LIMITED = 'LIMITED'
    MAIN = 'MAIN'
    LOG = 'LOG'
    TESTED = 'TESTED'
    USUAL = 'USUAL'