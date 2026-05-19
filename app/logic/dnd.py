from faker import Faker
from typing import Literal
from faker.providers.person.en_US import Provider as EnUsProvider
from faker.providers.person.ru_RU import Provider as RuProvider
from faker.providers.person.en_GB import Provider as EnGbProvider
from faker.providers.person.de_DE import Provider as DeProvider
from faker.providers.person.fr_FR import Provider as FrProvider
from faker.providers.person.it_IT import Provider as ItProvider
from app.validate.add.characters import Points
from collections import OrderedDict
from app.enum_type.char import Gender
from app.exeption.another import DiceError
from app.exeption.action import DiceCmdNoValideError
from app.validate.add.characters import ItemValide
from app.db.models.item import SkillDB, SkillSketchDB, ItemSketchDB
import random

providers = {
    'ru_RU':RuProvider, 
    'en_US':EnUsProvider, 
    'en_GB':EnGbProvider, 
    'de_DE':DeProvider, 
    'fr_FR':FrProvider, 
    'it_IT':ItProvider
}

class dice:
    def __init__(self, max: int = 6, min: int = 1, step: int = 1):
        if max < min:
            raise DiceError(f'This max({max}) < min({min})')

        self.max = max
        self.min = min
        self.step = step
        self.fake = Faker()
        self._throw = ()
    
    @property
    def throw(self):
        return self._to_throw()._throw[0]
    
    def _to_throw(self, quantity: int = 1):
        self._throw = tuple([self.fake.random_int(min=self.min, max=self.max, step=self.step) for _ in range(quantity)])
        return self
    
    def to_throw(self, quantity: int = 1):
        return self._to_throw(quantity).medium
    
    @property
    def sum(self):
        return sum(self._throw)
    
    @property
    def medium(self):
        return sum(self._throw)//len(self._throw)

class dices:
    def __init__(self, cubes: list[dice] = [dice()]):
        self.cubes = cubes
        self.throw = tuple([cube.throw for cube in self.cubes])

    def to_throw(self, quantity: int = 1, to_general_typle: bool = True):
        self.throw = tuple([cube.to_throw(quantity).throw for cube in self.cubes])
        if type(self.throw[0]) == tuple and to_general_typle:
            throw = []
            for values in self.throw:
                for value in values:
                    throw.append(value)
            self.throw = tuple(throw)
        return self
        
    def roll_dice(self, command: str, d: list[int] = [1, 20]):
        k_dice = 1
        mod = 0
        try:
            if 'd' in command:
                d_index = command.index('d')
                probel = command.index(' ') if ' ' in command else len(command)
                if d_index > 0:
                    k_dice = int(command[:d_index])
                    d = (d[0], int(command[d_index+1:probel]) or d[1])
                command = command.replace(command[0:d_index+1] + ' ', '')
            parts = command.split(' ')
            for c in parts:
                if '+' == c:
                    mod_index = parts.index('+')
                    if mod_index > 0:
                        mod += float(parts[mod_index+1])
                elif '-' == c:
                    mod_index = parts.index('-')
                    if mod_index > 0:
                        mod -= float(parts[mod_index+1])
        except ValueError as e:
            raise DiceCmdNoValideError(f'This dice-cmd dont valid')
        
        dices_throw = dice(d[1], d[0])._to_throw(k_dice)._throw
        self.throw = dices_throw
        self.mod = mod
        self.d = d
        self.d_text = f'{k_dice}d{d[1]}'
        self.result = self.sum + mod
        return self

    @property
    def sum(self):
        return sum(self.throw)
    
    @property
    def medium(self):
        return sum(self.throw)/len(self.throw)

class rnd_list:
    def __init__(self, list: list):
        self.list = list
        self.fake = Faker()
        self.len = len(list)

    @property
    def elements(self):
        return self.fake.random_elements(self.list, length=self.len, unique=True)
    
    def to_elements(self, len: int | None = None, unique: bool = True):
        if len == None: len = self.len
        return self.fake.random_elements(self.list, length=len, unique=unique)

    @property
    def element(self):
        return self.fake.random_element(self.list)
    
    @property
    def chouses(self):
        return self.fake.random_choices(self.list, self.len)
    
    def to_chouses(self, len: int | None = None):
        if len == None: len = self.len
        return self.fake.random_choices(self.list, len)    
    
    @property
    def chouse(self):
        return self.fake.random_choices(self.list)

class person:
    def __init__(self, gender: Gender, coins: int = 60, local: str = 'en_US'):
        self.fake = Faker(providers[local])
        self.provider = providers[local]
        self.coins = coins
        self.gender = gender
        self.random = random

    def get_names(self, local:  str | None = None): 
        if local:
            self.provider = providers[local]
        first_names = self.provider.first_names_male if self.gender == Gender.M.value else self.provider.first_names_female
        return (first_names, self.provider.last_names) if type(first_names) != dict and type(first_names) != OrderedDict else (first_names.keys(), self.provider.last_names.keys())

    @property
    def names(self):
        return self.get_names()

    @property
    def full_name(self):
        if self.gender == Gender.M.value:
            return self.fake.name_male()
        elif self.gender == Gender.W.value:
            return self.fake.name_female()
        
    @property
    def age(self):
        return self.to_age()

    @property
    def amount_age(self):
        return self.age + self.to_age() + 10

    def to_age(self, args: list[dice] = [dice(80, 16), dice(21, 18), dice(21, 18)]) -> int:
        return int(dices(args).medium)
    
    #@property
    #def penny(self):
    #    return self.to_penny()
#
    #def to_penny(self, args: list[dice] = [dice(10000, 0)]):
    #    return int(dices(args+[dice(self.age*100)]).sum)

    @property
    def points(self):
        point_list = [10]
        for _ in range(4):
            point_list.append(self.to_point())
            
        base_point_list = list(rnd_list(point_list).elements)
        dop_point_list = []
        for _ in range(6):
            dop_point_list.append(self.to_point([dice(2, -1), dice(2, -1), dice(2, -1)]))

        return Points(
            strength=base_point_list[0],
            health=base_point_list[1], 
            intelligence=base_point_list[2], 
            dexterity=base_point_list[3],
            speed_value=dop_point_list[0],
            spirituality=dop_point_list[1] if dop_point_list[1] > 0 else 0
            )

    def to_point(self, args: list[dice] = [dice(18, 8), dice(13, 10)]):
        point = int(dices(args).medium)
        self.coins -= point
        return point
    
    def check_size(self, max_size: int, size: int, quantity: int, accuracy: int = 1, inventory_part: float = 1.5, n = 0):
        if n > 900:
            return 0
        if max_size/inventory_part < size*quantity:
            return self.check_size(max_size, size, quantity-accuracy, n=n+1)
        return quantity

    def to_inventory(self, max_size: int, sketchs: list[ItemSketchDB]):
        items: list[ItemValide] = []
        for sketch in sketchs:
            random_int = self.random.random()
            if random_int > sketch.rarity:
                continue
            rnd_quantity = self.random.randint(sketch.min_drop, sketch.max_drop)
            quan = self.check_size(max_size, sketch.size, rnd_quantity)
            if quan > 0:
                items.append(ItemValide(sketch_id=sketch.id, quantity=quan, sketch=sketch))
        return items
    
class CharGenerator:
    def __init__(self, gender: str, coins: int = 50, local: str | None = None):
        self.gender = gender
        self.coins = coins
        self.random = random
        self.provider_str = self.random.choice(list(providers.keys()))
        self.faker = Faker(self.provider_str)
        self.provider = providers.get(self.provider_str)


    def to_age(self, args: list[dice] = [dice(80, 16), dice(21, 18), dice(21, 18)]) -> int:
        return int(dices(args).medium)
    
    @property
    def age(self):
        return self.to_age()

    @property
    def first_name(self):
        return self.faker.first_name_male() if self.gender == 'M' else self.faker.first_name_female()

    @property
    def last_name(self):
        return self.faker.last_name_male() if self.gender == 'M' else self.faker.last_name_female()
    
    def rnd_names(self):
        return (self.faker.first_name_male(), self.faker.last_name_male()) if self.gender == 'M' else (self.faker.first_name_female(), self.faker.last_name_female())

    def skills(self, base_skills: list[SkillSketchDB]):
        return {s.sketch.tag:s for s in [SkillDB(level=bs.default_level, coins=bs.default_coins, sketch=bs, sketch_tag=bs.tag, sketch_id=bs.id) for bs in base_skills]}

    def get_names_for_local(self, local:  str | None = None): 
        if local:
            self.provider = providers[local]
        first_names = self.provider.first_names_male if self.gender == Gender.M.value else self.provider.first_names_female
        return (first_names, self.provider.last_names) if type(first_names) != dict and type(first_names) != OrderedDict else (first_names.keys(), self.provider.last_names.keys())

    def get_all_names(self):
        fn, ln = [], []
        for local in providers:
            nfn, nln = self.get_names_for_local(local)
            fn.extend(list(nfn)), ln.extend(list(nln))
        return fn, ln

if __name__ == '__main__':   
    for _ in range(100):
        pd = person()
        print(pd.age, pd.amount_age, pd.full_name)