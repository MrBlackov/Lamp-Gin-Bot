from app.aio.msg.utils import TextHTML
from app.db.models.item import SkillDB

class ActionText:
    def actions(energy: int):
        return f'🎮 Что будем делать? [{str(energy)[:7]} ⚡]'
    
    

