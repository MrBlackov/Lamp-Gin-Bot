from app.aio.cls.callback.social import SocialBackCall, SocialActionCall, SocialFriendCall, SocialRequestCall
from app.aio.cls.callback.faq import FAQCall
from app.aio.inline_buttons.base import BotIKB
from app.logged.botlog import logs
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton
from app.aio.msg.utils import TextHTML
from app.db.models.main import UserDB

class SocialIKB(BotIKB):
    def back(self, where: str):
        return self.builder.button(text='↩️ Назад', callback_data=SocialBackCall(where=where, tg_id=self.tg_id)).as_markup()

    def friends(self, users: list[UserDB]):
        for u in users:
            self.builder.button(text=f'💠 {u.tg_user.fullname}', callback_data=SocialFriendCall(user_id=u.id, to_info=True, tg_id=self.tg_id))
        self.builder.button(text='➕ Добавить друга', callback_data=SocialActionCall(to_send_request=True, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def friend(self, user_id: int, where: str):               
        self.builder.button(text='❌ Перестать дружить', callback_data=SocialFriendCall(user_id=user_id, to_delete=True, tg_id=self.tg_id))        
        self.builder.button(text='↩️ Назад', callback_data=SocialBackCall(where=where, type=type, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def request(self, user_id: int):
        self.builder.button(text='❌ Отклонить', callback_data=SocialRequestCall(status='decline', user_id=user_id, tg_id=self.tg_id))
        self.builder.button(text='✅ Принять', callback_data=SocialRequestCall(status='accert', user_id=user_id, tg_id=self.tg_id))
        return self.builder.adjust(2).as_markup()


