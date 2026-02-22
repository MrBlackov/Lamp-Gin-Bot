from app.aio.config import Bot, token, DefaultBotProperties, ParseMode

class InfoTopics:
    chat = -1003584045594
    char = 3
    transfer = 16
    item = 9
    item_no_moderate = 37

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
    
infolog = InfoLog(token=token)