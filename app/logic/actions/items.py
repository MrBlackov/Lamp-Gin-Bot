from app.logic.actions.base import (ActionBase, 
                                    ActionTags, 
                                    ItemSketchDB,
                                    ItemDB,
                                    SkillTags, 
                                    add_db_obj, 
                                    ActionStateDB, 
                                    delete_action_state, 
                                    get_action_state_for_tag,
                                    get_action_states_for_tag,
                                    update_action_state_for_id,
                                    update_item_for_id,
                                    get_chars_for_exist_id,
                                    update_exist_for_id,
                                    action_point,
                                    TextHTML,
                                    infolog)
from app.logic.dnd import dices, dice
from app.exeption.action import DiceCmdNoValideError, NameLongError, BookDontHaveInfoError, BookSettingCloseError, DiceCmdDontHaveDError, DiceCmdLongError, PaperLongError
from app.validate.item import BookValide

class ItemsAction(ActionBase):
    to_IKB = False
    to_cmd = False
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
        self.check_have_item()
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

    @classmethod
    def have_items(self):
        return [self.tag]

    async def to_action(self):
        self.check_have_item()
        paper = self.char.exist.inventory.item_ids.get(self.item_id)
        is_escape = self.kwargs.get('is_escape')
        if self.step == 2:
            self.result = 'redact_paper'
            self.msg = '✏️ Отправьте новую надпись. Вы можете использовать форматирование текста. Максимум 2000 символов.'
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
        self.msg = TextHTML(f'📄 Надпись (отсуствует)' if type(text) != str else f'📄 Надпись \n\n' + text).replace('emoji_id', 'emoji-id')
        self.msg = self.msg.escape() if is_escape else self.msg
        self.is_escape = is_escape
        return self

class BookAction(ItemsAction):
    tag = ActionTags.book

    name = 'Открыть книгу'
    emodzi = '📖'

    @classmethod
    def have_items(self):
        return [self.tag]

    def __init__(self, char, user = None, step = 1, minute = None, action_tags = ..., **kwargs):
        super().__init__(char, user, step, minute, action_tags, **kwargs)
        self.page: int = kwargs.get('page', 0)

    async def to_action(self):
        self.check_have_item()
        book = self.char.exist.inventory.item_ids.get(self.item_id)
        book_info = BookValide.model_validate(book.nbt.get('book')) if book.nbt.get('book') else None
        self.book_info = book_info
        self.result = 'book_page'
        self.max_page = len(book_info.pages)
        self.pages = [TextHTML(book_info.pages[s][:20]).strip_html() for s in range(self.max_page)]
        if book_info and self.step == 1 and len(book_info.pages) > 0:
            self.msg = book_info.pages[self.page].replace('emoji_id', 'emoji-id')
        elif book_info and self.step == 2:
            self.result = 'book_pages'
            self.msg = '📃 Выберете страницу'
        elif book_info and self.step == 3:
            self.result = 'new_book_page'
            self.msg = '✏️ Введите текст для новой страницы, можете использовать форматирование текста или кастомные эмодзи. Максимум 2000 символов.'
        elif book_info and self.step == 4:
            if book_info == None:
                raise BookDontHaveInfoError('This book dont have info')
            if len(self.args) > 2000:
                raise PaperLongError('This paper too long')
            book_info.pages.insert(self.page+1, self.args)
            book = await update_item_for_id(book.id, {'nbt': book.nbt | {'book': book_info.model_dump()}})
            self.msg = book_info.pages[self.page].replace('emoji_id', 'emoji-id')
        elif book_info and self.step == 5:
            if book_info == None:
                raise BookDontHaveInfoError('This book dont have info')
            book_info.pages.pop(self.page)
            book = await update_item_for_id(book.id, {'nbt': book.nbt | {'book': book_info.model_dump()}})
            self.msg = book_info.pages[self.page].replace('emoji_id', 'emoji-id')
        else:
            self.msg = '📃 Страниц пока нету'
        return self
    
class BookSettingAction(ItemsAction):
    tag = ActionTags.book_setting

    name = 'Настройки книги'
    emodzi = '⚙️'

    @classmethod
    def have_items(self):
        return [self.tag]
    
    async def to_action(self):
        self.check_have_item()
        book = self.char.exist.inventory.item_ids.get(self.item_id)
        book_info = BookValide.model_validate(book.nbt.get('book')) if book.nbt.get('book') else None
        self.book_info = book_info
        self.is_close_setting = book_info.is_close_setting if book_info else False
        if book_info:
            if self.char.id != book_info.author_char_id and book_info.is_close_setting:
                raise BookSettingCloseError('This book is close setting')
        if (book_info == None or self.step == 0) and self.step != -1:
            self.msg = '✏️ Введите название книги'
            self.result = 'new_book'
            self.step = 0
            return self
        elif self.step == 2:
            self.msg = '✏️ Введите ваш псевдоним'
            self.result = 'book_author_name'
            return self
        elif self.step == 3:
            self.msg = '✏️ Введите описание книги'
            self.result = 'book_description'
            return self
        elif self.step == 5:
            self.msg = '🗑️ Книга очищена'
            self.result = 'book_delete'          
            book.nbt.pop('book')
            book = await update_item_for_id(self.item_id, {'nbt': book.nbt})
            return self
        elif self.step == 4:
            book = await update_item_for_id(self.item_id, {'nbt': book.nbt | {'book':book_info.model_dump() | {'is_close_setting':not book_info.is_close_setting}}})
        elif self.step == -1:
            book = await update_item_for_id(self.item_id, {'nbt': book.nbt | {'book':(BookValide(
                name=self.args, 
                author=self.char.exist.full_name,
                author_char_id=self.char.id).model_dump() if book_info == None else book_info.model_dump() | {'name':self.args})}})
        elif self.step == -2:
            book = await update_item_for_id(self.item_id, {'nbt': book.nbt | {'book':book_info.model_dump() | {'author':self.args}}})
        elif self.step == -3:
            book = await update_item_for_id(self.item_id, {'nbt': book.nbt | {'book':book_info.model_dump() | {'description':self.args}}})
        
        book_info = BookValide.model_validate(book.nbt.get('book')) if book.nbt.get('book') else None

        self.result = 'book_setting'
        self.msg = f'🏷️ {book_info.name}' + TextHTML('\n'.join([
                        f'👤 Автор: {book_info.author}',
                        f'✏️ Можно редактировать: {'✅' if not book_info.is_close_setting else '❌'}',
                        (f'📊 Кол-во страниц: {len(book_info.pages)}' if book_info.pages and len(book_info.pages) > 0 else '❌ Страниц нету'),
                        f'📜 Описание: {book_info.description if book_info.description and len(book_info.description) > 0 else "❌"}'
                    ])).blockquote()
        return self


class RadioAction(ItemsAction):
    tag = ActionTags.radio

    name = 'Настройки рации'
    emodzi = '📻'
    action_text = 'слушает'

    to_cmd = True
    commands_text = ['рация', 'radio']
    default_nbt = {'kanal':'y'}

    @classmethod
    def have_items(self):
        return [self.tag]

    def __init__(self, char, user = None, step = 1, minute = None, action_tags = ..., **kwargs):
        super().__init__(char, user, step, minute, action_tags, **kwargs)
        self.micro: bool = kwargs.get('micro', self.state == 'ActionState:micro')
        self.swoo: bool = kwargs.get('swoo', False)
        self.radio_kanals = ['y', 'r', 'b', 'g']
        self.radio_kanals_dict = {
            'y':'1к.',
            'r':'2к.',
            'b':'3к.',
            'g':'4к.',
            None:'Выкл.',
        }

    async def to_action(self):
        self.check_have_item()
        radio_state = await get_action_state_for_tag(self.tag, self.char.exist.id)
        self.radio_kanal = radio_state.nbt.get('kanal') if radio_state else None
        if self.step == 0 and radio_state:
            return await self.use_micro()
        if radio_state:
            self.swoo = True
        if self.step == 3 and radio_state == None:
            radio_state = (await add_db_obj(data=[ActionStateDB(tag=self.tag, level=self.default_level, is_block_freedom=self.is_block_freedom, reset=self.default_reset, start=self.start, end=self.end, nbt=self.default_nbt, exist_id=self.char.exist.id)]))[0]
            self.radio_kanal = radio_state.nbt.get('kanal', self.radio_kanal) if radio_state else self.radio_kanal
            self.swoo = True
        elif self.step == 3 and radio_state:
            is_stop = await delete_action_state(id=radio_state.id)
            self.radio_kanal = None
            self.swoo = False
            self.micro = False
        if self.step == 2:
            self.micro = not self.micro
        if self.step == 4 and self.radio_kanal:
            i_kanal = self.radio_kanals.index(self.radio_kanal)
            new_radio_kanal = self.radio_kanals[i_kanal + 1] if i_kanal < len(self.radio_kanals) - 1 else self.radio_kanals[0]
            radio_state = await update_action_state_for_id(radio_state.id, new_data={'nbt':radio_state.nbt | {'kanal':new_radio_kanal}})
            self.radio_kanal = radio_state.nbt.get('kanal', self.radio_kanal) if radio_state else self.radio_kanal

        self.result = 'radio'
        self.msg = self.emodzi + f' Рация ({self.radio_kanals_dict.get(self.radio_kanal)})'
        return self
    
    async def use_micro(self):
        if len(self.args) > 200:
            self.args = self.args[:200]
            is_long = True
        else:
            is_long = False
        radio_states = await get_action_states_for_tag(self.tag)
        radio_chars = await get_chars_for_exist_id(exist_ids=[r.exist_id for r in radio_states if r.nbt.get('kanal') == self.radio_kanal])
        self.purpose_msg = f'📻 [{self.radio_kanals_dict.get(self.radio_kanal)}]: {self.args}'
        self.msg = f'Вы 📻 [{self.radio_kanals_dict.get(self.radio_kanal)}]: {self.args}' +  (' \n\n❗ Сообщение большое, оно было обрезано' if is_long else '')
        self.result = 'use_micro'
        self.purpose_tg_ids = [c.user.tg_id for c in radio_chars if self.char.user.id != c.user.id]
        await infolog.radio_msg(self.char.user.id, self.purpose_msg + f'\n\n {self.char.exist.full_name} (char_id={self.char.id}, user_id={self.char.user.id})')
        return self
  

class TagAction(ItemsAction):
    tag = ActionTags.tag

    name = 'Сменить имя персонажа'
    emodzi = '✏️'
    description = 'Меняет имя перса на желаемый.'

    @classmethod
    def have_items(self):
        return [self.tag]

    def __init__(self, char, user = None, step = 1, minute = None, action_tags = ..., **kwargs):
        super().__init__(char, user, step, minute, action_tags, **kwargs)
        self.names = self.args.split(' ', 1) if self.args else [None, None]
        self.first_name, self.last_name = self.names if len(self.names) > 1 else (self.names[0], None)
        self.full_name = f'{self.first_name} {self.last_name if self.last_name else ''}' if self.first_name else None

    async def to_action(self):
        self.check_have_item()
        tag = self.char.exist.inventory.item_ids.get(self.item_id)
        if self.first_name and len(self.first_name) > 50:
            raise NameLongError('Name is long')
        if self.last_name and len(self.last_name) > 50:
            raise NameLongError('Name is long')
        if self.step == 1:
            self.result = 'input_name'
            self.msg = '✏️ Введите новое имя и фамилию через пробел'
            return self
        if self.step == 2:
            self.result = 'rename_menu'
            self.msg = f'❔ Вы хотите поменять имя персонажа с {self.char.exist.full_name} на {self.full_name}' if self.full_name else '❌ Вы не ввели имя'
            return self
        print(self.first_name, self.last_name)
        exist = await update_exist_for_id(self.char.exist.id, {'first_name':self.first_name, 'last_name':self.last_name if self.last_name else ''})
        await self.pay_item_price({tag:1})
        self.result = 'rename'
        self.msg = f'✅ Персонаж переименован. Новое имя: {exist.full_name}'
        await infolog.char_rename(self.char.user.id, self.char.id, self.char.exist.full_name, exist.full_name)
        return self
        

