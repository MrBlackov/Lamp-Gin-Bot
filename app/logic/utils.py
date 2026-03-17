from datetime import datetime, timedelta, date, time

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
