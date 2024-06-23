from datetime import datetime


def has_been_less_than(days: int, date: datetime):
    return (datetime.now() - date).days < days