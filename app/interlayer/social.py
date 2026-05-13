from app.interlayer.base import BaseLayer
from app.logic.social import SocialLogic
from app.exeption.social import SocialError, NoFindUserError, UserFriendError, EnterUserNameError, NotReceiveFriendshipRequestError
from app.logic.settings import is_receive_friedship_requests

class SocialLayer(BaseLayer):
    def __init__(self, tg_id):
        
        super().__init__(tg_id)
        self.logic = SocialLogic()

    async def get_friends(self):
        await self.get_char_info(and_char=False)
        return self.user.friends
     
    async def get_friend(self, user_name):
        await self.get_char_info(and_char=False)
        friend = await self.logic.get_friend(user_name)
        friend = await self.get_user_full_info(friend.id)
        if friend == None:
            raise NoFindUserError(f'Пользователь {user_name} не найден')
        if self.user.id == friend.id:
            raise EnterUserNameError(f'This user enter username but username == user.username')
        if friend.id in self.user.friend_ids:
            raise UserFriendError(f'This user is her friend')
        if friend.parametrs_tag.get(is_receive_friedship_requests.tag).value == False:
            raise NotReceiveFriendshipRequestError('This user no receive requets for friend')
        return friend, self.user

    async def answer_request(self, friend_id: int, status: str):
        await self.get_char_info(and_char=False)
        friend = await self.get_user_full_info(friend_id)
        if status == 'decline':
            return friend, self.user
        return await self.logic.operation(friend, self.user, '+')
     
    async def delete_friend(self, friend_id: int):
        await self.get_char_info(and_char=False)
        friend = await self.get_user_full_info(friend_id)
        return await self.logic.operation(friend, self.user, '-')
  

