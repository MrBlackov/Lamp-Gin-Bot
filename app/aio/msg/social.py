from app.aio.msg.utils import TextHTML
from app.db.models.main import UserDB

class SocialText:
    def send(user: UserDB):
        return f'✅ Запрос дружбы игроку {TextHTML(user.tg_user.fullname).openmessage(user.tg_id)} отправлен'

    def request(user: UserDB):
        return f'📧 {TextHTML(user.tg_user.fullname).openmessage(user.tg_id)} хочет добавить вас в друзья'
    
    def decline(user: UserDB):
        return f'❌ Запрос дружбы c {TextHTML(user.tg_user.fullname).openmessage(user.tg_id)} был отклонен'

    def accert(user: UserDB):
        return f'✅ Вы теперь друзья с {TextHTML(user.tg_user.fullname).openmessage(user.tg_id)}'

    def delete(user: UserDB):
        return f'❌ Вы больше не друзья с {TextHTML(user.tg_user.fullname).openmessage(user.tg_id)}'
    
    def bot_blocked(user: UserDB):
        return f'❌ Запрос дружбы c {TextHTML(user.tg_user.fullname).openmessage(user.tg_id)} не был отправлен, ваш друг заблокировал бота или еще не начал им пользоваться.'
