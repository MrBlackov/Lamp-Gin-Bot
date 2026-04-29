from app.aio.inline_buttons.action import ActionIKB
from app.aio.msg.action import ActionText
from app.service.base import BaseService 
from app.interlayer.action import ActionLayer, actions, all_action
from app.exeption.action import SleepError, StopError
from app.aio.cls.fsm.utils import ActionFSM

class ActionService(BaseService):
    actions = actions
    all_actions = all_action

    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.layer = ActionLayer(tg_id)
        self.text = ActionText
        self.state = ActionFSM(state)
        self.IKB = ActionIKB(tg_id)
        
    @property
    def cmds_and_tags(self):
        cmds = {}
        for action in self.all_actions:
            for prefix, command_list in action.commands(True):
                cmds[prefix+command_list] = action.tag
        return cmds
   
    async def get_actions(self, is_details: bool = True):
        try:
            await self.layer.actions()
            return '🎮 Что будем делать?', self.IKB.actions({a.tag:[a.emodzi, a.name] for a in self.actions}, is_details)
        except SleepError as e:
            return e.msg, self.IKB.wake_up()
        except StopError as e:
            return e.msg, self.IKB.stop()
    
    async def to_action(self, tag: str):
        try:
            action = await self.layer.action(tag)
            char_name = action.char.exist.full_name
            emodzi = action.emodzi
            msg_format = {
                'char_name': char_name,
                'emodzi': emodzi
            }
            msg = action.msg.format(**msg_format)
            match action.result:
                case 'is_sleep' | 'to_sleep':
                    return msg, self.IKB.wake_up()
                case 'wake_up' | 'no_sleep' | 'stop' | 'no_action':
                    return msg, self.IKB.back('actions')   
                case 'is_action' | 'to_action':
                    return msg, self.IKB.stop()
        except SleepError as e:
            return e.msg, self.IKB.wake_up()
        except StopError as e:
            return e.msg, self.IKB.stop()

    async def cmd_action(self, cmd: str):
        cmds = self.cmds_and_tags
        return await self.to_action(cmds.get(cmd))