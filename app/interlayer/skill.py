from app.interlayer.base import BaseLayer
from app.logic.skill import SkillLogic
from app.db.metods.gets import get_skills_for_attribute_point_id, get_skill_for_id, get_skill_for_sketch_id, get_skill_sketch_for_id, SkillDB, SkillSketchDB

class SkillLayer(BaseLayer):
    def __init__(self, tg_id):
        super().__init__(tg_id)
        self.logic = SkillLogic()

    async def get_my_skills(self, **kwargs):
        await self.get_char_info()
        return await self.logic.get_my_skills(self.char.exist.attibute_point.id, **kwargs)

    async def get_skill(self, skill_id: int):
        return await get_skill_for_id(skill_id)