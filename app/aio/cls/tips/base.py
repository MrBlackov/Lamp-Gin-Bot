import random

class TipBase:
    base_tips = ['❗ Подпишитесь на наш Газету и получите дополнитеьного персонажа',]
    tips = None

    def __init__(self, rarity: float = 1.0):
        self.rarity = rarity

    @property
    def tip(self):
        if self.tips and self.rarity >= random.random():
            return random.choice(self.all_tips)
        
    @property
    def all_tips(self):
        return self.base_tips + (self.tips if self.tips else [])
