from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from app.aio.cls.callback.kit import KitBackCall, KitIdCall, KitActionCall
from app.db.models.item import KitDB, KitSketchDB

class KitIKB(BotIKB):
    def back(self, where: str):
        self.builder.button(text='↩️ Назад', callback_data=KitBackCall(where=where))
        return self.builder.adjust(1).as_markup()
    
    def my_kits(self, kits: list[KitDB] | None, no_hide: list[KitSketchDB] | None):
        if kits:
            for kit in kits:
                self.builder.button(text='🟢 ' + kit.sketch.name, callback_data=KitIdCall(kit_id=kit.id))
        if no_hide:
            for kit in no_hide:
                self.builder.button(text='🆕 ' + kit.name, callback_data=KitIdCall(kit_id=kit.id, is_new=True))   
        self.builder.button(text='✒️ Ввести промокод', callback_data=KitActionCall(to_enter_code=True))
        return self.builder.adjust(1).as_markup()

    def kit(self, kit_id: int, where: str):
        self.builder.button(text='↩️ Назад', callback_data=KitBackCall(where=where))
        self.builder.button(text='📟 Использовать', callback_data=KitActionCall(kit_id=kit_id, to_get_kit=True))
        return self.builder.adjust(2).as_markup()

    def newkit(self, kit_id: int, where: str):
        self.builder.button(text='💾 Сохранить', callback_data=KitActionCall(kit_id=kit_id, to_save=True))
        self.builder.button(text='📟 Использовать', callback_data=KitActionCall(kit_id=kit_id, to_get_kit=True))
        self.builder.button(text='↩️ Назад', callback_data=KitBackCall(where=where))
        return self.builder.adjust(2).as_markup()

