from app.aio.inline_buttons.action import ActionIKB
from app.aio.msg.action import ActionText
from app.service.base import BaseService 
from app.interlayer.action import ActionLayer, ActionSelf
from app.exeption.action import SleepError, StopError
from app.aio.cls.fsm.utils import ActionFSM
from app.aio.cls.fsm.action import ActionState
from app.exeption.action import ActionError

class ActionService(BaseService):
    actions = ActionSelf

    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.layer = ActionLayer(tg_id)
        self.text = ActionText
        self.state = ActionFSM(state)
        self.IKB = ActionIKB(tg_id)
        
    @property
    def cmds_and_tags(self):
        cmds = {}
        for action in self.actions.cmd_actions:
            for prefix, command_list in action.commands(True):
                cmds[prefix+command_list] = action.tag
        return cmds
   
    async def get_actions(self, is_details: bool = True):
        try:
            energy = await self.layer.actions()
            return self.text.actions(energy.coins), self.IKB.actions({a.tag:[a.emodzi, a.name] for a in self.actions.IKB_actions}, is_details)
        except SleepError as e:
            return e.msg, self.IKB.wake_up()
        except StopError as e:
            return e.msg, self.IKB.stop()
    
    async def to_action(self, tag: str, step: int = 1, minute: int | None = None):
        try:
            action = await self.layer.action(tag, step, minute)
            emodzi = action.emodzi
            result = action.result
            msg_format = {
                'char_name': action.char.exist.full_name,
                'emodzi': emodzi,
                **action.msg_kwargs
            }
            msg = action.msg.format(**msg_format)
            match result:
                case 'is_sleep' | 'to_sleep':
                    return msg, self.IKB.wake_up()
                case 'wake_up' | 'no_sleep' | 'stop' | 'no_action' | 'recovery' | 'no_lookaround':
                    return msg, self.IKB.back('actions')   
                case 'is_action' | 'to_action':
                    return msg, self.IKB.stop()     
                case 'stats':
                    return msg, self.IKB.stats()    
                case 'lookaround':
                    return msg, self.IKB.lookaround(action.results)  
                case 'to_action_time':
                    return msg, self.IKB.time_action(tag=tag, minute=action.minute, emodzi=emodzi, action_text=action.name, where='actions')
        except SleepError as e:
            return e.msg, self.IKB.wake_up()
        except StopError as e:
            return e.msg, self.IKB.stop()

    async def cmd_action(self, cmd: str, minute: str | None =  None):
        cmds = self.cmds_and_tags
        return await self.to_action(cmds.get(cmd), minute=int(minute) if minute else None)
    
    async def to_time_redact(self, tag: str, msg):
        await self.state.update_data(tag=tag, msg=msg)
        await self.state.set_state(ActionState.minute)
        return '✒️ Введите время в минутах', self.IKB.back('action')

    async def back_action(self, tag: str):
        tag = await self.state.get_value('tag')
        return await self.to_action(tag)
    
    async def time_redact(self, minute: str):
        tag = await self.state.get_value('tag')
        return await self.to_action(tag, minute=int(minute))
        
    async def to_stats(self, tag: str):
        return await self.to_action(tag)
