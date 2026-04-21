from app.aio.msg.utils import TextHTML
from app.db.models.item import SkillDB

class SkillText:
    def __init__(self, skills: list[SkillDB]):
        self.skills = skills
    
    def text_alert(skill: SkillDB):
        return skill.sketch.description or 'Описание отсутствует'
    
    @property
    def text(self):
        return '💡 Ваши навыки' + TextHTML.num_list([f'{skill.sketch.emodzi} {skill.sketch.name}: {str(skill.level)[:5]} ур.' for skill in self.skills]).blockquote()