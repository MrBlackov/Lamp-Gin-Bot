from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.enum_type.item import ItemType
from app.aio.cls.callback.item import AddItemBackCall, AddItemTypeCall, AddItemMisskCall, AddItemToCreate

class AddItemIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=AddItemBackCall(where=where))

    def to_type(self, where: str = 'name'):
        for t in ItemType:
            self.builder.button(text=t.to_str(), callback_data=AddItemTypeCall(type=t.value))
        self.back(where)
        return self.builder.adjust(1).as_markup()
    
    def to_miss(self, back_where: str, next_where: str | None = None):
        if next_where:
            self.builder.button(text='❌ Пропустить', callback_data=AddItemMisskCall(where=next_where))
        return self.builder.adjust(1).as_markup()

    def to_back(self, where: str):
        self.back(where)
        return self.builder.adjust(1).as_markup()
    
    def to_check(self, where: str):
        self.builder.button(text='✅ Создать', callback_data=AddItemToCreate())
        self.back(where)
        return self.builder.adjust(1).as_markup()
        
        