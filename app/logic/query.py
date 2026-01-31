
class LetterSearch:
    def __init__(self, words: list[str]):
        words = [w.lower() for w in words]
        self.words = words

    @property
    def all_letters(self):
        return sorted(set(list(''.join(self.words))))

    @property
    def letter_and_words(self):
        word_and_letters: dict[str, list] = {l:[] for l in self.all_letters}
        for letter in self.all_letters:
            word_on_letter = []
            for word in self.words:
                if letter in word:
                    word_on_letter.append(word)
            word_and_letters[letter] = word_on_letter    
        return dict(sorted(word_and_letters.items()))

    @property
    def word_letter(self):
        return [list(w) for w in self.words]

    @property
    def word_letter_count(self):
        return_dict = {}
        for word in self.words:
            word_composition = {}
            for letter in set(list(word)):
                letter_count = word.count(letter)
                word_composition[letter] = letter_count
            return_dict[word] = word_composition
        return dict(sorted(return_dict.items()))

    def search_for_letters(self, find: str):
        words = list(set([w.lower() for w in self.words]))
        word_congeniality = {}
        find = find.lower()
        if find in words:
            word_congeniality[find] = 100
            words.remove(find)
        if len(words) > 0:
            for w in words:
                min_count = min(len(find), len(w))
                average_value = 99/min_count
                points = 0
                for c in range(min_count):
                    if w[c] == find[c]:
                        points += average_value
                if len(find) > len(w):
                    points /= 2
                if points > 0:
                    word_congeniality[w] = int(points)
        return word_congeniality
    
    def search_for_three_letter(self, find: str):
        words = list(set([w.lower() for w in self.words]))
        find = find.lower() 
        return_words = {}     
        words_three = {}
        find_three = [find[n:n+3] for n in range(len(find)-2)]
        for word in words:         
    
            three = []
            for n in range(len(word)-2):
                three.append(word[n:n+3])
            words_three[word] = sorted(three)
    
        for word, three in words_three.items():   
            average_value = len(find_three)
            count = len(set(three) & set(find_three))
            if count:
                return_words[word] = count
        return return_words

    def search(self, find: str) -> tuple[str]:
        if len(find) > 3:
            result = self.search_for_three_letter(find)
        elif len(find) <= 3:
            result = self.search_for_letters(find)
        search_sort = sorted([tuple([c, n]) for n, c in result.items()], reverse=True)
        return tuple([n for c, n in search_sort])
        


random_words = [
    "кенгуру", "хамелеон и дикобраз", "мангуст", "тукан",
    "алгоритм", "интерфейс", "хостинг", "фреймворк", "гаджет",
    "водопад", "иней", "рассвет", "ущелье", "гейзер",
    "восхищение", "ностальгия", "изумление", "умиротворение", "азарт",
    "гипотеза", "квант", "синтез", "параметр", "формула",
    "импровизация", "колорит", "силуэт", "гармония", "перформанс",
    "зонтик", "скворечник", "веревка", "конверт", "шнурок",
    "карамель", "ватрушка", "маринад", "эспрессо", "гренки",
    "агроном", "картограф", "реставратор", "стилист", "логист",
    "переменная", "случайность", "парадокс", "эпизод", "контекст"
]

print(LetterSearch(random_words).search('хамлон в дкбраз'))

