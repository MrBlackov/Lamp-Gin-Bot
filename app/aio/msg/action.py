from app.aio.msg.utils import TextHTML
from app.db.models.item import SkillDB

class ActionText:
    def actions(energy: int):
        return f'🎮 Что будем делать? [{TextHTML.float_format(energy, 7)} ⚡]'
    
    

