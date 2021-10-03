import datetime

# It can get a the execution's time

# yyyymmdd
def get_current_yyyymmdd():
    
    today = datetime.date.today()
    yyyymmdd = today.strftime('%Y%m%d')

    return yyyymmdd

# yyyy-mm-dd
def get_current_yyyy_mm_dd():
    
    today = datetime.date.today()
    yyyymmdd = today.strftime('%Y-%m-%d')

    return yyyymmdd