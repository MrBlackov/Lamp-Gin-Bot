from app.aio.inline_buttons.social import SocialIKB
from app.enum_type.char import Gender
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.aio.msg.social import TextHTML, SocialText
from app.aio.msg.base import TextHTML, UserText
from app.service.base import BaseService 
from app.interlayer.social import SocialLayer
from app.aio.cls.fsm.utils import SocialFSM
from app.aio.cls.fsm.social import SocialState
from app.exeption.social import SocialError
from app.aio.config import bot

class SocialService(BaseService):
    def __init__(self, tg_id, state = None, message = None, **kwargs):
        super().__init__(tg_id, state, message, **kwargs)
        self.layer = SocialLayer(tg_id)
        self.text = SocialText
        self.state = SocialFSM(state)
        self.IKB = SocialIKB(tg_id)

    async def get_friends(self):
        friends = await self.layer.get_friends()
        await self.state.update_data(friends={f.id:f for f in friends})
        return ('😎 Ваши друзья' if len(friends) > 0 else '☹️ У вас пока нет друзей'), self.IKB.friends(friends)
    
    async def friend(self, user_id: int):
        friends = await self.state.get_value('friends', {})
        friend = friends.get(user_id)
        return UserText(friend.tg_user, friend).text, self.IKB.friend(user_id, 'myfriends')
    
    async def to_send_request(self, msg):
        await self.state.set_state(SocialState.friend_data)
        await self.state.update_data(msg=msg)
        return '✒️ Отправьте юзер пользователя', self.IKB.back('myfriends')

    async def send_request(self, user_name: str):
        friend, user = await self.layer.get_friend(user_name.strip('@'))
        await bot.send_message(chat_id=friend.tg_id, text=self.text.request(user), reply_markup=SocialIKB(friend.tg_id).request(user.id))
        return self.text.send(friend), self.IKB.back('myfriends')
    
    async def answer_request(self, friend_id: int, status: str):
        friend, user = await self.layer.answer_request(friend_id, status)
        if status == 'decline':
            await bot.send_message(chat_id=friend.tg_id, text=self.text.decline(user), reply_markup=SocialIKB(friend.tg_id).back('myfriends'))
            return self.text.decline(friend), self.IKB.back('myfriends')
        elif status == 'accert':            
            await bot.send_message(chat_id=friend.tg_id, text=self.text.accert(user), reply_markup=SocialIKB(friend.tg_id).back('myfriends'))
            return self.text.accert(friend), self.IKB.back('myfriends')
    
    async def delete_friend(self, friend_id: int):
        friend, user = await self.layer.delete_friend(friend_id)
        await bot.send_message(chat_id=friend.tg_id, text=self.text.delete(user), reply_markup=SocialIKB(friend.tg_id).back('myfriends'))
        return self.text.delete(friend), self.IKB.back('myfriends')

