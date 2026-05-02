from app.interlayer.base import BaseLayer
from app.logic.action import ActionLogic, ActionSelf
from app.db.metods.gets import get_action_states, ActionStateDB
from app.db.metods.unique import get_action_states_for_datetime
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

    async def action(self, tag: str, step: int = 1, minute: int | None = None):
        await self.get_char_info()
        await self.checking_freedom(tag)
        return await self.logic.action(self.char, tag, step, minute)

    async def check_action(self, action_state: ActionStateDB):
        try:
            await self.get_char_info_for_exist_id(action_state.exist_id)
            await ActionSelf.action_tags.get(ActionSelf.tags.recovery   )(self.char, action_tags=ActionSelf.tags).to_action()
            action = ActionSelf.action_tags.get(action_state.tag)
            result = await action(char=self.char, action_tags=ActionSelf.tags).to_state_action(action_state)
            if result.msg:
                await self.bot.send_message(self.user.tg_id, result.msg.format(emodzi=result.emodzi, name=result.name, char_name=self.char.exist.full_name))
                print(result.msg.format(emodzi=result.emodzi, char_name=self.char.exist.full_name))
            else:
                print(f'{result.emodzi} {self.char.exist.full_name} {result.action_text}')
        except Exception as e:
            log.warning(f'CheckAction: {e}')
            return True

    async def state_checker(self):
        while True:
            try:
                action_states = await get_action_states_for_datetime(is_start=True, time=datetime.now())
                results = await asyncio.gather(*[self.check_action(action_state) for action_state in action_states], return_exceptions=True)
            except Exception as e:
                print('ActionStatesRunner: ', e)
                return True
            finally:
                await asyncio.sleep(60)