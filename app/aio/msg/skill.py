from app.aio.msg.utils import TextHTML
from app.db.models.item import SkillDB, SkillSketchDB

class SkillText:
    def __init__(self, skills: list[SkillDB]):
        self.skills = skills
    
    def to_text(skill: SkillDB):
        return f'{skill.sketch.text} ({TextHTML.float_format(skill.level, 5)} ур.)' + TextHTML('\n'.join([
            f'🔰 Sketch ID: {skill.sketch.id}',
            f'🏷️ Тег: {skill.sketch.tag}',
            f'📜 Описание: {skill.sketch.description if skill.sketch.description else '❌'}',
        ])).blockquote()
    
    def to_sketch_text(sketch: SkillSketchDB):
        return f'{sketch.text}' + TextHTML('\n'.join([
            f'🔰 Sketch ID: {sketch.id}',
            f'🏷️ Тег: {sketch.tag}',
            f'📜 Описание: {sketch.description if sketch.description else '❌'}',
        ])).blockquote()

    @property
    def text(self):
        return '💡 Ваши навыки' + TextHTML.num_list([f'{skill.sketch.emodzi} {skill.sketch.name}: {str(skill.level)[:5]} ур.' for skill in self.skills]).blockquote() + '\n \n ❗ Чтобы получить информацию о навыке нажмите на нужную кнопку.'