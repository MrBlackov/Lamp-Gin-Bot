from app.logic.char import CharLogic
from app.logic.item import ItemsLogic, ItemSketchsLogic
from app.logic.transfer import TransferLogic
from app.interlayer.item import ItemLayer, ItemDB
from app.db.models.char import CharacterDB
from app.db.metods.gets import get_user_for_tg_id, get_user_for_id, get_main_char_for_user_id, get_char_for_id, get_items_for_inventory
from app.exeption.transfer import TransferNoHaventItemError, TransferQuantityNoIntError, TransferSellerNoHaventItemError, TransferError, TransferNoFindError
from app.db.models.transfer import TransferDB

class TransferLayer:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id
        self.char = CharLogic(tg_id)
        self.item = ItemsLogic()
        self.item_sketch = ItemSketchsLogic()
        self.transfer = TransferLogic()

    async def get_char_info(self, user_id: int | None = None):
        if user_id:
            self.user = await get_user_for_id(user_id)
        else:
            self.user = await get_user_for_tg_id(self.tg_id, True)
        self.char_id = await get_main_char_for_user_id(self.user.id)
        self.char_info = await get_char_for_id(self.char_id)
        return self

    async def locator(self):
        await self.get_char_info()
        chars = await self.char.get_all_chars()
        return [char for char in chars if char.id != self.char_id]

    async def check_inventory(self, char: CharacterDB, items: list[ItemDB] | None, is_seller: bool = False):
        if items == None:
            return True
        inventory = await get_items_for_inventory(char.exist.inventory.id)
        inventory_items_id = {i.sketch.id: i for i in inventory}
        for item in items:
            if item.sketch.id not in inventory_items_id or inventory_items_id[item.sketch.id].quantity < item.quantity:
                if is_seller: 
                    raise TransferSellerNoHaventItemError(f'This char(id={char.id}, is seller) has not enough item for transfers')
                raise TransferNoHaventItemError(f'This char(id={char.id}) has not enough item for transfers')
        return True

    async def newtrade(self, 
                       char1: CharacterDB, 
                       char2: CharacterDB,
                       items1: list,
                       items2: list, 
                       status: str):
        self = await self.get_char_info()
        if status == 'confirmed':
            inventory = await get_items_for_inventory(char1.exist.inventory.id)
            self.item.check_size_inventory(char1, inventory, items2, '+')
            await self.check_inventory(char1, items1)
        trade = await self.transfer.new_transfer(char1.id, char2.id, items1, items2, status)
        user = await get_user_for_id(char2.user_id)
        return user.tg_id, self.user, trade
    
    async def transfers(self):
        self = await self.get_char_info()
        return await self.transfer.get_transfers(self.char_id)
    
    async def search(self, query: str, search_type: str):
        if query.isdigit() == False:
            raise TransferQuantityNoIntError(f'This user(tg_id={self.tg_id}) enter quantity to transfer no int')
        query = int(query)
        self = await self.get_char_info()
        print(search_type)
        if search_type == 'transfer_id':
            result = await self.transfer.search_for_id(self.char_id, query)
            if result:
                return result
        elif search_type == 'char_id':
            result = await self.transfer.search_for_char_id(self.char_id, query)
            if result.from_me or result.to_me:
                return result
        elif search_type == 'item_id':
            result = await self.transfer.search_for_item_id(self.char_id, query)
            if result.from_me or result.to_me:
                return result

        raise TransferNoFindError(f'This user(tg_id={self.tg_id}) enter search value, but nothing found', level='error')

    async def get_items(self, transfer_id: int):
        return await self.transfer.get_items_for_transfer_id(transfer_id)

    async def update_status(self, transfer_id: int, new_status: str):
        transfer =  await self.transfer.update_status(transfer_id, new_status)
        seller_tg = await get_user_for_id(transfer.seller.user_id)
        buyer_tg = await get_user_for_id(transfer.buyer.user_id)
        if buyer_tg.tg_id == self.tg_id:
            self.char = transfer.seller
            self.user_tg = seller_tg
            self.my_char = transfer.buyer
        elif seller_tg.tg_id == self.tg_id:
            self.char = transfer.buyer
            self.user_tg = buyer_tg
            self.my_char = transfer.seller
        else:
            raise TransferError(f'Transfer(id={transfer_id}) not seller and buyer', level='error')
        self.transfer = transfer
        return self

    async def transfer_complete(self, transfer_id: int):
        transfer, seller_items, buyer_items = await self.transfer.get_transfer_for_id(transfer_id)
        await self.check_inventory(transfer.buyer, buyer_items)
        await self.check_inventory(transfer.seller, seller_items, is_seller=True)
        
        await self.item.action_for_items(seller_items, transfer.seller, '-')
        await self.item.action_for_items(buyer_items, transfer.buyer, '-')

        side1 = await self.item.action_for_items(seller_items, transfer.buyer, '+')
        side2 = await self.item.action_for_items(buyer_items, transfer.seller, '+')
        if side1 and side2:
            await self.transfer.update_status(transfer_id, 'completed')
            user_tg = await get_user_for_id(transfer.seller.user_id)
            return transfer.seller, user_tg, transfer.buyer
        raise TransferError(f'Transfer(id={transfer_id}) not completed', level='error')

    async def delete_transfer(self, transfer_id: int):
        return await self.transfer.delete_transfer(transfer_id)

    async def redact_transfer(self, transfer: TransferDB, new_status: str):
        if transfer.status == 'created':
            await self.transfer.delete_transfer(transfer.id)
        elif transfer.status == 'confirmed':
            await self.transfer.update_status(transfer.id, new_status)

        

        

