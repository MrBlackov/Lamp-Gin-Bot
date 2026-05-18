from app.logic.actions.base import (ActionBase, 
                                    ActionTags, 
                                    ItemSketchDB,
                                    ItemDB,
                                    SkillTags, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    get_item_for_tag,
                                    get_item_sketch_for_action_tag,
                                    action_point,
                                    TextHTML)
from app.logic.dnd import dices, dice
from app.exeption.action import DiceCmdNoValideError, DiceCmdDontHaveDError, DiceCmdLongError

class DiceAction(ActionBase):
    tag = ActionTags.dice
    spending_time = 0.2
    is_have_items = True

    name = 'Кинуть кубик'
    emodzi = '🎲'
    description = 'Исполняет dice-команды.'

    to_cmd = True
    commands_text = ['кость', 'dice']

    @classmethod
    def have_items(self):
        return [self.tag]

    async def to_action(self):
        if self.args and 'd' not in self.args:
            raise DiceCmdDontHaveDError(f'This dice-cmd dont have "d"')
        try:
            if self.args:
                result = dices().roll_dice(self.args)
                self.msg = f'🎲 {result.d_text}: {list(result.throw)} + {int(result.mod)} = {int(result.result)}'
                self.result = 'dice'
            else:
                self.result = 'to_dice'
                self.msg = '✏️ Отправьте dice-команду для выполнения' 
            if len(self.msg) > 4000:
                raise DiceCmdLongError('This dice-result too long')
            return self
        except ValueError as e:
            raise DiceCmdNoValideError(f'This dice-cmd dont valid')



