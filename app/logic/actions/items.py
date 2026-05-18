from app.logic.actions.base import (ActionBase, 
                                    ActionTags, 
                                    ItemSketchDB,
                                    ItemDB,
                                    SkillTags, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    update_item_for_id,
                                    get_item_sketch_for_action_tag,
                                    action_point,
                                    TextHTML)
from app.logic.dnd import dices, dice
from app.exeption.action import DiceCmdNoValideError, DiceCmdDontHaveDError, DiceCmdLongError, PaperLongError

class ItemsAction(ActionBase):
    to_IKB = False
    is_have_items = True

class DiceAction(ItemsAction):
    tag = ActionTags.dice

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

class PaperAction(ItemsAction):
    tag = ActionTags.paper

    name = 'Изменить надпись'
    emodzi = '✏️'
    commands_text = ['кость', 'dice']

    @classmethod
    def have_items(self):
        return [self.tag]

    async def to_action(self):
        paper = self.char.exist.inventory.item_ids.get(self.item_id)
        if self.step == 2:
            self.result = 'redact_paper'
            self.msg = '✏️ Отправьте новую надпись. Вы можете использовать HTML-разметку текста'
            return self
        elif self.step == 3:
            if len(self.args) > 2000:
                raise PaperLongError('This paper too long')
            paper = await update_item_for_id(paper.id, {'nbt': paper.nbt | {'text': self.args}})
        elif self.step == 4:
            if 'text' in paper.nbt:
                paper.nbt.pop('text')
            paper = await update_item_for_id(paper.id, {'nbt': paper.nbt})
        self.result = 'paper'
        text = paper.nbt.get('text')
        self.is_have_text = type(text) == str
        self.msg = TextHTML(f'📄 Надпись (отсуствует)' if type(text) != str else f'📄 Надпись \n\n' + text).escape()
        return self




