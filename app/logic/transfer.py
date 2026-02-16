from app.db.metods.gets import get_transfers, get_transfers_for_char_id, get_items_for_transfer, get_transfer_for_id
from app.db.metods.unique import get_transfers_for_item_id
from app.db.metods.deletes import delete_transfer_for_id
from app.db.metods.updates import update_transfer
from app.db.metods.adds import add_transfer_dict, add_items_db, ItemDB, ItemSketchDB, TransferDB
from app.logic.cls import MyTransfers
from datetime import datetime

class TransferLogic:
    async def new_transfer(self, char1_id: int, char2_id: int, items1: list[ItemDB], items2: list[ItemDB], status: str):
        transfer = await add_transfer_dict(data={'seller_id':char1_id, 'buyer_id':char2_id, 'type':'trade', 'status':status})
        if items1:
            new_items1 = await add_items_db(data=[ItemDB(transfer_id=transfer.id, sketch_id=item.sketch_id, quantity=item.quantity, from_char_transfers=True) for item in items1])
        if items2:
            new_items2 = await add_items_db(data=[ItemDB(transfer_id=transfer.id, sketch_id=item.sketch_id, quantity=item.quantity, from_char_transfers=False) for item in items2])
        await update_transfer(filters={'id': transfer.id}, 
                              new_data={'seller_items': [item.id for item in new_items1] if items1 else None, 
                                        'buyer_items': [item.id for item in new_items2] if items2 else None})
        return transfer
    
    async def get_transfers(self, char_id: int):
        return await get_transfers(char_id)

    async def search_for_id(self, char_id: int, transfer_id: int) -> TransferDB | None:
        transfers = await self.get_transfers(char_id)
        result = transfers.all_for_id.get(transfer_id, None)
        return result
    
    async def search_for_char_id(self, char_id: int, query_char_id: int) -> MyTransfers:
        transfers = await get_transfers_for_char_id(char_id, query_char_id)  
        return transfers

    async def search_for_item_id(self, char_id: int, item_id: int) -> MyTransfers:
        transfers: list[TransferDB] = await get_transfers_for_item_id(char_id=char_id, item_id=item_id)
        buyers = [t for t in transfers if t.buyer_id == char_id]
        sellers =  [t for t in transfers if t.seller_id == char_id]
        return MyTransfers(sellers, buyers)

    async def get_items_for_transfer_id(self, transfer_id: int) -> MyTransfers:
        items1 = await get_items_for_transfer(transfer_id, True)
        items2 = await get_items_for_transfer(transfer_id, False)
        return MyTransfers(from_me_items=items1, to_me_items=items2)

    async def update_status(self, transfer_id: int, new_status: str) -> TransferDB:
        return await update_transfer(filters={'id': transfer_id}, new_data={'status': new_status})

    async def update_data_complete(self, transfer_id: int):
        return await update_transfer(filters={'id': transfer_id}, new_data={'data_completion': datetime.now()})

    async def get_transfer_for_id(self, transfer_id: int) -> tuple[TransferDB | None, list[ItemDB] | None, list[ItemDB] | None]:
        transfer =  await get_transfer_for_id(transfer_id)
        seller_items = await get_items_for_transfer(transfer_id, True)
        buyer_items = await get_items_for_transfer(transfer_id, False)
        return transfer, seller_items, buyer_items

    async def transfer_complete(self, transfer_id: int) -> bool:
        await self.update_status(transfer_id, 'completed')
        await self.update_data_complete(transfer_id)
        return True

    async def update_items_for_char(self, inventory1_id: int, inventory2_id: int, items1: list[ItemDB], items2: list[ItemDB]):
        await add_items_db(data=[ItemDB(inventory_id=inventory1_id, sketch_id=item.sketch_id, quantity=item.quantity) for item in items2])
        await add_items_db(data=[ItemDB(inventory_id=inventory2_id, sketch_id=item.sketch_id, quantity=item.quantity) for item in items1])
        return True

    async def delete_transfer(self, transfer_id: int):
        return await delete_transfer_for_id(transfer_id)