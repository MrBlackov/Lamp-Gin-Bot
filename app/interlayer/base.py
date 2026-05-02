from app.db.metods.gets import get_user_for_tg_id, get_user_for_id, get_action_states_for_block_freedom, get_main_char_for_user_id, get_char_for_id, get_skills_for_attribute_point_id
from app.db.metods.unique import get_char_for_exist_id
from app.logged.infolog import infolog
from app.aio.config import admins, bot
from app.exeption.action import SleepError, StopError
from app.enum_type.tags import ActionTags, SkillTags
from app.service.utils import to_msg

class BaseLayer:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.logic = None
        self.bot = bot

    async def get_char_info(self, user_id: int | None = None):
        if user_id:
            self.user = await get_user_for_id(user_id)
        else:
            self.user = await get_user_for_tg_id(self.tg_id, True)
        self.char_id = await get_main_char_for_user_id(self.user.id)
        self.char = await get_char_for_id(self.char_id)
        skills = await get_skills_for_attribute_point_id(self.char.exist.attibute_point.id)
        self.char.exist.attibute_point.add_skills(skills)
        return self
    
    async def get_char_info_for_exist_id(self, exist_id: int):
        self.char = await get_char_for_exist_id(exist_id=exist_id)
        self.char_id = self.char.id
        self.user = await get_user_for_id(self.char.user_id)
        skills = await get_skills_for_attribute_point_id(self.char.exist.attibute_point.id)
        self.char.exist.attibute_point.add_skills(skills)
        return self
    
    @property
    def energy(self):
        return self.char.exist.attibute_point.skill_tags.get(SkillTags.energy)

    async def checking_freedom(self, tag: str | None = None):
        action_states = await get_action_states_for_block_freedom(is_block_freedom=True, exist_id=self.char.exist.id)
        if tag == ActionTags.stats or tag == ActionTags.stop or tag == ActionTags.wake_up or len(action_states) == 0:
            return True
        for action_state in action_states:
            if action_state.tag == ActionTags.sleep:
                raise SleepError(f'💤 Char sleep, user(id={self.user.id}, tg_id={self.user.tg_id})')
            elif action_state.is_block_freedom:
                raise StopError(f'❌ Char busy, user(id={self.user.id}, tg_id={self.user.tg_id})')
        return True

    def another(self, tg_id: int):
        self.tg_id = tg_id
        return self
