from app.aio.config import Bot, token, DefaultBotProperties, ParseMode, infolog

class InfoTopics:
    chat = infolog
    char = 3
    transfer = 16
    item = 9
    item_no_moderate = 37
    craft = 414
    craft_no_moderate = 419 
    radio = 1096
    give = 1113
    tag = 1105

class InfoLog:
    def __init__(self, token: int, **kwargs):
        self.token = token
        self.kwargs = kwargs
        self.bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML), **kwargs)
        self.topic = InfoTopics()

    async def new_char(self, user_id: int, text: str):
        await self.bot.send_message(chat_id=self.topic.chat, text=text + f'\n #newchar #user_id_{user_id}', message_thread_id=self.topic.char)
        return True
    
    async def new_transfer(self, user_id: int, text: str):
        await self.bot.send_message(chat_id=self.topic.chat, text=text + f'\n #newtransfer #user_id_{user_id}', message_thread_id=self.topic.transfer)
        return True
    
    async def new_item(self, user_id: int, text: str):
        await self.bot.send_message(chat_id=self.topic.chat, text=text + f'\n #newitem #user_id_{user_id}', message_thread_id=self.topic.item)
        return True
    
    async def new_sketch_no_moderate(self, user_id: int, text: str, markup = None):
        await self.bot.send_message(chat_id=self.topic.chat, text=text + f'\n #newitemsketch #user_id_{user_id}', reply_markup=markup, message_thread_id=self.topic.item_no_moderate)
        return True
    
    async def new_craft_no_moderate(self, user_id: int, text: str, markup = None):
        await self.bot.send_message(chat_id=self.topic.chat, text=text + f'\n #newcraftsketch #user_id_{user_id}', reply_markup=markup, message_thread_id=self.topic.craft_no_moderate)
        return True

    async def new_craft(self, user_id: int, text: str):
        await self.bot.send_message(chat_id=self.topic.chat, text=text + f'\n #newcraft #user_id_{user_id}', message_thread_id=self.topic.craft)
        return True
    
    async def radio_msg(self, user_id: int, text: str):
        await self.bot.send_message(chat_id=self.topic.chat, text=text + f'\n #radio #user_id_{user_id}', message_thread_id=self.topic.radio)
        return True

    async def char_rename(self, user_id: int, char_id: int, old_name: str, new_name: str):
        await self.bot.send_message(chat_id=self.topic.chat, text=f'🏷️ Персонаж переименован \n char_id={char_id} \n exist_id={self.char.exist.id}] \n "{old_name}" -> "{new_name}" \n\n #rename #user_id_{user_id}', message_thread_id=self.topic.tag)
        return True    
  
    async def give_info(self, user_id: int, text: str):
        await self.bot.send_message(chat_id=self.topic.chat, text=text + f'\n\n #give #user_id_{user_id}', message_thread_id=self.topic.give)
        return True

infolog = InfoLog(token=token)