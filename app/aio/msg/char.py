from app.validate.api.characters import CharSketchInfo
from app.validate.info.characters import CharacterInfo
from app.aio.msg.utils import TextHTML
from app.db.models.item import ItemDB
from app.aio.msg.item import ItemText

class SketchInfoText:

    def __init__(self, sketch: CharSketchInfo):
        self.sketch = sketch

    @property
    def ST(self):
        return self.sketch.points.strength

    @property
    def IQ(self):
        return self.sketch.points.intelligence

    @property
    def HT(self):
        return self.sketch.points.health
    
    @property
    def DX(self):
        return self.sketch.points.dexterity
    
    @property
    def speed_bonus(self):
        return self.sketch.points.speed_value
    
    @property
    def spirituality(self):
        return self.sketch.points.spirituality
    
    @property 
    def age(self):
        return self.sketch.age

    @property
    def template(self) -> str:
        return '💪 Сила: {ST} \n' \
               '🤸‍♂️ Ловкость: {DX} \n' \
               '🧑‍🎓 Интелект: {IQ} \n' \
               '❤️ Здоровье: {HT} \n' \
               '🏃 Бонус к Скорости: {SPEED_BONUS} \n' \
               '🔮 Духовность: {SPIRITUALITY} \n' \
               '⌛ Возраст: {AGE} \n' \
               #'🪙 Пенни: {PENNY}(фунтов: {LBS})'

    @property
    def gender_template(self):
        return '{GENDER}\n' + self.template

    @property
    def text(self):
        return self.to_text()
    
    def to_text(self, and_gender: bool = False):
        format_dict = {            
            'ST':self.ST,
            'DX':self.DX,
            'IQ':self.IQ,
            'HT':self.HT,
            'SPEED_BONUS':self.speed_bonus,
            'SPIRITUALITY':self.spirituality,
            'AGE':self.age,
            #'PENNY':self.sketch.penny,
            #'LBS':self.sketch.penny//400
            }
        
        if and_gender: 
            format_dict |= {'GENDER':'👨 Пол: Мужской' if self.gender == 'M' else '👩 Пол: Женский'}
            return self.gender_template.format(**format_dict)

        return self.template.format(**format_dict)
    
    @property
    def gender(self):
        return self.sketch.gender

class CharInfoText:
    def __init__(self, char: CharacterInfo):
        self.char = char

    @property
    def ST(self):
        return self.char.exist.attibute_point.strength

    @property
    def IQ(self):
        return self.char.exist.attibute_point.intelligence

    @property
    def HT(self):
        return self.char.exist.attibute_point.health
    
    @property
    def DX(self):
        return self.char.exist.attibute_point.dexterity
    
    @property
    def speed_bonus(self):
        return self.char.exist.attibute_point.speed_value
    
    @property
    def spirituality(self):
        return self.char.exist.attibute_point.spirituality
    
    @property 
    def age(self):
        return self.char.exist.age

    @property
    def descript(self):
        return self.char.description
    
    @property
    def full_name(self):
        return self.char.exist.full_name
    
    @property
    def char_id(self):
        return self.char.id

    @property
    def temlate_exist_points(self) -> str:
        return '💪 Сила: {ST} \n' \
               '🤸‍♂️ Ловкость: {DX} \n' \
               '🧑‍🎓 Интелект: {IQ} \n' \
               '❤️ Здоровье: {HT} \n' \
               '🏃 Бонус к Скорости: {SPEED_BONUS} \n' \
               '🔮 Духовность: {SPIRITUALITY} \n' \
               '⌛ Возраст: {AGE} \n' \
               #'🪙 Пенни: {PENNY}(фунтов: {LBS})'

    @property
    def template_full_name(self):
        return '🪪 {FULL_NAME} ({ID}) \n'
    
    @property
    def text(self):
        texts = [
            self.template_full_name.format(FULL_NAME=self.full_name, ID=self.char_id),
            TextHTML(self.temlate_exist_points.format(**{            
            'ST':self.ST,
            'DX':self.DX,
            'IQ':self.IQ,
            'HT':self.HT,
            'SPEED_BONUS':self.speed_bonus,
            'SPIRITUALITY':self.spirituality,
            'AGE':self.age,
            #'PENNY':self.char.exist.saving.penny,
            #'LBS':self.char.exist.saving.penny//400
            })).blockquote()]
        
        if self.descript:
            texts.append('📜 Описание')
            texts.append(TextHTML(self.descript).blockquote(True))

        return ''.join(texts)
    
class InventoryItemsText:
    def inventory(size: int, max_sixe: int):
        return f'Ваш инвентарь [{size}/{max_sixe}кг]'
    
    def no_items():
        return 'Ваш инвентарь пустой'
    
    def throw():
        return 'Сколько выбросить?'

    def item(item: ItemDB):
        return ItemText(item).text