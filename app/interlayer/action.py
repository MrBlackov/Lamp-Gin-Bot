from app.interlayer.base import BaseLayer
from app.logic.action import ActionLogic, actions, all_action
from app.db.metods.gets import get_skills_for_attribute_point_id, get_skill_for_id, get_skill_for_sketch_id, get_skill_sketch_for_id, SkillDB, SkillSketchDB

class ActionLayer(BaseLayer):
    def __init__(self, tg_id):
        super().__init__(tg_id)
        self.logic = ActionLogic()

    async def actions(self):
        await self.get_char_info()
        await self.checking_freedom()
        return True

    async def action(self, tag: str):
        await self.get_char_info()
        await self.checking_freedom(tag)
        return await self.logic.action(self.char, tag)

