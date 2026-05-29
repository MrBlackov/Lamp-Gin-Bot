from app.db.metods.adds import add_db_obj, ItemSketchDB, DropDB, ItemDB, ChatDB
from app.db.metods.gets import get_chat_for_tg_id, get_drops_for_chat_id, get_item_sketchs_for_ids, get_chat_for_tg_id, get_drop_for_id
from app.db.metods.unique import get_item_sketch_for_action_tag, get_drop_for_datetime, get_drops_for_datetime, get_chats_for_type
from app.db.metods.updates import update_drop_for_id, update_drops_for_id
from app.logic.action import ActionSelf
from app.logic.utils import random_today_time, random, datetime, timedelta
from app.validate.item import ItemDropValide
from app.exeption.drop import DropNotFoundError, ChatDontReceiveDropError, PrivateChatDontReceiveDropError
from app.enum_type.bd import TgType
from app.db.metods.deletes import delete_drop

class DropLogic:
    async def get_chats(self) -> list[ChatDB]:
        return await get_chats_for_type(types=[TgType.GROUP.value, TgType.SUPERGROUP.value])

    async def get_drop_item(self) -> list[ItemSketchDB]:
        return await get_item_sketch_for_action_tag(action_tag=ActionSelf.tags.drop)
 
    async def check_drop(self, chat_tg_id: int):
        chat = await get_chat_for_tg_id(chat_tg_id)
        if chat.tg_chat.tg_type.value == 'PRIVATE':
            raise PrivateChatDontReceiveDropError('❌ Дропы недоступны в личных чатах')
        if chat.setting.receive_drops == False:
            raise ChatDontReceiveDropError('❌ В этом чате выключено получение дропов')
        return chat 
    
    async def get_drop_for_chat(self, chat_tg_id):
        chat = await self.check_drop(chat_tg_id)
        drops = await self.get_drops(chat_id=chat.id, is_open=True)
        return max(drops, key=lambda x: x.open) if len(drops) > 0 else None

    async def get_drop(self, drop_id: int, **kwargs) -> DropDB:
        drop = await get_drop_for_id(drop_id)
        await self.check_drop(drop.chat.tg_id)
        return drop

    async def get_drops(self, time: datetime = datetime.now(), arg_name: str = 'open', chat_id: int | None = None, operator: str = '<=', **kwargs) -> list[DropDB]:
        return list(await get_drops_for_datetime(time=time, arg_name=arg_name, chat_id=chat_id, operator=operator, **kwargs))

    async def open_drop(self, drop_id: int):
        drop = await get_drop_for_id(drop_id)
        await self.check_drop(drop.chat.tg_id)
        if len(drop._items) == 0:
            await self.delete_drop(drop.id)
            return None
        return await self.get_items_by_drop(drop)

    async def get_items_by_drop(self, drop: DropDB) -> list[ItemDB]:
        items = {i.id:i for i in await get_item_sketchs_for_ids(ids={id for id, q in drop.items})}
        return [ItemDB(sketch=i, sketch_id=i.id, quantity=q) for i, q in [[items.get(id), q] for id, q in drop.items if id in items]]

    async def update_drops(self, drop_ids: list[int], new_data: dict):
        return await update_drops_for_id(ids=drop_ids, new_data=new_data)

    async def create_drop(self, chat_tg_id: int, coins: int, is_random: bool = True) -> DropDB:
        chat = await self.check_drop(chat_tg_id)
        drops = await get_drops_for_chat_id(chat_id=chat.id)
        items = self.generate_drop_items(items=await self.get_drop_item(), coins=coins)
        if len(items) < 1:
            return None
        open_time = random_today_time() if is_random else datetime.now()
        while datetime.now() > open_time:
            open_time = random_today_time()
        drop = DropDB(open=open_time + timedelta(days=len(drops)), chat_id=chat.id, _items=[f'{item.sketch_id}:{item.quantity}' for item in items])
        return await add_db_obj(data=[drop], logger=False)

    def generate_drop_items(self, items: list[ItemSketchDB], coins: int, drop_lenght: int = 10000) -> list[ItemDB]:
        all_items: list[ItemDB] = []
        drops: list[ItemDB] = []
        prices = {}
        for item in random.sample(items, k=len(items)):
            drop = item.nbt.get('drop')
            if drop:
                drop = ItemDropValide.model_validate(drop)
                if drop.price*drop.min_quantity > coins: 
                    continue
                prices[item.id] = drop.price
                for _ in range(int(drop.rarity*drop_lenght)):
                    all_items.append(ItemDB(sketch=item, sketch_id=item.id, quantity=drop.min_quantity))
        while coins > 0 and len(all_items) > 0:
            item = random.choice(all_items)
            coins -= item.quantity*prices.get(item.sketch_id)
            drops.append(item)
        return drops
 
    async def delete_drop(self, drop_id: int):
        return await delete_drop(id = drop_id)

