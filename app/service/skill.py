from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.skill import SKillIKB
from app.enum_type.char import Gender
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.aio.msg.skill import TextHTML, SkillText
from app.service.base import BaseService 
from app.exeption import error_faq, BotError
from app.interlayer.skill import SkillLayer
from app.aio.cls.fsm.utils import SkillFSM

class SkillService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.layer = SkillLayer(tg_id)
        self.text = SkillText
        self.state = SkillFSM(state)
        self.IKB = SKillIKB(tg_id)

    async def get_my_skills(self):
        skills = await self.layer.get_my_skills()
        await self.state.update_data(all_skills=skills, skill_ids={s.id:s for s in skills})
        return '💡 Ваши навыки', self.IKB.skills(skills, page=0, max_page=1)
    
    async def get_all_skills(self):
        skills = await self.layer.get_all_skills()
        await self.state.update_data(all_skills=skills, skill_ids={s.id:s for s in skills})
        return '💡 Все навыки в боте', self.IKB.sketchs(skills, page=0, max_page=1)

    async def skill(self, skill_id: int):
        skill_ids = await self.state.get_value('skill_ids')
        if skill_ids == None:
            skill = await self.layer.get_skill(skill_id)
        else:
            skill = skill_ids.get(skill_id)
        return self.text.to_text(skill), self.IKB.skill(skill)


    async def sketch(self, sketch_id: int):
        skill_ids = await self.state.get_value('skill_ids')
        if skill_ids == None:
            skill = await self.layer.get_sketch(sketch_id)
        else:
            skill = skill_ids.get(sketch_id)
        return self.text.to_sketch_text(skill), self.IKB.back('sketchs')