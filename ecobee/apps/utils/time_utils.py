from datetime import datetime, timedelta


def dt_to_milliseconds(dt): return dt.timestamp() * 1000


def get_today_dt(): return datetime.now()


def get_half_a_day_ago_dt():
    today = get_today_dt()
    half_a_day = timedelta(hours=12)
    half_a_day_ago = today - half_a_day
    half_a_day_ago = dt_to_milliseconds(half_a_day_ago)
    return half_a_day_ago


def get_yesterday_dt():
    today = get_today_dt()
    yesterday = today - one_day
    yesterday = dt_to_milliseconds(yesterday)
    return yesterday
