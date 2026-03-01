from aiogram.fsm.context import FSMContext

class FSMUtils:
    prefixs: list[str] = []
    
    def __init__(self, state: FSMContext | None, prefix_two: str = ''):
        self.state = state
        self.prefix_two = prefix_two

    @property
    def prefix(self):
        return '_'.join(self.prefixs + [self.prefix_two])
    
    def get_value(self, key: str, default = None):
        print(self.prefix + key)
        return self.state.get_value(self.prefix + key, default)
    
    def update_data(self, **kwargs):
        print({self.prefix + k: v for k, v in kwargs.items()})
        return self.state.update_data(**{self.prefix + k: v for k, v in kwargs.items()})
    
    def set_state(self, new_state = None):
        return self.state.set_state(new_state)
 
    def get_data(self):
        return self.state.get_data()

    def clear(self):
        return self.state.clear()

class CharFSM(FSMUtils):
    prefixs = ['char']

class ItemFSM(FSMUtils):
    prefixs = ['item']

class CraftFSM(FSMUtils):
    prefixs = ['craft']

class FaqFSM(FSMUtils):
    prefixs = ['faq']
    
class KitFSM(FSMUtils):
    prefixs = ['kit']
    
class MainFSM(FSMUtils):
    prefixs = ['main']
    
class StatsFSM(FSMUtils):
    prefixs = ['stats']
    
class TransferFSM(FSMUtils):
    prefixs = ['transfer']
    

