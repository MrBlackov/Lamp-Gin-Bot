from datetime import datetime, timedelta, date, time
import random
import string
import re

def generate_date_range(start_date: date = date(1, 1, 1), 
                        end_date: date = date(1, 1, 1), 
                        start_time: time = time(), 
                        end_time: time = time(), 
                        sep: timedelta = timedelta(days=1)) -> list[datetime]:
    dates = []
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)
    current_date = start_datetime
    
    while current_date <= end_datetime:
        dates.append(current_date)
        current_date += sep
    
    return dates

def random_date(start_date, end_date, n: int = 1, sep: timedelta = timedelta(days=1)):
    date_range = generate_date_range(start_date, end_date, sep=sep)
    return random.sample(date_range, n)

def random_time(start_time, end_time, n: int = 1, sep=timedelta(minutes=1)):
    date_range = generate_date_range(start_time=start_time, end_time=end_time, sep=sep)
    return random.sample(date_range, n)

def generate_password(length=12, use_digits=True, use_punctuation=True):
    chars = string.ascii_letters
    if use_digits:
        chars += string.digits
    if use_punctuation:
        chars += string.punctuation
    
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def roll_dice(dice_string):
    
    if '+' in dice_string:
        match = re.match(r'(\d+)d(\d+)(?:\+(\d+))?', dice_string)
        if not match:
            return None
        
        count, sides, bonus = match.groups()
        bonus = int(bonus) if bonus else 0
    else:
        match = re.match(r'(\d+)d(\d+)(?:\-(\d+))?', dice_string)
        if not match:
            return None
        
        count, sides, bonus = match.groups()
        bonus = int(bonus) if bonus else 0
        bonus = -bonus
        
    rolls = [random.randint(1, int(sides)) for _ in range(int(count))]
    total = sum(rolls) + bonus
        

    return {
        'rolls': rolls,
        'bonus': bonus,
        'total': total
    }


print('\n'.join([str(roll_dice('3d20+20')) for _ in range(100)]))