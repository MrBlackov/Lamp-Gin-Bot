from app.db.models.item import ItemDB, ItemSketchDB
from app.db.models.char import CharacterDB
from app.validate.sketchs.item_sketchs import ItemSketchValide, ItemValide
from app.aio.msg.utils import TextHTML
from app.logic.actions import ActionTags
from app.validate.item import BookValide

class ItemText:
    def __init__(self, item: ItemDB):
        self.sketch = item.sketch
        self.item = item
 
    @property
    def dop_text(self):
        texts = []
        if ActionTags.paper in self.sketch.action:
            text = self.item.nbt.get('text')
            texts.append(f'📄 Надпись (отсуствует)' if type(text) != str else f'📄 Надпись \n\n' + text.replace('emoji_id', 'emoji-id'))
        if ActionTags.book in self.sketch.action:
            text: dict = self.item.nbt.get('book')
            if text:
                book = BookValide.model_validate(text)
                texts.append(
                    f'🏷️ {book.name}' + TextHTML('\n'.join([
                        f'👤 Автор: {book.author}',
                        f'✏️ Можно редактировать: {'✅' if not(book.is_close_setting) else '❌'}',
                        (f'📊 Кол-во страниц: {len(book.pages)}' if book.pages and len(book.pages) > 0 else '❌ Страниц нету'),
                        f'📜 Описание: {book.description if book.description and len(book.description) > 0 else "❌"}'
                    ])).blockquote()
                )
            else:
                texts.append(f'❗ Вы можете написать книгу')
        return '\n' + '\n'.join(texts)

    @property
    def temperate(self):
        return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '♠️ Предмет ID: {ITEMID}',
            '♣️ Эскиз ID: {SKETCHID}',
            '📊 Кол-во: {QUANTITY}',
            '⏲️ Вес одного: {WEIGHT}кг',
            '🧳 Общий вес: {ALLWEIGHT}кг',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote() + '\n{DOP}'
 
    @property    
    def text(self):
        value = self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            QUANTITY=self.item.quantity,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            ALLWEIGHT=self.sketch.size*self.item.quantity/1000,
            ITEMID=self.item.id,
            SKETCHID=self.sketch.id,
            DOP=self.dop_text
        )
        return value

class NewItemText:
    def __init__(self, sketch: ItemSketchValide):
        self.sketch = sketch
 
    def text(self):
        return ('{EMODZI} {NAME}' + TextHTML('\n'.join([
            '🏷️ Тэг: {TAG}',
            '⏲️ Вес одного: {WEIGHT}кг',
            #'🎲 Шанс выпадения: {RARITY}%'
            #] + ([
            #'📈 Макс. выпадения: {MAX_DROP}',
            #'📉 Мин. выпадения: {MIN_DROP}' ] if self.sketch.rarity > 0 else []) + [
            '🎟️ Действия: {ACTION_TAGS}',
            '📑 NBT: {NBT}',
        ])).blockquote()).format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            WEIGHT=self.sketch.size/1000,
            RARITY=self.sketch.rarity*100,
            MAX_DROP=self.sketch.max_drop,
            MIN_DROP=self.sketch.min_drop,
            TAG=self.sketch.tag,
            ACTION_TAGS='✅' if self.sketch.action and len(self.sketch.action) > 0 else '❌',
            NBT='✅' if self.sketch.nbt and len(self.sketch.nbt) > 0 else '❌'
        ) + '\n📜 Описание' + TextHTML(self.sketch.description if self.sketch.description else '❌').blockquote(True)
    
    def to_redact_text(redact_key: str):
        match redact_key:
            case 'name':
                return '✒️ Отправьте имя предмета. Количество символов должно быть не больше 30'
            case 'emodzi':
                return '✒️ Отправьте эмодзи для предмета. Эмодзи должен быть 1'
            case 'size':
                return '✒️ Отправьте вес одного предмета в граммах. Вес должен быть целым числом'
            case 'description':
                return '✒️ Отправьте описание для предмета. Количество символов должно быть не больше 200'
            case 'rarity':
                return '✒️ Отправьте редкость предмета в виде десятичной дроби от 0 до 1. Например, 0.1 будет означать 10% шанс выпадения'
            case 'max_drop':
                return '✒️ Отправьте максимальное количество предметов, которое может выпасть. Должно быть целым числом'
            case 'min_drop':
                return '✒️ Отправьте минимальное количество предметов, которое может выпасть. Должно быть целым числом и не больше максимального количества'
            case 'creator_id':
                return '✒️ Отправьте user_id создателя'
            case 'tag':
                return '✒️ Отправьте тег предмета. Тег должен быть уникальным и состоять из букв латинского алфавита в нижнем регистре'
            case 'nbt':
                return '✒️ Отправьте NBT-данные предмета. Данные должны быть в формате JSON. Старые данные перезапишутся!'
            case _:
                return '✒️ Отправьте значение'
            
    def nbt(self, lang: str = 'python'):
        return '\n📑 NBT' + (TextHTML(TextHTML.json_format(self.sketch.nbt)).pre(lang) if self.sketch.nbt else TextHTML('❌').blockquote())


class ItemSketchText:
    def __init__(self, sketch: ItemSketchDB):
        self.sketch = sketch
 
    @property
    def temperate(self):
        if self.sketch.rarity == 0:
            return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '⏲️ Вес одного: {WEIGHT}кг',
            '🎲 Шанс выпадения: {RARITY}%',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()
        return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '⏲️ Вес одного: {WEIGHT}кг',
            '🎲 Шанс выпадения: {RARITY}%',
            '📈 Макс. выпадения: {MAX_DROP}',
            '📉 Мин. выпадения: {MIN_DROP}',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()
 
    @property
    def temperate_admin(self):
        return '{EMODZI} {NAME}' + TextHTML('\n'.join([
            '👤 Создатель: {USER_ID}',
            '♣️ Эскиз ID: {ID}',
            '⏲️ Вес одного: {WEIGHT}кг',
            '🎲 Шанс выпадения: {RARITY}%',
            '📈 Макс. выпадения: {MAX_DROP}',
            '📉 Мин. выпадения: {MIN_DROP}',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()
    
    def text(self, is_admin: bool = False):
        if is_admin:
            value = self.temperate_admin.format(
            USER_ID=self.sketch.creator_id,
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            ID=self.sketch.id,
            RARITY=self.sketch.rarity*100,
            MAX_DROP=self.sketch.max_drop,
            MIN_DROP=self.sketch.min_drop
        )
            return value
        if self.sketch.rarity == 0:
            return self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            RARITY=str(self.sketch.rarity*100)[:6]
        )
        return self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            RARITY=str(self.sketch.rarity*100)[:6],
            MAX_DROP=self.sketch.max_drop,
            MIN_DROP=self.sketch.min_drop
        )

    def change_text(self):
        return ('{EMODZI} {NAME} ' + f'({'👁️ Предмет виден' if not self.sketch.is_hide else '🌫️ Предмет скрыт'})' + TextHTML('\n'.join([
            '👤 Создатель: {USER_ID}',
            '♣️ Эскиз ID: {ID}',
            '🏷️ Тэг: {TAG}',
            '⏲️ Вес одного: {WEIGHT}кг',
            '🎲 Шанс выпадения: {RARITY}%',
            '📈 Макс. выпадения: {MAX_DROP}',
            '📉 Мин. выпадения: {MIN_DROP}',
            '🎟️ Действия: {ACTION_TAGS}',
            '📑 NBT: {NBT}',
            
        ])).blockquote()).format(
            USER_ID=self.sketch.creator_id,
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            WEIGHT=self.sketch.size/1000,
            ID=self.sketch.id,
            RARITY=self.sketch.rarity*100,
            MAX_DROP=self.sketch.max_drop,
            MIN_DROP=self.sketch.min_drop,
            TAG=self.sketch.tag,
            ACTION_TAGS='✅' if self.sketch.action and len(self.sketch.action) > 0 else '❌',
            NBT='✅' if self.sketch.nbt and len(self.sketch.nbt) > 0 else '❌'
        ) + '\n📜 Описание' + TextHTML(self.sketch.description if self.sketch.description else '❌').blockquote(True)
    
    def nbt(self, lang: str = 'json'):
        return '\n📑 NBT' + (TextHTML(TextHTML.json_format(self.sketch.nbt)).pre(lang) if self.sketch.nbt else TextHTML('❌').blockquote())

    def action(self, lang: str = 'json'):
        return '\n🎟️ Действия' + (TextHTML(TextHTML.json_format(self.sketch.action)).pre(lang) if self.sketch.nbt else TextHTML('❌').blockquote())

    def moderate_sketch(self):
        
        return self.change_text() + self.nbt() + self.action()

class CharItemText:    
    def __init__(self, char: CharacterDB, item: ItemDB):
        self.sketch = item.sketch
        self.item = item
        self.char = char

    @property
    def temperate(self):
        return ''.join(['{FULL_NAME}'+ TextHTML('\n'.join([
            '👤 ID: {CHARID}',
            '🪪 User ID: {USERID}',
            '💼 Макс. вес: {MAX_SIZE}кг'
        ])).blockquote(),
            '\n {EMODZI} {NAME}' + TextHTML('\n'.join([
            '♠️ Предмет ID: {ITEMID}',
            '♣️ Эскиз ID: {SKETCHID}',
            '📊 Кол-во: {QUANTITY}',
            '⏲️ Вес одного: {WEIGHT}кг',
            '🧳 Общий вес: {ALLWEIGHT}кг',
            '📜 Описание: {DESCRIPT}',
        ])).blockquote()])
    
    @property    
    def text(self):
        value = self.temperate.format(
            EMODZI=self.sketch.emodzi,
            NAME=self.sketch.name,
            QUANTITY=self.item.quantity,
            DESCRIPT=self.sketch.description if self.sketch.description else '❌',
            WEIGHT=self.sketch.size/1000,
            ALLWEIGHT=self.sketch.size*self.item.quantity/1000,
            ITEMID=self.item.id,
            SKETCHID=self.sketch.id,
            FULL_NAME=self.char.exist.full_name,
            CHARID=self.char.id,
            USERID=self.char.user_id,
            MAX_SIZE=self.char.exist.attibute_point.strength
        )
        return value