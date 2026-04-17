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

def action_point(points: list[int | float | list]) -> float | int:
    p = 0
    for point in points:
        if type(point) == int or type(point) == float:
            p += point
        elif type(point) == list:
            p += action_point(point)
    
    return p/len(points)
