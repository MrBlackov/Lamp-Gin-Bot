from app.aio.cls.tips.base import TipBase

class NewCharTips(TipBase):
    tips = [
        '❗ Кнопка [↩️ Назад] вернет навыки к изначальному значению',
        '❗ Непотраченные 💮 Очки навыков конвертируются в фунты',
        '❗ Сбалансированные персонажи - ваш лучший выбор',
        '❗ Предметы больше не будут выпадать при создании персонажа',
        '❗ Не тратьте все 💮 Очки навыков, вам еще пригодятся фунты',
    ]

    @property
    def menu(self):
        return self.tips
    
new_char_tips = NewCharTips().menu



