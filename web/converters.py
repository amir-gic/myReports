from datetime import datetime , date
import re
from django.core import exceptions
from django.utils import timezone

class DateTimeRange():
    def __init__(self, year, month, day, hour=0, minute=0, second=0, microsecond=0 , range = None):
        self.year = year
        self.month = month
        self.day = day
        self.range = range  # Initialize the range field

    @classmethod
    def check_value(cls, value):
            if re.search(r"\d{4}-\d{1,2}-\d{1,2}",value):
                return "%Y-%m-%d" , "day"
            if re.search(r"\d{4}-\d{1,2}",value):
                return "%Y-%m" , "month"
            if re.search(r"\d{4}",value):
                return "%Y" , "year"
            return None
    
    @classmethod
    def strptime(cls, date_string: str):
        format , rang = cls.check_value(date_string)
        parsed_date =  datetime.strptime(date_string, format)
        datetime_rage =  cls(parsed_date.year , parsed_date.month , parsed_date.day)
        datetime_rage.range = rang
        return datetime_rage
    
    @classmethod
    def today(cls):
        d = timezone.localtime()
        return cls(d.year , d.month , d.day , range = "day")
    
    def strftime(self) -> str:
        format_map = { 
            "day": "%Y-%m-%d",
            "month": "%Y-%m",
            "year": "%Y"
        }
        time = datetime(self.year , self.month , self.day )
        return time.strftime(format_map[self.range])
    def make_date(self) -> date:
        time = datetime(self.year , self.month , self.day).date()
        return time
class DateConverter:

    regex = "\d{4}(-\d{1,2})?(-\d{1,2})?"
    # regex = "\\d{4}-\\d{1,2}-\\d{1,2}"
    # regex = "[0-9]{4}"

    format = "%Y"
    def to_python(self , value):
        return DateTimeRange.strptime(value)

    def to_url(self , value):
        return value.strftime()
        
