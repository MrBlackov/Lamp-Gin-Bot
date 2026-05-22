from app.db.metods.gets import get_user_for_tg_id, get_users_for_ids, get_all_skills, get_user_setting_for_user_id, get_char_setting_for_char_id, get_action_states_for_exist_id, get_user_for_id, get_items_for_inventory, get_action_states_for_block_freedom, get_main_char_for_user_id, get_char_for_id, get_skills_for_attribute_point_id
from app.db.metods.unique import get_char_for_exist_id, ActionStateDB
from app.logged.infolog import infolog
from app.aio.config import admins, bot
from app.exeption.action import SleepError, StopError
from app.enum_type.tags import ActionTags, SkillTags
from app.service.utils import to_msg
from app.logic.actions import RecoveryAction, ActionSelf
from app.logic.settings import SettingSelf

class BaseLayer:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.logic = None
        self.bot = bot

    async def get_char_info(self, user_id: int | None = None, and_char: bool = True, **kwargs):
        self.user = await self.get_user_full_info(user_id)
        if and_char:
            self.char_id = await get_main_char_for_user_id(self.user.id, **kwargs)
            self.char = await self.get_char_full_info(self.char_id, **kwargs)
        return self
    
    async def get_user_full_info(self, user_id: int | None = None, and_setting: bool = True, and_frinends: bool = True, **kwargs):
        if user_id:
            user = await get_user_for_id(user_id)
        else:
            user = await get_user_for_tg_id(self.tg_id, True)
        if and_setting:
            setting = await get_user_setting_for_user_id(user.id)
            user.add_setting(setting, [a(setting) for a in SettingSelf.all_parameters if setting])
        if and_frinends:
            friends = (await get_users_for_ids(ids=user.friend_ids)) if user.friend_ids and len(user.friend_ids) > 0 else []
            user.add_friends(friends)
        return user

    async def get_char_full_info(self, char_id: int, and_skills: bool = True, and_items: bool = True, and_action: bool = True, and_setting: bool = True, and_recovery: bool = True, **kwargs):
        char = await get_char_for_id(char_id)
        if and_skills:
            skills = await get_skills_for_attribute_point_id(char.exist.attibute_point.id)
            char.exist.attibute_point.add_skills(skills)
        if and_items:
            items = await get_items_for_inventory(char.exist.inventory.id)
            char.exist.inventory.add_items(items)
        if and_action:
            action_states = await get_action_states_for_exist_id(char.exist.id)
            char.exist.add_action_state(action_states)
        if and_setting:
            setting = await get_char_setting_for_char_id(char_id)
            char.add_setting(setting, [a(setting) for a in SettingSelf.all_parameters if setting])
        if and_recovery:
            await RecoveryAction(char, action_tags=ActionSelf.action_tags).to_action()
        return char

    async def get_char_info_for_exist_id(self, exist_id: int):
        self.char = await get_char_for_exist_id(exist_id=exist_id)
        self.user = await self.get_user_full_info(self.char.user_id, and_frinends=False)
        self.char = await self.get_char_full_info(self.char.id, and_recovery=False)
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

    async def all_skills(self, is_hide: bool | None = False):
        return await get_all_skills(is_hide) 
