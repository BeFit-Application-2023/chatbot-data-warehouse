from datetime import datetime
import holidays

US_HOLIDAYS = holidays.US()

month_int2name = {
    1 : "January",
    2 : "February",
    3 : "March",
    4 : "April",
    5 : "May",
    6 : "June",
    7 : "July",
    8 : "August",
    9 : "September",
    10 : "October",
    11 : "November",
    12 : "December"
}


def unix_to_date_dict(unix):
    date = datetime.utcfromtimestamp(unix)
    month = date.month
    month_str = month_int2name[month]
    year = date.year
    hour = date.hour
    minute = date.minute
    seconds = date.second
    day_of_week = date.weekday() + 1
    is_weekend = True if day_of_week in [6, 7] else False
    is_holiday = True if date.strftime("%d-%m-%Y") in US_HOLIDAYS else False

    return {
        "date" : date,
        "month" : month,
        "month_str" : month_str,
        "year" : year,
        "hour" : hour,
        "minute" : minute,
        "seconds" : seconds,
        "day_of_week" : day_of_week,
        "is_weekend" : is_weekend,
        "is_holiday" : is_holiday
    }


