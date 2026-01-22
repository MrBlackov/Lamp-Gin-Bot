from faker import Faker
from typing import Literal
from faker.providers.person.en_US import Provider as EnUsProvider
from app.validate.add.characters import Points
from collections import OrderedDict
from app.enum_type.char import Gender
from app.exeption.another import DiceError

lokals = {
    'loen':'en_US'
}
providers = {
    'loen':EnUsProvider,
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
        return self.to_throw()._throw[0]
    
    def to_throw(self, quantity: int = 1):
        self._throw = tuple([self.fake.random_int(min=self.min, max=self.max, step=self.step) for _ in range(quantity)])
        return self

    @property
    def sum(self):
        return sum(self.throw)
    
    @property
    def medium(self):
        return sum(self.throw)/len(self.throw)

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
    def __init__(self, gender: Gender, coins: int = 60, local: Literal['loen'] = 'loen'):
        self.fake = Faker(lokals[local])
        self.provider = providers[local]
        self.coins = coins
        self.gender = gender

    def get_names(self, local:  Literal['loen'] | None = None): 
        if local:
            self.provider = providers[local]
        first_names = self.provider.first_names_male if self.gender == Gender.M else self.provider.first_names_female
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
    
    @property
    def penny(self):
        return self.to_penny()

    def to_penny(self, args: list[dice] = [dice(10000, 0)]):
        return int(dices(args+[dice(self.age*100)]).sum)

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

    def to_point(self, args: list[dice] = [dice(14, 7), dice(13, 8)]):
        point = int(dices(args).medium)
        self.coins -= point
        return point
        


if __name__ == '__main__':   
    for _ in range(100):
        pd = person()
        print(pd.age, pd.amount_age, pd.full_name)