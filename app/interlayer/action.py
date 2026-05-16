from app.interlayer.base import BaseLayer
from app.logic.action import ActionLogic, ActionSelf
from app.db.metods.gets import get_action_states, ActionStateDB
from app.db.metods.unique import get_action_states_for_datetime
from app.db.metods.updates import update_action_state_for_id
import asyncio
from app.logged.botlog import log
from datetime import datetime

class ActionLayer(BaseLayer):
    def __init__(self, tg_id):
        super().__init__(tg_id)
        self.logic = ActionLogic()

    async def actions(self):
        await self.get_char_info()
        await self.checking_freedom()
        return self.energy

    async def action(self, tag: str, step: int = 1, minute: int | None = None, **kwargs):
        await self.get_char_info()
        await self.checking_freedom(tag)
        kwargs = await self.get_info_for_action(**kwargs)
        return await self.logic.action(self.char, self.user, tag, step, minute, **kwargs)

    async def get_info_for_action(self, **kwargs):
        match kwargs:
            case {'purpose_char_id':None}:
                return kwargs
            case {'purpose_char_id':char_id}:
                purpose_char = await self.get_char_full_info(char_id, False, False, False, True, False)
                purpose_user = await self.get_user_full_info(purpose_char.user_id, False)
                return kwargs | {'purpose_char':purpose_char, 'purpose_user':purpose_user}
            case _:
                return kwargs

    @log.decor()
    async def check_action(self, action_state: ActionStateDB):
        try:
            await self.get_char_info_for_exist_id(action_state.exist_id)
            action = ActionSelf.action_tags.get(action_state.tag)
            result = await action(char=self.char, action_tags=ActionSelf.tags).to_state_action(action_state)
            if result.msg:
                await self.bot.send_message(self.user.tg_id, result.msg.format(emodzi=result.emodzi, name=result.name.lower(), char_name=self.char.exist.full_name))
                print(result.msg.format(emodzi=result.emodzi, char_name=self.char.exist.full_name))
            else:
                print(f'{result.emodzi} {self.char.exist.full_name} {result.action_text}')
            if result.new_action_state:
                new_action_state = result.new_action_state.to_dict
                new_action_state.pop('exist')
                action_state = await update_action_state_for_id(result.new_action_state.id, new_action_state)
        except Exception as e:
            log.warning(f'CheckAction, char_id: {self.char.exist.id}, action_state_id: {action_state.id}, error: {e}')
            return True

    async def state_checker(self):
        while True:
            try:
                action_states = await get_action_states_for_datetime(is_start=True, time=datetime.now())
                results = await asyncio.gather(*[ActionLayer(0).check_action(action_state) for action_state in action_states], return_exceptions=True)
            except Exception as e:
                print('ActionStatesRunner: ', e)
                return True
            finally:
                await asyncio.sleep(60)