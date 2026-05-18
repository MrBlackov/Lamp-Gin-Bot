from app.aio.inline_buttons.action import ActionIKB
from app.aio.msg.action import ActionText
from app.service.base import BaseService 
from app.interlayer.action import ActionLayer, ActionSelf
from app.exeption.action import SleepError, StopError
from app.aio.cls.fsm.utils import ActionFSM
from app.aio.cls.fsm.action import ActionState
from app.exeption.action import ActionError
from app.service.utils import is_natural_int

class ActionService(BaseService):
    actions = ActionSelf

    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
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
    
    async def to_action(self, tag: str, step: int = 1, minute: int | None = None, **kwargs):
        try:
            action = await self.layer.action(tag, step, minute, **kwargs)
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
                case 'wake_up' | 'no_sleep' | 'stop' | 'no_action' | 'recovery' | 'no_lookaround' | 'no_throw':
                    return msg, self.IKB.back('actions')  
                case 'to_throw':
                    await self.bot.send_message(action.purpose_user.tg_id, action.purpose_msg)
                    return msg, self.IKB.back('actions')    
                case 'is_action' | 'to_action':
                    return msg, self.IKB.stop()     
                case 'stats':
                    return msg, self.IKB.stats()       
                case 'paper':
                    return msg, self.IKB.redact_paper(action.item_id, action.is_have_text)   
                case 'redact_paper':
                    await self.state.set_state(ActionState.redact_paper)
                    await self.state.update_data(msg=self.message, item_id=action.item_id)
                    return msg, self.IKB.paper_back(action.item_id)   
                case 'lookaround':
                    return msg, self.IKB.lookaround(action.results)  
                case 'to_action_time':
                    return msg, self.IKB.redact(tag=tag, minute=action.minute, emodzi=emodzi, action_text=action.name, where='actions')
                case 'item_throw':
                    return msg, self.IKB.item_throw(action.char, action.kwargs, 'actions')
                case 'dice':
                    return msg, self.IKB.dice(action.kwargs)
                case 'to_dice':
                    await self.state.set_state(ActionState.dice_command)
                    await self.state.update_data(msg=self.message)
                    return msg, self.IKB.dice_command()
                case 'char_throw':
                    values_in_page = 10
                    char_pages = [tuple(action.chars[i:i+values_in_page]) for i in range(0, len(action.chars), values_in_page)]
                    await self.state.update_data(char_pages=char_pages, msg_text=msg, throw_kwargs=action.kwargs)
                    return msg + f'{f' [1/{len(char_pages)}стр]' if len(char_pages) > 1 else ''}', self.IKB.char_throw(char_pages[0], action.kwargs, page=0, max_page=len(char_pages), where='actions')
                case 'throw_menu':
                    return msg, self.IKB.throw_menu(action.kwargs, 'actions')
                case _:
                    return '💻 Скоро', self.IKB.back('actions')
        except SleepError as e:
            return e.msg, self.IKB.wake_up()
        except StopError as e:
            return e.msg, self.IKB.stop()

    async def cmd_action(self, cmd: str, minute: str | None =  None, args: str | None =  None, **kwargs):
        cmds = self.cmds_and_tags
        return await self.to_action(cmds.get(cmd), minute=int(minute) if minute and minute.isdigit() else None, args=args, kwargs=kwargs)
    
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
 
    async def del_timer(self, tag: str):
        await self.state.update_data(tag=tag)
        return await self.time_redact(-1)
   
    async def to_throw_quantity(self, msg, **kwargs: dict):
        await self.state.update_data(throw_kwargs=kwargs, msg=msg)
        await self.state.set_state(ActionState.throw_quantity)
        return '✏️ Отправьте количество, которое хотите бросить', self.IKB.back('throw_menu')

    async def throw_quantity(self, quantity: str):
        kwargs = await self.state.get_value('throw_kwargs')
        quantity = is_natural_int(quantity)
        return await self.to_action('throw', **(kwargs | {'quantity':quantity}))

    async def char_throw(self, page: int):
        char_pages = await self.state.get_value('char_pages')
        msg_text = await self.state.get_value('msg_text')
        throw_kwargs = await self.state.get_value('throw_kwargs')
        return msg_text + f'{f' [{page + 1}/{len(char_pages)}стр]' if len(char_pages) > 1 else ''}', self.IKB.char_throw(char_pages[page], throw_kwargs, page=page, max_page=len(char_pages), where='actions')

    async def dice_command(self, cmd: str):
        return await self.to_action('dice', args=cmd)
 
    async def redact_paper(self, text: str):
        item_id = await self.state.get_value('item_id')
        return await self.to_action('paper', step=3, item_id=item_id, args=text)
