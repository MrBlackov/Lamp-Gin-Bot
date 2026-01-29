from app.logic.dnd import person
from app.validate.add.characters import Existence_add, Character_add, CharSketch
from app.enum_type.char import Gender

class CreateExistence:
    def __init__(self, gender: Gender = 'M', prs: person = person('M')):
        self.person = prs
        self.gender = gender

    def create_char_skecth(self):
        return CharSketch(
            gender=self.gender,
            points=self.person.points,
            age=self.person.age,
            amount_life=self.person.amount_age
        )
    
    def create_char_skecths(self, sketch_quantity: int = 5):
        return [self.create_char_skecth() for _ in range(sketch_quantity)]

    def char_sketch_to_valid_model(user_id: int, names: tuple | str, sketch: CharSketch, descript: str | None = None) -> Character_add:
        if type(names) == str:
            names = tuple(names.split(' ', maxsplit=2))
        return Character_add(
            user_id=user_id,
            exist=Existence_add(
                first_name=names[0],
                last_name=names[1] if len(names) > 1 else None,
                gender=sketch.gender,
                attibute_point=sketch.points,
                age=sketch.age,
                amount_life=sketch.amount_life
                                ),
            description=descript
        )

    def create_exist(self, names: tuple | str):
        if type(names) == str:
            names = tuple(names.split(' ', maxsplit=2))
        return Existence_add(
            first_name=names[0],
            last_name=names[1] if len(names) > 1 else None,
            gender=self.gender,
            attibute_point=self.person.points,
            age=self.person.age,
            amount_life=self.person.amount_age
        )
    
    def create_char(self, names: str, user_id: int, descript: str | None = None):
        new_exist = self.create_exist(names)
        return Character_add(user_id=user_id, exist=new_exist, description=descript)



    







