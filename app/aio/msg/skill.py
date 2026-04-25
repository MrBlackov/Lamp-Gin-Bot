from app.aio.msg.utils import TextHTML
from app.db.models.item import SkillDB

class SkillText:
    def __init__(self, skills: list[SkillDB]):
        self.skills = skills
    
    def text_alert(skill: SkillDB):
        return f'{skill.sketch.emodzi} {skill.sketch.name}\n\n' + skill.sketch.description if skill.sketch.description else f'{skill.sketch.emodzi} {skill.sketch.name}\n\n'
    
    @property
    def text(self):
        return '💡 Ваши навыки' + TextHTML.num_list([f'{skill.sketch.emodzi} {skill.sketch.name}: {str(skill.level)[:5]} ур.' for skill in self.skills]).blockquote() + '\n \n ❗ Чтобы получить информацию о навыке нажмите на нужную кнопку.'