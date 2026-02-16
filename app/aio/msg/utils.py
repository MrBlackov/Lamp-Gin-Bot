import random
import html

class TextHTML:
    def __init__(self, text: str):
        self.text = text

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

def get_invisibly_edited():
    return str('\u200b'*random.choice(range(10)))