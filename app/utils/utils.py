from datetime import datetime


def parse_date(raw_date):
    year, month, day = map(int, raw_date.split('-'))
    return datetime(year=year, day=day, month=month)