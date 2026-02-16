from app.db.models.base import UserDB, TgUserDB
from app.aio.msg.utils import TextHTML

class UserText:
    def __init__(self, tg_user: TgUserDB, user: UserDB):
        self.user = user
        self.tg_user = tg_user

    @property
    def text(self):
        return TextHTML(f'{self.tg_user.fullname}').href(f'tg://openmessage?user_id={self.user.tg_id}') + TextHTML('\n'.join([
            f'🔰 user_id: {self.user.id}',
            f'💠 tg_id: {self.user.tg_id}',
            f'📧 username: {self.tg_user.username if self.tg_user.username else "❌"}'
        ])).blockquote()
