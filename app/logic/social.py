from app.db.metods.adds import add_db_obj, UserSettingDB, CharSettingDB, UserDB
from app.db.metods.gets import get_users_for_ids, CharacterDB
from app.db.metods.unique import get_user_for_username
from app.db.metods.updates import update_user_for_id
from app.logic.settings import SettingValueBase, SettingSelf

class SocialLogic:
    async def get_friends(self, ids: list[int]):
        return await get_users_for_ids(ids)
    
    async def get_friend(self, user_name: str) -> UserDB | None:
        return await get_user_for_username(username=user_name)  
    
    async def operation(self, friend: UserDB, user: UserDB, operation: str):
        match operation:
            case "+":
                friend = await update_user_for_id(friend.id, {'friend_ids':(list(friend.friend_ids) + [user.id] if friend.friend_ids else [user.id])})
                user = await update_user_for_id(user.id, {'friend_ids':(list(user.friend_ids) + [friend.id] if user.friend_ids else [friend.id])})
            case "-":
                friend_ids = list(friend.friend_ids) if friend.friend_ids else []
                user_ids = list(user.friend_ids) if user.friend_ids else []
                friend_ids.remove(user.id)
                user_ids.remove(friend.id)
                friend = await update_user_for_id(friend.id, {'friend_ids':friend_ids})
                user = await update_user_for_id(user.id, {'friend_ids':user_ids})
        return friend, user