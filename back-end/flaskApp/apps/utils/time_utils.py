from datetime import datetime, timedelta


def dt_to_milliseconds(dt): return dt.timestamp() * 1000


def get_X_hours_ago_dt(hours):
    today = datetime.now()
    X_hours = timedelta(hours=hours)
    X_hours_ago = today - X_hours
    X_hours_ago = dt_to_milliseconds(X_hours_ago)
    return X_hours_ago
