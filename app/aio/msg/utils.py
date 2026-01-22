import random
import html

class TextHTML:
    def __init__(self, text: str):
        self.text = text

    def blockquote(self, expandable: bool = False):
        if expandable: 
            return '<blockquote expandable>' + self.text + '</blockquote>'
        return '<blockquote>' + self.text + '</blockquote>'
 

    @property
    def escape(self):
        return html.escape(self.text)
    
    @property
    def unescape(self):
        return html.unescape(self.text)

def get_invisibly_edited():
    return str('\u200b'*random.choice(range(10)))