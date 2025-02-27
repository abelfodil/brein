from datetime import datetime, timedelta

a_month_ago = datetime.now() - timedelta(days=30)


def has_been_less_than(date: datetime, period: datetime):
    return date > period
