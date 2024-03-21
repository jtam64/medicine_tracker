import datetime

def calculate_remaining(quantity:int, modifier:int):
    "Calculate remaining_days and end_date"
    today = datetime.date.today()
    end_date = today + datetime.timedelta(modifier)
    remaining_days = int(quantity / modifier)

    return end_date, remaining_days