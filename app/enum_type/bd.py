from enum import Enum

class TgType(Enum):
    PRIVATE = 'PRIVATE'
    SUPERGROUP = 'SUPERGROUP'    
    GROUP = 'GROUP'    
    CHANNEL = 'CHANNEL'

class WorkType(Enum):
    BAN = 'BAN'
    LIMITED = 'LIMITED'
    MAIN = 'MAIN'
    LOG = 'LOG'
    TESTED = 'TESTED'
    USUAL = 'USUAL'