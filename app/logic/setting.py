from app.db.metods.adds import add_db_obj, UserSettingDB, CharSettingDB, UserDB
from app.db.metods.gets import get_char_setting_for_char_id, get_user_setting_for_user_id, CharacterDB
from app.db.metods.updates import update_char_setting, update_user_setting
from app.logic.settings import SettingValueBase, SettingSelf

class SettingLogic:
    setting_self = SettingSelf
    
    async def check_setting(self, type: str, user: UserDB, char: CharacterDB) -> list[SettingValueBase]:
        if user.setting == None:
            user.setting = (await add_db_obj(data=[UserSettingDB(user_id=user.id)]))[0]
        if char.setting == None:
            char.setting = (await add_db_obj(data=[CharSettingDB(char_id=char.id, user_setting_id=user.setting.id)]))[0]

    async def redact_setting(self, tag: str, type: str, user: UserDB, char: CharacterDB) -> list[SettingValueBase]:
        match type:
            case 'user':
                settings: list[SettingValueBase] = user.parametrs
                setting = {a.tag:a.value for a in settings if not(a.is_bot_default)}
                a = self.setting_self.parameters_tags.get(tag)(user.setting)
                new_value = a.redact()
                if new_value == SettingSelf.DEFAULT and tag in setting:
                    setting.pop(tag)
                elif new_value != SettingSelf.DEFAULT:
                    setting[tag] = new_value
                new_setting = await update_user_setting(filters={'user_id':user.id}, new_data={'settings':setting})
                return [a(new_setting) for a in SettingSelf.all_parameters]
            case 'char':
                settings: list[SettingValueBase] = char.parametrs
                setting = {a.tag:a.value for a in settings if not(a.is_bot_default or a.is_user_default)}
                a = self.setting_self.parameters_tags.get(tag)(char.setting)
                new_value = a.redact()
                if new_value == SettingSelf.DEFAULT and tag in setting:
                    setting.pop(tag)
                elif new_value != SettingSelf.DEFAULT:
                    setting[tag] = new_value
                new_setting = await update_char_setting(filters={'char_id':char.id}, new_data={'settings':setting})
                return [a(new_setting) for a in SettingSelf.all_parameters]

    async def insert_json(self, data: dict, type: str, user: UserDB, char: CharacterDB) -> list[SettingValueBase]:
        match type:
            case 'user':
                new_setting = await update_user_setting(filters={'user_id':user.id}, new_data={'settings':data})
                return [a(new_setting) for a in SettingSelf.all_parameters]
            case 'char':
                new_setting = await update_char_setting(filters={'char_id':char.id}, new_data={'settings':data})
                return [a(new_setting) for a in SettingSelf.all_parameters]
 
    

 