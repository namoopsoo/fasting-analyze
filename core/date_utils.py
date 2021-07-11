import datetime
import pytz


def utc_ts():
    utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    return utc_now.strftime('%Y-%m-%dT%H%M%S')
