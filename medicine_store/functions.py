import datetime

def calculate_remaining(quantity:int, modifier:int):
    "Calculate remaining_days and end_date"
    today = datetime.date.today()

    remaining_days = int(quantity / modifier)
    
    end_date = today + datetime.timedelta(days=remaining_days)

    return end_date, remaining_days