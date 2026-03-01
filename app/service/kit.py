from aiogram.fsm.context import FSMContext
from app.aio.inline_buttons.char import AddCharIKB, InfoCharIKB, InventoryIKB
from app.enum_type.char import Gender
from app.logged.botlog import logs
from app.logged.infolog import infolog
from app.aio.msg.base import UserText
from app.aio.msg.utils import TextHTML
from app.service.base import BaseService 
from app.interlayer.kit import KitLayer
from app.aio.inline_buttons.kit import KitIKB
from app.aio.cls.fsm.kit import KitState
from app.aio.msg.kit import KitText
from app.aio.cls.fsm.utils import KitFSM

class KitService(BaseService):
    def __init__(self, tg_id, state = None):
        super().__init__(tg_id, state)
        self.state = KitFSM(state)
        self.layer = KitLayer(tg_id)
        self.IKB = KitIKB()

    async def kits(self):
        kits, no_hide = await self.layer.my_kits()
        await self.state.update_data(kits=kits, no_hide=no_hide)
        return (('💼 Доступные для использования наборы' if kits or no_hide else '❌ У вас нет достпуных для использования наборов'), 
                self.IKB.my_kits([k for k in kits if k.get == False] if kits else None, no_hide))

    async def kit(self, kit_id: int, is_new: bool = False):
        kits = await self.state.get_value('kits')
        kits = {k.id: k for k in kits} if kits else {}
        no_hide = await self.state.get_value('no_hide')
        no_hide = {k.id: k for k in no_hide} if no_hide else {}
        if kits:
            kit = kits.get(kit_id)
            sketch = kit.sketch
            items = await self.layer.kit_items(kit.sketch)
        elif no_hide:
            sketch = no_hide.get(kit_id)
            items = await self.layer.kit_items(sketch)
        return (KitText(sketch=sketch).text(items, True), self.IKB.newkit('cmd')) if is_new else (KitText(kit).text(items), self.IKB.kit('cmd'))

    async def to_enter_code(self, msg):
        await self.state.update_data(msg=msg)
        await self.state.set_state(KitState.code)
        return '✒️ Введите промкоод', self.IKB.back('cmd')

    async def enter_code(self, code: str):
        kit = await self.layer.get_kit_for_code(code)
        sketchs = await self.layer.kit_items(kit)
        return KitText(kit).text(sketchs, True), self.IKB.newkit('cmd')