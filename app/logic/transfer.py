from app.db.metods.gets import get_item, get_item_for_id, get_char_for_id, get_items_for_inventory, get_item_sketch, get_item_sketchs
from app.db.metods.adds import add_transfer_dict, add_items_db, ItemDB, ItemSketchDB

class TransferLogic:
    async def new_transfer(self, char1_id: int, char2_id: int, items1: list[ItemDB], items2: list[ItemDB]):
        transfer = await add_transfer_dict(data={'seller_id':char1_id, 'buyer_id':char2_id, 'type':'trade', 'status':'pending'})
        if items1:
            await add_items_db(data=[ItemDB(transfer_id=transfer.id, sketch_id=item.sketch_id, quantity=item.quantity) for item in items1])
        if items2:
            await add_items_db(data=[ItemDB(transfer_id=transfer.id, sketch_id=item.sketch_id, quantity=item.quantity) for item in items2])
        return transfer