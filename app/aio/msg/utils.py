import random
import html
import json

class TextHTML:
    def __init__(self, text: str):
        self.text = str(text)

    def blockquote(self, expandable: bool = False):
        """ Цитата
            - expandable: Позволяет сделать цитату разворачиваемой"""
        if expandable:
            return '<blockquote expandable>' + self.text + '</blockquote>'
        return '<blockquote>' + self.text + '</blockquote>'
 
    @property
    def escape(self):
        ''' Экранирование HTML '''
        return html.escape(self.text)
    
    @property
    def unescape(self):
        ''' Обратное экранирование HTML '''
        return html.unescape(self.text)

    @property
    def bold(self):
        ''' Жирный текст '''
        return f'<b>{self.text}</b>'

    @property
    def code(self):
        ''' Моноширный (копируемый) текст '''
        return f'<code>{self.text}</code>'
    
    @property
    def italic(self):
        ''' Курсивный текст '''
        return f'<i>{self.text}</i>'

    def href(self, url: str):
        ''' Ссылка
            - url: Ссылка на ресурс '''
        return f'<a href="{url}">{self.text}</a>'
    
    def custom_emoji(self, emoji_id: str):
        ''' Пользовательская эмодзи
            - emoji_id: ID пользовательской эмодзи '''
        return f'<tg-emoji emoji-id="{emoji_id}">{self.text}</tg-emoji>'
    
    def spoiler(self):
        ''' Скрытый текст (спойлер) '''
        return f'<tg-spoiler>{self.text}</tg-spoiler>'
    
    @classmethod
    def to_list(cls, items: list[str], type: str = 'num', sep: str = '\n'):
        ''' Нумерованный список
            - items: Список элементов 
            - type: Тип списка (num - нумерованный, любой другой - кастомный символ)
            - sep: Разделитель между элементами списка '''
        if type == 'num':
            return cls(sep.join([f'{i+1}. {item}' for i, item in enumerate(items)]))
        elif type == 'bullet':
            return cls(sep.join([f'• {item}' for item in items]))
        else:
            return cls(sep.join([f'{type} {item}' for item in items]))
        
    @classmethod
    def num_list(cls, items: list[str], sep: str = '\n'):
        ''' Нумерованный список
            - items: Список элементов для нумерации
            - sep: Разделитель между элементами списка '''
        return cls.to_list(items, type='num', sep=sep)
    
    def float_format(value, decimals=2):
        """Форматирует число без лишних нулей"""
        formatted = f"{value:.{decimals}f}"
        return formatted.rstrip('0').rstrip('.')
    
    def json_format(json_data: dict, indent: int = 2):
        return json.dumps(json_data, indent=indent)

    def pre(self, language: str = 'python'):
        return f'<pre><code class="language-{language}">{self.text}</code></pre>'

def get_invisibly_edited():
    return str('\u200b'*random.choice(range(10)))   

