from app.logic.dnd import person
from app.validate.add.characters import Existence_add, Character_add, CharSketch, Inventory_add
from app.enum_type.char import Gender

class CreateExistence:
    def __init__(self, gender: Gender = 'M', prs: person = person('M')):
        self.person = prs
        self.gender = gender

    def create_char_skecth(self, sketchs):
        return CharSketch(
            gender=self.gender,
            points=self.person.points,
            age=self.person.age,
            amount_life=self.person.amount_age,
            items=self.person.to_inventory(self.person.points.strength*1000, sketchs)
        )
    
    def create_char_skecths(self, items, sketch_quantity: int = 5):
        return [self.create_char_skecth(items) for _ in range(sketch_quantity)]

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
                amount_life=sketch.amount_life,
                inventory=Inventory_add(
                    items=sketch.items
                )
                                ),
            description=descript
        )

    def create_exist(self, sketch: CharSketch, names: tuple | str):
        if type(names) == str:
            names = tuple(names.split(' ', maxsplit=2))
        return Existence_add(
            first_name=names[0],
            last_name=names[1] if len(names) > 1 else None,
            gender=self.gender,
            attibute_point=self.person.points,
            age=self.person.age,
            amount_life=self.person.amount_age,
            inventory=Inventory_add(
                items=sketch.items
            )
        )
    
    def create_char(self, names: str, user_id: int, sketch: CharSketch, descript: str | None = None):
        new_exist = self.create_exist(sketch, names)
        return Character_add(user_id=user_id, exist=new_exist, description=descript)



    







