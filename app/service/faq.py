from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.faq import FaqIKB
from app.enum_type.char import Gender
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.aio.msg.faq import TextHTML, FaqText
from app.service.base import BaseService 
from app.exeption import error_faq, BotError
from aiogram.types.chat_member_banned import ChatMemberStatus
from app.exeption.faq import FaqErrorNoEnterError, FaqErrorNoFindError

class FaqService(BaseService):
    def __init__(self, tg_id: int, state: FSMContext | None = None):
        super().__init__(tg_id, state)
        self.IKB = FaqIKB()
        self.text = FaqText

    def to_error_faq(self, text: str, code: str):
        error = error_faq.get(code, None)
        if error == None:
            raise FaqErrorNoFindError(f'This user(tg_id:{self.tg_id}) enter code, but dont find error')        
        return text + TextHTML(error.faq).blockquote(), None
    
    def help_error_faq(self, code: str):
        error = error_faq.get(code, None)
        if error == None:
            raise FaqErrorNoFindError(f'This user(tg_id:{self.tg_id}) enter code, but dont find error')   
        return self.text(error).help_error_faq(), None
    
    def to_start(self, name: str | None):
        return self.text.to_start(name if name else 'уважаемый'), None

    def help_cmd(self):
        if self.tg_id in self.admins:
            return self.text.help_cmd(True), None
        return self.text.help_cmd(), None

    def help(self):
        return self.text.help(), None
   
    def to_item_rules(self):
        return self.text.item_rules(), None
     
    def help_chars(self):
        return self.text.help_chars(), None
    
    def help_items(self):
        return self.text.help_items(), None
    


